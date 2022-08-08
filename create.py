#!/usr/bin/env python3
import argparse
import fileinput
import logging
import os
import requests
from shutil import copytree
import sys


def process_arguments():
    desc = ('Create a skeleton for a new TryHackMe writeup\n'
            'It will be create as sub-directory in the current working directory.\n')
    parser = argparse.ArgumentParser(
        description=desc, formatter_class=argparse.RawTextHelpFormatter)

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-u', '--url', required=True,
                          help='URL of the lab')
    required.add_argument('-t', '--title', required=True,
                          help='Title of the lab, used as directory name')

    optional.add_argument('-d', '--debug', action='store_true',
                          help='Even more verbose output')
    args = parser.parse_args()

    log_format = '[%(levelname)8s] %(message)s'
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format=log_format)
    else:
        logging.basicConfig(level=logging.INFO, format=log_format)

    return args


def check_config(args):
    return True


def get_details(args):
    d = {}
    d['title'] = args.title
    d['url'] = args.url
    return d


def create_skeleton(details):
    template_dir = f'{os.path.dirname(os.path.realpath(__file__))}/.templates'
    target_dir = os.path.join(os.getcwd(), details['title'].replace(' ', '_'))

    copytree(template_dir, target_dir)

    for file in os.listdir(target_dir):
        logging.debug(f'file: {file}')

        if not os.path.isfile(f'{target_dir}/{file}'):
            continue

        for line in fileinput.input(f'{target_dir}/{file}', inplace=1):
            line = line.replace('<LAB_NAME>', details['title'])
            line = line.replace('<LAB_LINK>', details['url'])
            print(line, end='')


def main():
    args = process_arguments()
    if not check_config(args):
        logging.error(f'Invalid state in arguments: {args}')
        sys.exit(-1)

    details = get_details(args)
    if not details:
        sys.exit(-2)

    create_skeleton(details)


if __name__ == "__main__":
    main()
