# contribution-stats

Copyright (c) 2021-2022 [Antmicro](https://antmicro.com)

This repository contains a simple script that can be used to calculate code authorship inside a git repository.
Note that it uses git-blame to make the decisions.

Here is an example on how to use that:

Clone this repository:

```
git clone https://github.com/antmicro/contribution-stats.git
```

Install dependencies:

```
pip3 install GitPython argparse pyyaml
```

Run the script:
```
cd contribiution-stats
./contribution_stats.py --configs-dir ../configs --config sv-tests https://github.com/SymbiFlow/sv-tests.git
```

The script skips all submodules.

Run `./contribution_stats.py --help` for list of all available options:

```
./count_contribution.py --help
usage: contribution_stats.py [-h] [--config {sv-tests}] [--skip_folders SKIP_FOLDERS [SKIP_FOLDERS ...]]
                             [--mail_aliases MAIL_ALIASES] [--threshold THRESHOLD]
                             url

Git contributors stats

positional arguments:
  url                   Repository URL

optional arguments:
  -h, --help            show this help message and exit
  --configs-dir CONFIGS_DIR
                        Path to configs directory
  --config CONFIG       Use predefined config
  --skip_folders SKIP_FOLDERS [SKIP_FOLDERS ...]
                        List of folders (within the repository) to be excluded from analisys
  --mail_aliases MAIL_ALIASES
                        Provide yaml file with email aliases
  --threshold THRESHOLD
                        Print contributors with contributions above given percent (default 0)
```
