#!/usr/bin/env python3

import sys
import tempfile
import git
import re
import yaml
import os
import argparse

botstrings = ['[bot]']

class PathFilter:
    def __init__(self, exclude_dirs):
        self.exclude_dirs = exclude_dirs

    def __call__(self, blob) -> bool:
        for d in self.exclude_dirs:
            if blob[1].path.startswith(d):
                #print("blob", blob[1].path, "dir", d)
                return False
        return True

def load_config(config, configs_dir):
    config_dir = os.path.join(configs_dir, config)
    with open(os.path.join(config_dir, 'mail_aliases.yml')) as fd:
        mail_aliases = yaml.load(fd, Loader=yaml.FullLoader)

    with open(os.path.join(config_dir, 'skip_folders')) as fd:
        skip_folders = list(filter(None, fd.read().split('\n')))

    with open(os.path.join(config_dir, 'threshold')) as fd:
        threshold = float(fd.read())

    return mail_aliases, skip_folders, threshold

def is_bot(mail):
    for s in botstrings:
        if s in mail:
            return True
    return False

def get_org(mail):
    domain = mail.split('@')[-1]
    return domains.get(domain, mail)

def get_alias(mail):
    return mail_aliases.get(mail, mail)

def main(url, skip_folders=None, mail_aliases=None, threshold=0):

    directory = tempfile.TemporaryDirectory(prefix='contribution-checker')

    print("Cloning ...")

    repo = git.Repo.clone_from(url, directory.name)
    stats = {}
    lines_count = 0

    print("Processing ...")

    for blob in repo.index.iter_blobs(PathFilter(skip_folders)):
        blame = repo.git.blame(blob[1].path, '--show-email', '-w')
        for line in blame.split('\n'):
            m = re.match(".*\(<(.*?@.*?)>", line)
            mail = get_alias(m.group(1))
            if is_bot(mail):
                continue
            owner = get_org(mail)
            lines_count = lines_count + 1
            if owner not in stats:
                stats[owner] = 1
            else:
                stats[owner] = stats[owner] + 1

    print("Contributors with contribution above {}% are".format(threshold))
    for entry in sorted(stats, key=lambda e: stats[e], reverse=True):
        percent = stats[entry]/lines_count*100
        if percent < threshold:
            return
        print(entry, ':', "{:.2f}".format(percent))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Git contributors stats')
    parser.add_argument('--configs-dir', type=str,
                        help="Path to configs directory")
    parser.add_argument('--config', type=str,
                        help='Use predefined config')
    parser.add_argument('--skip_folders', action='append', nargs="+", default=[],
                        help='List of folders (within the repository) to be excluded from analisys')
    parser.add_argument('--mail_aliases', type=str, default={}, help='Provide yaml file with email aliases')
    parser.add_argument('--threshold', type=int, default=0, help='Print contributors with contributions above given percent (default 0)')
    parser.add_argument('url', nargs=1, help='Repository URL')

    args = parser.parse_args()

    if args.config:
        mail_aliases, skip_folders, threshold = load_config(args.config, args.configs_dir)
    else:
        mail_aliases = None
        if args.mail_aliases:
            with open(args.mail_aliases) as fd:
                mail_aliases = yaml.load(fd, Loader=yaml.FullLoader)
        skip_folders = args.skip_folders
        threshold = args.threshold

    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(script_dir+'/domains.yml') as fd:
        domains = yaml.load(fd, Loader=yaml.FullLoader)

    main(
        url=args.url[0],
        mail_aliases=mail_aliases,
        skip_folders=skip_folders,
        threshold=threshold
        )

