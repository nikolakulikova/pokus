import subprocess

from dockerfile_parse import DockerfileParser


class DockerChecker:

    def __init__(self, file_path: str, file_name: str):
        self.file = file_name
        self.file_path = file_path

    @staticmethod
    def _check_image(image: str) -> bool:
        if ":" in image:
            image = image.split(":")
            if len(image) != 2:
                return False
            if image[1].strip() != "":
                return False
            image = image[0]
        elif "@" in image:
            image = image.split("@")
            if len(image) != 2:
                return False
            if image[1].strip() != "":
                return False
            image = image[0]
        return image.strip() != ""

    @staticmethod
    def _check_platform(platform: str) -> bool:
        if "--platform=" in platform:
            platform = platform.split("=")
            if len(platform) != 2:
                return False
            return platform[1] != ""
        return False

    @staticmethod
    def _check_add(value: str) -> bool:
        if value == "--link":
            return True
        if "--chown" in value:
            if "=" in value:
                split_value = value.split("=")
                if len(split_value) == 2 and ":" in split_value[1]:
                    chown = split_value[1].split(":")
                    if len(chown) == 2 and chown[0].strip() != "" and chown[1].strip() != "":
                        return True
                return split_value[1].strip() != ""
            return False
        elif "--chmod" in value:
            if "=" in value:
                split_value = value.split("=")
                return split_value[1].strip() != ""
            return False
        elif value.startswith("--") or value.startswith("-"):
            return False

        # todo check ci dana cesta exsituje
        return value.strip() != ""

    @staticmethod
    def _runnable(CMD: str) -> bool:
        # try:
        #     _ = subprocess.check_output(CMD, shell=True)
        # except:
        #     return False
        #todo asi nie runnut , moze nastat problem ak by cmd vymazaval subory napriklad
        return True

    def _check_command(self, CMD: str, command: str) -> bool:
        if CMD.strip() == "CMD":
            if self._runnable(command):
                if command.strip() != "":
                    return True
        return False

    # TODO
    def _check_cache(self, val: list) -> bool:
        was_required = False
        for option in val:
            if "=" not in option:
                return False
            option = option.split("=")
            op = option[0].strip()
            value = option[1].strip()
            if op in ["target", "id", "from", "source"]:
                if op == "target":
                    was_required = True
                if value == "":
                    return False
            elif op in ["mode", "uid", "gid"]:
                if not value.isnumeric():
                    return False
            elif op in ["ro", "readonly"]:
                if value != "":
                    return False
            elif op == "sharing":
                if value not in ["shared", "private","locked"]:
                    return False
        if not was_required:
            return False
        return True

    def _check_bind(self, val: list) -> bool:
        was_required = False
        for option in val:
            if "=" not in option:
                return False
            option = option.split("=")
            op = option[0].strip()
            value = option[1].strip()
            if op in ["target", "source", "from"]:
                if op == "target":
                    was_required = True
                if value == "":
                    return False
            elif op in ["rw", "readwrite"]:
                if value != "":
                    return False
        if not was_required:
            return False
        return True

    def _check_tmpfs(self, val: list) -> bool:
        was_required = False
        for option in val:
            if "=" not in option:
                return False
            option = option.split("=")
            op = option[0].strip()
            value = option[1].strip()
            if op == "target":
                was_required = True
                if value == "":
                    return False
            elif op == "size":
                if not value.isnumeric():
                    return False
        if not was_required:
            return False
        return True

    def _check_ssh_secret(self, val: list) -> bool:
        for option in val:
            if "=" not in option:
                return False
            option = option.split("=")
            op = option[0].strip()
            value = option[1].strip()
            if op in ["target", "id"]:
                if value == "":
                    return False
            elif op in ["required"]:
                if value not in ["true", "false"]:
                    return False
            elif op in ["mode", "uid", "gid"]:
                if not value.isnumeric():
                    return False
        return True

    def _check_run_with_mount(self, value: str) -> bool:
        value = value.split("--mount=")
        cmd = None
        if " " in value[-1]:
            cmd = value[-1][value[-1].index(" ") + 1:]
            value[-1] = value[-1][:value[-1].index(" ")]
        for i in range(len(value)):
            val = value[i].strip()
            if "," in val:
                val = val.split(",")
            else:
                val = list(val)
            if "type" in val[0]:
                type = val[0][val[0].index("=") + 1:]
            else:
                return False
            if type == "cache":
                if not self._check_cache(val):
                    return False
            elif type == "bind":
                if not self._check_bind(val):
                    return False
            elif type == "tmpfs":
                if not self._check_tmpfs(val):
                    return False
            elif type == "ssh":
                if not self._check_ssh_secret(val):
                    return False
            elif type == "secret":
                if not self._check_ssh_secret(val):
                    return False
        if not self._runnable(cmd):
            return False
        return True

    def _check_run_with_security(self, value: str) -> bool:
        cmd = None
        if " " in value:
            cmd = value[value.index(" ") + 1:].strip()
            value = value[:value.index(" ") + 1].strip()
        if value in ["insecure", "sandbox"]:
            if cmd != "" and self._runnable(cmd):
                return True
        return False

    def _check_run_with_network(self, value: str) -> bool:
        cmd = None
        if " " in value:
            cmd = value[value.index(" ") + 1:].strip()
            value = value[:value.index(" ") + 1].strip()
        value = value.strip()
        if value in ["default", "none"] or value != "":
            if cmd != "" and self._runnable(cmd):
                return True
        return False

    def _check_instruction(self, instruction: str, line: int, value: str) -> str:
        """
        """
        value = value.strip()
        if instruction == "COMMENT":
            return ""
        if value == "":
            return f" instruction {instruction} at line {line} missing value"

        if instruction == "FROM":
            value = value.split(" ")
            if len(value) == 1:
                if self._check_image(value[0]):
                    return ""
            elif len(value) == 2:
                if self._check_image(value[1]) and self._check_platform(value[0]):
                    return ""
            elif len(value) == 3:
                if value[1].strip() == "AS":
                    if self._check_image(value[0]):
                        return ""
            elif len(value) == 4:
                if value[2].strip() == "AS":
                    if self._check_image(value[0]) and self._check_platform(value[1]):
                        return ""
        elif instruction == "COPY":
            if value.startswith("--parents"):
                value = value[value.index(" "):]
            return self._check_instruction("ADD", line, value)
        elif instruction == "RUN":
            if value.startswith("/bin/bash -c"):
                if self._runnable(value.removeprefix('/bin/bash  -c')):
                    return ""
            if value.startswith("cmd /S /C"):
                if self._runnable(value.removeprefix('/bin/bash  -c')):
                    return ""
            elif value.startswith("--") or value.startswith("-"):
                # start security
                if value.startswith("--security=") and self._check_run_with_security(value.removeprefix("--security=")):
                    return ""
                # start network
                if value.startswith("--network=") and self._check_run_with_network(value.removeprefix("--network=")):
                    return ""
                # start mount
                if value.startswith("--mount=") and self._check_run_with_mount(value.removeprefix("--mount=")):
                    return ""
            elif value.startswith("[") and value.endswith("]"):
                value = value[1:-1]
                value = value.replace('"', "").replace(",", " ")
                if value.startswith("/bin/bash"):
                    value = value.removeprefix('/bin/bash  -c')
                    if self._runnable(value):
                        return ""
                if value.startswith("cmd /S /C"):
                    if self._runnable(value.removeprefix('/bin/bash  -c')):
                        return ""
        elif instruction == "CMD":
            if value.startswith("["):
                if value.endswith("]"):
                    cmd = value[1:-1]
                    if "'" not in cmd:
                        if self._runnable(cmd):
                            return ""
            elif self._runnable(value):
                return ""
        elif instruction == "LABEL":
            if "=" in value:
                value = value.split("=")
                for i in range(0, len(value) - 1, 2):
                    key = value[i].strip()
                    val = value[i + 1].strip()
                    if key != "" and val != "":
                        return ""
        elif instruction == "MAINTAINER":
            return ""
        elif instruction == "EXPOSE":
            if "/" in value:
                value = value.split("/")
                if value[0].isnumeric():
                    if value[1] in ["udp", "tcp", "ftp", "http"]:
                        return ""
            elif value.isnumeric():
                return ""
        elif instruction == "ENV":
            value = value.split("=")
            if len(value) == 2:
                if value[0].strip() != "" and value[1].strip() != "":
                    return ""
        elif instruction == "ADD":
            values = value.split(" ")
            error = False
            for val in values:
                if not self._check_add(val):
                    error = True
            if not error:
                if len(values) >= 2:
                    if "--chmod" not in values[-1] and "--chown" not in values[-1] and "--link" not in values[-1]:
                        if "--chmod" not in values[-2] and "--chown" not in values[-2] and "--link" not in values[-2]:
                            return ""

        elif instruction == "ENTRYPOINT":
            if "[" in value:
                value = value[1:-1].split(",")
                cmd = ""
                for i in range(len(value)):
                    if "'" in value[i]:
                        cmd = None
                        break
                    cmd += value[i]
            else:
                cmd = value.strip()
            if self._runnable(cmd):
                return ""

        elif instruction == "WORKDIR":
            if "'" not in value and '"' not in value:
                return ""
        elif instruction == "VOLUME":
            if "'" not in value and '"' not in value:
                return ""
        elif instruction == "USER":
            if ":" in value:
                value = value.split(":")
                if value[0].strip() != "" and value[1].strip() != "":
                    return ""
            elif value != "" and "'" not in value and '"' not in value:
                return ""
        elif instruction == "ARG":
            if "=" in value:
                value = value.split("=")
                if value[0].strip() != "" and value[1].strip() != "":
                    return ""
            else:
                return ""
        elif instruction == "ONBUILD":
            new_instruction = value[:value.index(" ")].strip()
            new_value = value[value.index(" ") + 1:].strip()
            return self._check_instruction(new_instruction, line, new_value)
        elif instruction == "STOPSIGNAL":
            return ""
        elif instruction == "HEALTHCHECK":
            if value == "NONE":
                return ""
            value = value.split(" ")
            options = ["--interval", "--timeout", "--start-period", "--start-interval", "--retries"]
            for i in range(len(value)):
                val = value[i].strip()
                if "=" in val:
                    val = val.split("=")
                    if val[0].strip() in options:
                        if val[0] == "--retries":
                            if not val[1].isnumeric():
                                break
                        else:
                            if not val[1][:-1].isnumeric():
                                break
                elif val.strip() == "":
                    continue
                else:
                    if "CMD" in val:
                        new_val = " ".join(value[i + 1:])
                        return self._check_instruction("CMD", line, new_val)
                    break

        elif instruction == "SHELL":
            if value.startswith("[") and value.endswith("]"):
                value = value[1:-1].split(",")
                cmd = ""
                for i in range(len(value)):
                    cmd += value[i]
                if self._runnable(cmd):
                    return ""

        else:
            return f"wrong instruction at line {line}."
        error = f"instruction {instruction} in line {line} has error"
        return error

    def _parse_structure(self, structure: str) -> list:
        """

        """
        errors = []
        for line in structure:
            instruction = line["instruction"]
            line_num = int(line["startline"]) + 1
            value = line["value"]

            error = self._check_instruction(instruction, line_num, value)
            if error != "":
                errors.append(error)
        return errors

    def check(self) -> list:
        with open(self.file, "r") as file:
            lines = file.readlines()
            lines += "\n"
            file.close()
        with open(self.file, "w") as file:
            file.writelines(lines)
            file.close()
        dfp = DockerfileParser(self.file_path)
        structure = dfp.structure
        errors = []
        errors += self._parse_structure(structure)
        print("\n".join(errors))
        return errors
