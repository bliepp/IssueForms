from configparser import ConfigParser, SectionProxy
from typing import Tuple

config = ConfigParser()
config.read("config.ini")

def get_prefixed_sections(prefix: str) -> Tuple[str, SectionProxy]:
    for section in config:
        if section.startswith(f"{prefix}:"):
            key = section.replace(f"{prefix}:", "")
            yield key, config[section]


form_sections = dict(get_prefixed_sections("form"))
