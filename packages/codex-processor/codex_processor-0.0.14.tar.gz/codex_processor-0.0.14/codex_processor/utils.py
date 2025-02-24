from typing import NamedTuple
import functools
import json
import os
import shutil
import sys

import toml
import yaml
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt

_open = functools.partial(open, encoding="utf8")


def load_config(filepath):
    if not filepath:
        return {}
    assert filepath.endswith((".json", ".toml", ".yaml"))
    with _open(filepath, "r") as f:
        cnt = f.read()
    if filepath.endswith(".json"):
        return json.loads(cnt)
    elif filepath.endswith(".yaml"):
        return yaml.load(cnt)
    elif filepath.endswith(".toml"):
        return toml.loads(cnt)


def get_codex_processor_dir():
    path = os.path.join(os.path.expanduser("~"), ".codex_processor")
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_resource_dir():
    sourcedir = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
    resourcedir = os.path.join(sourcedir, "resources")
    return resourcedir


class FontFinder:
    def __init__(self, root_dir=None):
        self.fonts = {
            "texgyrepagella-math.otf": None,
            "SourceCodePro-Bold.otf": None,
            "SourceCodePro-BoldIt.otf": None,
            "SourceCodePro-It.otf": None,
            "SourceCodePro-Regular.otf": None,
            "SourceSerif4-Bold.otf": None,
            "SourceSerif4-BoldIt.otf": None,
            "SourceSerif4-It.otf": None,
            "SourceSerif4-Regular.otf": None,
        }
        if not root_dir:
            root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for dir_, _, files in os.walk(root_dir):
            for fn in files:
                if fn in self.fonts and not self.fonts[fn]:
                    self.fonts[fn] = os.path.join(dir_, fn)
        self.not_found = {fn for fn in self.fonts if not self.fonts[fn]}
        if self.not_found:
            sys.stderr.write(
                f"following fonts were not found: {', '.join(sorted(self.not_found))}\n"
            )


def read_front_matter(cnt):
    lines = cnt.split("\n")
    front_matter_end = None
    if lines[0].strip() == "---":
        for i, line in enumerate(lines[1:]):
            if line.strip() == "---":
                front_matter_end = i + 1
                break
    if front_matter_end:
        front_matter = "\n".join(lines[1:front_matter_end])
        cnt = "\n".join(lines[front_matter_end + 1 :])
        try:
            parsed_front_matter = yaml.safe_load(front_matter)
            return parsed_front_matter, cnt
        except Exception as e:
            sys.stderr.write(
                f"exception while trying to parse front matter: {type(e)} {e}\n"
            )
            return {}, cnt

    else:
        return {}, cnt


def dump_front_matter(front_matter):
    return (
        "---\n"
        + yaml.safe_dump(front_matter, allow_unicode=True, sort_keys=False)
        + "\n---\n"
    )


def parse_json(obj):
    if obj:
        return json.loads(obj)
    else:
        return


def copy_file(*args, **kwargs):
    try:
        shutil.copy(*args, **kwargs)
    except shutil.SameFileError:
        pass


class Heading(NamedTuple):
    level: int
    span_id: str
    text: str


def parse_headings(cnt):
    md = MarkdownIt("commonmark")
    tokens = md.parse(cnt)
    result = []
    prev_token = None
    for token in tokens:
        if prev_token and prev_token.type == "heading_open" and token.type == "inline":
            text = ""
            span_id = None
            for child in token.children:
                if child.type == "text":
                    text += child.content
                elif child.type == "html_inline" and "span" in child.content:
                    parsed = BeautifulSoup(child.content, "html.parser")
                    span = parsed.find("span")
                    if span and not span_id:
                        span_id = span.attrs.get("id")
            if text and span_id:
                result.append(
                    Heading(level=int(prev_token.tag[1]), span_id=span_id, text=text)
                )
        prev_token = token
    return result
