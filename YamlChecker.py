import yaml
from cerberus import Validator


class YamlChecker:

    def __init__(self, file: str, schema: str):
        self.file = file
        self.schema = schema

    def load_doc(self):
        with open(self.file, 'r') as file:
            try:
                return yaml.load(file, yaml.FullLoader)
            except yaml.YAMLError as exception:
                return f" error {exception}"
            finally:
                file.close()

    def _proceed_errors(self, errors: dict) -> list:
        error = []
        error_keys = list(errors.keys())
        with open(self.file, 'r') as file:
            for num, line in enumerate(file):
                for key in error_keys:
                    if key in line:
                        error.append(f"error {key}: {errors[key]} at line {num + 1}")
                        break
            file.close()
        for key in error_keys:
            was_key = False
            for e in error:
                if key in e:
                    was_key = True
                    break
            if not was_key:
                error.append(f"error {key} missing : {errors[key]}")
        print("\n".join(error))
        return error

    def check(self):
        errors = []
        if "docker-compose" in self.file:
            ...
        else:
            schema = eval(open(self.schema, 'r').read())
            v = Validator(schema)
            doc = self.load_doc()
            if "error" in doc:
                print(doc)

                return doc
            v.validate(doc, schema)
            errors = v.errors

            errors = self._proceed_errors(errors)
        return errors
