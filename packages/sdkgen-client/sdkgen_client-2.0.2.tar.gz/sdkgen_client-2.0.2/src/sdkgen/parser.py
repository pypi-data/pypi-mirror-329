import string
import datetime


class Parser:
    base_url: str = None

    def __init__(self, base_url: str):
        self.base_url = self.normalize_url(base_url)

    def url(self, path: str, parameters: dict[str, any]) -> str:
        return self.base_url + "/" + self.substitute_parameters(path, parameters)

    @classmethod
    def substitute_parameters(cls, path: str, parameters: dict[str, any]) -> str:
        parts = path.split("/")
        result = []

        for part in parts:
            if part is None or part == "":
                continue

            name = ""
            if part.startswith(":"):
                name = part[1:]
            elif part.startswith("$"):
                try:
                    pos = part.index("<")
                    name = part[1:pos]
                except ValueError:
                    name = part[1:]
            elif part.startswith("{") and part.endswith("}"):
                name = part[1:len(part) - 1]

            if name in parameters:
                part = cls.to_string(parameters[name])

            result.append(part)

        return "/".join(result)

    @classmethod
    def query(cls, parameters: dict[str, any], struct_names: list[str] = None) -> dict[str, any]:
        result: dict[str, any] = {}
        for name, value in parameters.items():
            if value is None:
                continue

            if struct_names and name in struct_names:
                result = result | cls.query(value.model_dump())
            else:
                result[name] = cls.to_string(value)

        return result

    @classmethod
    def to_string(cls, value: any) -> string:
        t = type(value)
        if t is int:
            return str(value)
        elif t is float:
            return str(value)
        elif t is bool:
            return "1" if value else "0"
        elif t is str:
            return str(value)
        elif t is datetime.date:
            return value.isoformat()
        elif t is datetime.datetime:
            return value.isoformat() + "Z"
        elif t is datetime.time:
            return value.isoformat()
        else:
            return ""

    @classmethod
    def normalize_url(cls, value: string) -> string:
        if value.endswith("/"):
            value = value[0:len(value) - 1]
        return value
