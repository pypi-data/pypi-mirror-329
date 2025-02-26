import typing
from pathlib import Path

import yaml
from good_common.types import URL
# from yaml import dump, load

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader


#
# YAML Functions
#


def str_presenter(dumper, data):
    text_list = [line.rstrip() for line in data.splitlines()]
    fixed_data = "\n".join(text_list)
    if len(text_list) > 1:
        print(fixed_data)
        return dumper.represent_scalar("tag:yaml.org,2002:str", fixed_data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", fixed_data)


# def url_dumper(dumper, data):
#     data = str(data)
#     return dumper.represent_scalar("tag:yaml.org,2002:str", data)


# def set_dumper(dumper: Dumper, data):
#     return dumper.represent_list(sorted(list(data)))
#     # return dumper.represent_sequence("tag:yaml.org,2002:set", data, flow_style=True)


# def dict_dumper(dumper: Dumper, data):
#     def _to_dict(d):
#         if isinstance(d, dict):
#             return {k: _to_dict(v) for k, v in d.items()}
#         else:
#             return d

#     return dumper.represent_dict(_to_dict(data))


# Dumper.add_representer(str, str_presenter)
# Dumper.add_representer(set, set_dumper)
# Dumper.add_representer(URL, url_dumper)
# Dumper.add_representer(dict, dict_dumper)

# Dumper.ignore_aliases = lambda *args: True


def force_multiline_strings(data):
    """Recursively process data structure to identify multiline strings"""
    if isinstance(data, dict):
        return {k: force_multiline_strings(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [force_multiline_strings(item) for item in data]
    elif isinstance(data, str):
        lines = data.splitlines()
        if len(lines) > 1:
            # We'll use this class to mark strings that should use | style
            return PreservedScalarString("\n".join(line.rstrip() for line in lines))
        return data
    return data


class PreservedScalarString(str):
    """String class that will always be serialized with | style"""

    pass


class NestedStringDumper(Dumper):
    """Custom YAML Dumper that properly handles nested multi-line strings"""

    pass


def preserved_str_presenter(dumper, data):
    """String presenter for PreservedScalarString class"""
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")


def url_dumper(dumper, data):
    """URL type dumper"""
    data = str(data)
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


def set_dumper(dumper, data):
    """Set type dumper"""
    return dumper.represent_list(sorted(list(data)))


def dict_dumper(dumper, data):
    """Dict type dumper with recursive conversion"""

    def _to_dict(d):
        if isinstance(d, dict):
            return {k: _to_dict(v) for k, v in d.items()}
        else:
            return d

    return dumper.represent_dict(_to_dict(data))


# Register representers
NestedStringDumper.add_representer(PreservedScalarString, preserved_str_presenter)
NestedStringDumper.add_representer(set, set_dumper)
NestedStringDumper.add_representer(URL, url_dumper)
NestedStringDumper.add_representer(dict, dict_dumper)

# Ignore aliases
NestedStringDumper.ignore_aliases = lambda *args: True
yaml.representer.SafeRepresenter.add_representer(
    str, str_presenter
)  # to use with safe_dum


def yaml_load(path) -> typing.Any:
    with open(path, "r") as f:
        return yaml.load(f, Loader=Loader)


def yaml_dumps(data: typing.Any, sort_keys: bool = False, **kwargs) -> str:
    return yaml.dump(data, Dumper=NestedStringDumper, sort_keys=sort_keys, **kwargs)


def yaml_loads(data: str) -> typing.Any:
    return yaml.load(data, Loader=Loader)


def yaml_dump(path: str | Path, data: typing.Any, sort_keys=False, **kwargs) -> None:
    with open(path, "w") as f:
        return yaml.dump(
            data, f, Dumper=NestedStringDumper, sort_keys=sort_keys, **kwargs
        )
