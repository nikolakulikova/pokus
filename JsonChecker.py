import json
import time

import jsonschema


class JsonChecker:

    def __init__(self, file: str, schema: str):
        self.file = file
        self.file_schema = json.load(open(schema))

    @staticmethod
    def _reformat_errors(errors: list) -> list:
        """
        reformat errors given by jsonValidator, to have more usefull information for user
        """
        result = []
        for error in errors:
            error = str(error).split("\n")
            whats_wrong = ""

            # TODO doskusat moznosti
            if "not of type" in error[0]:
                key = error[-2]
                whats_wrong = f"wrong type of key {key[key.index('[') + 1: key.index(']')]} ({error[0]})"
            if "required property" in error[0]:
                key = error[0].split("is")[0].replace('"', "", 2)
                whats_wrong = f" missing key {key} in json file"

            result.append(whats_wrong)

        return result

    @staticmethod
    def _change(json: str, to_change: str, position: int) -> str:
        """
        change json string by error and create new string to be use for next load
        """
        new_json = ""
        for i in range(len(json)):
            if i == position:
                new_json += to_change
            new_json += json[i]
        return new_json

    @staticmethod
    def _check_brackets(json: str) -> (set, str):
        """
        check brackets which are in json, add missing brackets for better checking
        """
        results = set()
        result_string = ""
        split_json = json.split("\n")
        stack = []

        for number, line in enumerate(split_json):
            for char in line:
                if char in "{[":
                    stack.append(char)
                    result_string += char
                    continue
                if char in "}]":
                    if len(stack) != 0:
                        opened = stack.pop()
                        if char == "}" and opened == "{":
                            result_string += char
                            break
                        if char == "]" and opened == "[":
                            result_string += char
                            break
                        if char == "}" and opened != "{":
                            result_string += "]"
                            results.add(f"line {number + 1} error missing closing ]")
                            continue
                        if char == "]" and opened != "[":
                            result_string += "}"
                            results.add(f"line {number + 1} error missing closing {'}'}")
                if len(stack) == 0:
                    if char == "}":
                        results.add(f"line {number + 1} error more {'}'} than needed")
                    if result_string.strip()[-1] == "}":
                        continue
                    else:
                        result_string += char
                else:
                    result_string += char
            result_string += "\n"
        result_string = result_string[:-1]
        if stack:
            for item in reversed(stack):
                if item == "{":
                    result_string += "}"
                else:
                    result_string += "]"
                results.add(f"line: {number + 1} error: unclosed {item}")

        return results, result_string

    @staticmethod
    def _change_quotes(json: str, line_num: int) -> str:
        pom = json.split("\n")
        num = 0
        for n, line in enumerate(pom):
            for char in line:
                if char == "'":
                    num += 1
            if n == line_num:
                break
        return json.replace("'", '"', num)

    def _change_json_by_error(self, to_change: str, position: int, json: str, line: int = 0) -> str:
        copy_json = ""

        if to_change.count(",") != 0:
            to_change = ","
            copy_json = self._change(json, to_change, position)
        elif to_change.count("value") != 0:
            to_change = '"string"'
            copy_json = self._change(json, to_change, position)
        elif to_change.count("Invalid control character") != 0:
            to_change = '"'
            copy_json = self._change(json, to_change, position)
        elif to_change == "Expecting ':' delimiter":
            to_change = ":"
            copy_json = self._change(json, to_change, position)
        elif to_change.count("double quotes") != 0:
            if json.count("'") != 0:
                copy_json = self._change_quotes(json, line)
            else:
                to_change = '"'
                copy_json = self._change(json, to_change, position)

        return copy_json

    def check(self) -> list:
        """
        first check syntax by load json file, then check keys and values used in file by schema,
        return all error, if error appeared in first check -> not checking keys and values
        :return list of errors
        """

        # check if it has not syntax error
        file = open(self.file, "r")
        try:
            file_to_check = json.load(file)
        except:
            file.close()
            print("mas syntax error")
            copy_json = open(self.file, "r").read()
            errors = set()
            error, copy_json = self._check_brackets(copy_json)
            last_error = ""
            count_last = 0
            for i in error:
                errors.add(i)
            while True:
                try:
                    _ = json.loads(copy_json)
                    break
                except ValueError as e:
                    copy_json = self._change_json_by_error(e.msg, e.pos, copy_json, e.lineno - 1)
                    if count_last == 10:
                        print(errors)
                        return errors
                    if last_error == e.msg:
                        count_last += 1
                    else:
                        last_error = e.msg
                        count_last = 0
                    errors.add(e.args[0])


            print(errors)
            return errors
        finally:
            file.close()

        # check keys and values by schema
        validator = jsonschema.Draft7Validator(self.file_schema)
        result = validator.iter_errors(instance=file_to_check)
        print(self._reformat_errors(result))
        return result
