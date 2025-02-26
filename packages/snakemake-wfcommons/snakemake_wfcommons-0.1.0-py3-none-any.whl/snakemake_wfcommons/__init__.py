# SPDX-FileCopyrightText: 2025 Technische Universität Dresden, Germany <tu-dresden.de/zih>
# SPDX-License-Identifier: BSD-3-Clause

import base64, json, io, sys
from pathlib import Path
from collections import defaultdict
from wfcommons import *
from datetime import datetime

class makespan:
    def __init__(self):
        self.start = sys.float_info.max
        self.end = 0
    def add_task(self, start, end):
        self.start = min(start, self.start)
        self.end = max(end, self.end)

class SnakemakeToWfFormat:
    def __init__(self, output_json=None):
        self.metadata_dir = Path("./.snakemake/metadata")
        self.span = makespan()
        self.categories = defaultdict(int)
        task_list = [ self.convert_file(x) for x in self.metadata_dir.glob('**/*') if x.is_file() ]
        wms_version = ''
        try:
            import snakemake._version
            wms_version = snakemake._version.get_version()['version']
        except:
            pass
        wf = common.Workflow(name="snakemake",
                             description = "Snakemake converter",
                             wms_name = "Snakemake",
                             wms_version = wms_version,
                             wms_url = 'https://snakemake.github.io',
                             executed_at = self.span.start,
                             makespan = self.span.end - self.span.start)
        for t in task_list:
            wf.add_task(t)
        for t in task_list:
            output_files = [ o for o in t.files if o.link == common.FileLink.OUTPUT]
            for o in output_files:
                for u in task_list:
                    input_files = [i for i in u.files if i.link == common.FileLink.INPUT]
                    for i in input_files:
                        if(i.name == o.name):
                            wf.add_dependency(t.name, u.name)
        wf.write_json(output_json if output_json is not None else 'snakemake.json')

    def make_file(self, filename, link_type):
        link = common.FileLink(link_type)
        return common.File(filename, Path(filename).stat().st_size if Path(filename).exists() else 0, link)

    def decode_output(self, filename):
        components = str(filename.relative_to(self.metadata_dir)).split('/')
        full = ''.join([c[1:] for c in components[:-1]] + [components[-1]])
        return base64.b64decode(full).decode()

    def convert_file(self, filename):
        metadata = json.load(open(filename, "r"))
        self.span.add_task(start = metadata['starttime'], end = metadata['endtime'])
        output_files = [ self.make_file(self.decode_output(filename), "output") ]
        input_files = [self.make_file(f, "input") for f in metadata['input']]
        self.categories[metadata['rule']] += 1
        cmdline = metadata['script'] if 'script' in metadata else metadata['shellcmd']
        prg = cmdline
        argv = []
        if cmdline is not None:
            argv = cmdline.split()
            prg = argv.pop(0)
        return common.Task(task_id = metadata['job_hash'],
                           name = f"{metadata['rule']}_{self.categories[metadata['rule']]}",
                           category = metadata['rule'],
                           task_type = common.TaskType.COMPUTE,
                           runtime = metadata['endtime'] - metadata['starttime'],
                           files = output_files + input_files,
                           program = prg,
                           args = argv,
                           start_time = datetime.fromtimestamp(metadata['starttime']).isoformat())
