# Install

```console
$ pip install snakemake-wfcommons
```

# Integrate into Snakemake

Call `wfcommons-converter` in the top-level `all` rule of your workflow to automatically convert the executed workflow into WfFormat like this:

```snakemake
rule all:
    input:
        <your finale result file>
    shell:
        "wfcommons-converter [<workflow-name.json>]"
```
