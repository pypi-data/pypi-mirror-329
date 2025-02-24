import re
import sys
from collections import Counter, defaultdict
import os

from codex_processor.typograph import typograph
from codex_processor.utils import _open


class CodexProcessor:
    _refname_base = "(?P<refname>[a-zA-Z0-9_]"
    _refname_mandatory = _refname_base + "+)"
    _refname_optional = _refname_base + "*)"
    _ext_filename = "(?P<ext_filename>[a-zA-Z0-9_]+)"
    _footnote = "\\[\\^(?P<fnref>.+?)\\]"
    re_section = re.compile("(?P<section>§+)" + _refname_optional)
    re_reference = re.compile("(?P<prev_char>.)\\^\\^" + _refname_mandatory)
    re_ext_reference = re.compile(
        "(?P<prev_char>.)\\^\\^\\(" + _ext_filename + "\\)" + _refname_mandatory
    )
    re_short_reference = re.compile("<\\^\\^" + _refname_mandatory + ">")
    re_footnote_ref = re.compile(_footnote)
    re_footnote_expl = re.compile(
        "\n" + _footnote + ": (?P<fncontent>.+?)\n", flags=re.MULTILINE
    )
    re_include = re.compile('<include src="(?P<filepath>.+?)">')
    reset_counter = "RESETCOUNTER"
    TOC_MARKER = "<!-- toc -->"

    def __init__(
        self,
        source,
        target=None,
        remake_footnotes=False,
        resolve_external_links=False,
        skip_output=False,
        source_from_string=False,
        typograph=True,
    ):
        self.source = source
        self.target = target
        self.remake_footnotes = remake_footnotes
        self.resolve_external_links = resolve_external_links
        self.skip_output = skip_output
        self.source_from_string = source_from_string
        self.typograph = typograph
        self.section_counter = Counter()
        self.ref_to_section = {}
        self.toc = []
        self.counter_has_been_reset = False

    @classmethod
    def generate_anchor(cls, anchor_name):
        return f'<span id="{anchor_name}"></span>'

    def add_section(self, srch):
        level = len(srch.group("section"))
        refname = srch.group("refname")
        if self.reset_counter in refname:
            refname = refname.replace(self.reset_counter, "")
            self.counter_has_been_reset = True
            self.section_counter = Counter()
        self.section_counter[level] += 1
        for level_ in self.section_counter:
            if level_ > level:
                self.section_counter[level_] = 0
        name = "\\.".join(str(self.section_counter[i]) for i in range(1, level + 1))
        anchor_name = name.replace("\\", "")
        anchor = self.generate_anchor(anchor_name)
        if refname and not self.counter_has_been_reset:
            self.ref_to_section[refname] = {"anchor": anchor_name, "name": name}
        self.cnt = self.replace_span(srch, name + "\\." + anchor, self.cnt)

    def resolve_ref(self, srch, return_replacement=False):
        refname = srch.group("refname")
        prev_char = srch.group("prev_char")
        try:
            replacement = (
                prev_char
                + self.ref_to_section[refname]["anchor" if prev_char == "#" else "name"]
            )
            self.ref_to_section[refname]["referenced"] = True
        except KeyError:
            replacement = f"UNRESOLVED_REFERENCE({refname})"
            sys.stderr.write(f"couldn't resolve reference '{refname}'\n")
        if return_replacement:
            return replacement
        self.cnt = self.replace_span(srch, replacement, self.cnt)

    @classmethod
    def replace_span(cls, match, replacement, cnt):
        span = match.span()
        cnt = cnt[: span[0]] + replacement + cnt[span[1] :]
        return cnt

    def _remake_footnotes(self):
        ref_to_expl = {}
        ref_to_num = {}
        srch = self.re_footnote_expl.search(self.cnt)
        while srch:
            ref_to_expl[srch.group("fnref")] = srch.group("fncontent")
            self.cnt = self.cnt.replace(srch.group(0), "")
            srch = self.re_footnote_expl.search(self.cnt)
        srch = self.re_footnote_ref.search(self.cnt)
        fncounter = 1
        refcounter = defaultdict(lambda: -1)
        while srch:
            ref = srch.group("fnref")
            if ref not in ref_to_num:
                ref_to_num[ref] = fncounter
                fncounter += 1
            refcounter[ref] += 1
            num = ref_to_num[ref]
            replacement = f'<span id="xfnref{num}-{refcounter[ref]}"></span>^[[{num}]](#xfn{num})^'
            self.cnt = self.replace_span(srch, replacement, self.cnt)
            srch = self.re_footnote_ref.search(self.cnt)
        if not ref_to_expl:
            return
        addition = ["\n", "---", ""]
        for ref in sorted(ref_to_expl, key=lambda k: ref_to_num[k]):
            num = ref_to_num[ref]
            refc = refcounter[ref]
            if refc > 0:
                ord_ = ord("a")
                lst = []
                for i in range(refc + 1):
                    lst.append(f"^[{chr(ord_)}](#xfnref{num}-{i})^")
                    ord_ += 1
                additional_refs = " ".join(lst) + " "
            else:
                additional_refs = " "
            expl = ref_to_expl[ref]
            addition.append(
                f'{num}\\. [\\^](#xfnref{num}-0) {additional_refs}<span id="xfn{num}"></span> {expl}'
            )
        self.cnt += "\n\n".join(addition)

    def _resolve_external_links(self):
        ext_processors = {}
        bad_fns = set()
        srch = self.re_ext_reference.search(self.cnt)
        while srch:
            ext_fn = srch.group("ext_filename") + ".md"
            if ext_fn not in ext_processors and ext_fn not in bad_fns:
                try:
                    ext_processors[ext_fn] = CodexProcessor(
                        source=ext_fn,
                        skip_output=True,
                        resolve_external_links=False,
                    )
                    ext_processors[ext_fn].process()
                except Exception as e:
                    sys.stderr.write(
                        f"couldn't process {ext_fn} during processing {self.source}: {type(e)} {e}\n"
                    )
                    ext_processors.pop(ext_fn, None)
                    bad_fns.add(ext_fn)
            replacement = None
            if ext_fn in ext_processors:
                try:
                    replacement = ext_processors[ext_fn].resolve_ref(
                        srch, return_replacement=True
                    )
                except Exception as e:
                    sys.stderr.write(
                        f"couldn't resolve {srch.group(0)} during processing {self.source}: {type(e)} {e}\n"
                    )
            if not replacement:
                replacement = f"UNRESOLVED_EXTERNAL_REFERENCE({srch.group('ext_filename')/srch.group('refname')}"
            self.cnt = self.replace_span(srch, replacement, self.cnt)
            srch = self.re_ext_reference.search(self.cnt)

    def process(self):
        if self.source_from_string:
            self.cnt = self.source
        else:
            with _open(self.source, "r") as f:
                self.cnt = f.read()

        srch = self.re_include.search(self.cnt)
        while srch:
            filepath = srch.group("filepath")
            with _open(filepath, "r") as f:
                replacement = f.read()
            self.cnt = self.replace_span(srch, replacement, self.cnt)
            srch = self.re_include.search(self.cnt)

        srch = self.re_section.search(self.cnt)
        while srch:
            self.add_section(srch)
            srch = self.re_section.search(self.cnt)

        srch = self.re_short_reference.search(self.cnt)
        while srch:
            rn = srch.group("refname")
            replacement = f"[^^{rn}](#^^{rn})"
            self.cnt = self.replace_span(srch, replacement, self.cnt)
            srch = self.re_short_reference.search(self.cnt)

        srch = self.re_reference.search(self.cnt)
        while srch:
            self.resolve_ref(srch)
            srch = self.re_reference.search(self.cnt)

        if self.resolve_external_links:
            self._resolve_external_links()

        if self.resolve_external_links:
            unreferenced = sorted(
                [
                    f"{refname} ({self.ref_to_section[refname]['name']})"
                    for refname in self.ref_to_section
                    if not self.ref_to_section[refname].get("referenced")
                ]
            )
            if unreferenced:
                sys.stderr.write(
                    f"warning: unreferenced names: {', '.join(unreferenced)}\n"
                )

        if self.remake_footnotes:
            self._remake_footnotes()

        if self.typograph:
            self.cnt = typograph(self.cnt)

        if self.skip_output:
            return self.cnt
        if not self.target:
            bn, ext = os.path.splitext(self.source)
            self.target = bn + "_output" + ext
        with _open(self.target, "w") as f:
            f.write(self.cnt)
