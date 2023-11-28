import xmlschema


class XmlChecker:

    def __init__(self, file: str, schema: str):
        self.file = file
        self.file_schema = schema

    def check(self) -> list:
        '''
        first check syntax by load json file, then check keys and values used in file by schema,
        return all error, if error appeared in first check -> not checking keys and values
        :return list of errors
        '''

        with open(self.file, "r") as file:
            xml_string = file.read()
        schema = xmlschema.XMLSchema(self.file_schema)
        validation_error_iterator = schema.iter_errors(xml_string)
        errors = []
        for idx, validation_error in enumerate(validation_error_iterator, start=1):
            if "Unexpected child with tag" in validation_error.reason:
                error_index = self._get_row_index_unexpected_child(xml_string, validation_error.path, validation_error.reason)
            else:
                error_index = self._get_row_index(xml_string, validation_error.path)
            errors.append(f"line {error_index} {validation_error.reason}")
        print("\n".join(errors))
        return errors

    @staticmethod
    def _get_row_index_unexpected_child(file: str, path: str, reason: str) -> int:

        file = file.strip().split("\n")
        path = path[1:].strip().split("/")
        element = reason[reason.index("'") + 1:]
        element = element[:element.index("'")]
        position = int(reason[reason.index("position") + 8: reason.index(".")].strip()) - 1

        new_path = []
        for p in path:
            if p.count("[") != 0:
                p = p[:p.index("[")]
                new_path.append(p)
            else:
                new_path.append(p)

        el = ""
        for num, line in enumerate(file):
            line = line.strip()
            if line in ["\n", ""]:
                continue
            if line.count("xml version") != 0:
                continue
            if len(new_path) == 0:
                if el == "":
                    if line.count("<") == 0:
                        continue
                    pom = line[1:]
                    for char in pom:
                        if char not in [" ", ">"]:
                            el += char
                        else:
                            break
                if f"/{el}" in line:
                    el = ""
                    position -= 1
                    continue
                if element in line:
                    if position == 0:
                        return num + 1
            elif new_path[0] in line:
                new_path = new_path[1:]
                continue



    @staticmethod
    def _get_row_index(file: str, path: str) -> int:
        """
            check file by given path and return the index of row in which was error
        """
        file = file.strip().split("\n")
        path = path[1:].strip().split("/")
        new_path = []
        stop_at = None
        stop_num = 0
        for p in path:
            if p.count("[") != 0:
                el_number = int(p[p.index("[") + 1: p.index("]")]) - 1
                p = p[:p.index("[")]
                stop_at = p
                stop_num = el_number
            else:
                new_path.append(p)
        if stop_at is None:
            stop_at = new_path[-1]
            new_path = new_path[:-1]

        for num, line in enumerate(file):
            if line in ["\n"]:
                continue
            if line.count("xml version") != 0:
                continue
            if len(new_path) == 0:
                if f"/{stop_at}" in line:
                    continue
                if stop_at in line:
                    if stop_num == 0:
                        return num + 1
                    else:
                        stop_num -= 1
            elif new_path[0] in line:
                new_path = new_path[1:]
                continue
        return num + 1

