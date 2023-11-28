import argparse
import json

import jsonschema

from DockerChecker import DockerChecker
from JsonChecker import JsonChecker
from XmlChecker import XmlChecker
from YamlChecker import YamlChecker


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", help=" schema of given file", default=None)
    parser.add_argument("--file", help="file to check", default=None)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    file = args.file  # "example.json"
    file = "files/example.yaml"
    file = "files/docker-compose.yaml"
    file_p = "files/"
    schema = args.schema  # json.load(open("schema.json"))
    schema = "files/schema.py"
    schema = "files/docker-compose-schema.py"

    if ".json" in file:
        checker = JsonChecker(file, schema)
        result = checker.check()
    if ".xml" in file:
        checker = XmlChecker(file, schema)
        result = checker.check()
    if ".yaml" in file:
        checker = YamlChecker(file, schema)
        result = checker.check()
    else:
        checker = DockerChecker(file_p, file)
        result = checker.check()
