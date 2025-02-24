import os
import random
import re
import shutil
import subprocess
import sys
import tempfile

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt

from codex_processor.utils import (
    _open,
    copy_file,
    dump_front_matter,
    get_resource_dir,
    load_config,
    parse_headings,
    read_front_matter,
)

WATER_HEADER = """\
<!DOCTYPE html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1" />
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/light.css">
<style>blockquote {font-style: normal;}</style>
</head>
<body>
"""


def wrap_bytes(s):
    if isinstance(s, bytes):
        return s.decode("utf8", errors="replace")
    return s


class Converter:
    re_caps = re.compile("(\\b)([А-ЯЁA-Z]{2,})(\\b)", flags=re.UNICODE)
    re_list_item = re.compile("^(?P<spaces>\\s*)(?P<list_mark>\\- )")
    extension_dict = {"latex": ".pdf", "latex_raw": ".pdf"}
    TOC_MARKER = "<!-- toc -->"
    RE_SUBSECTION = re.compile(
        "^\\\\(sub)*section\\[(?P<heading>.+?)\\]\\{(?P<content>.+)\\}$"
    )
    RE_HYPERTARGET = re.compile("\\\\hypertarget\\{(?P<number>.+?)\\}")

    def __init__(
        self,
        dirname=None,
        latex_bin="lualatex",
        font_finder=None,
        timeout=20,
        pandoc_path=None,
    ):
        self.dirname = dirname
        self.latex_bin = latex_bin
        self.pandoc_path = pandoc_path
        self.tmpd = tempfile.TemporaryDirectory()
        self.font_finder = font_finder
        self.timeout = timeout
        if dirname:
            for fn in os.listdir(dirname):
                full_path = os.path.join(dirname, fn)
                if os.path.isfile(full_path):
                    copy_file(full_path, os.path.join(self.tmpd.name, fn))

    @classmethod
    def wrap_latex_letterspace(cls, cnt_):
        already_matched = set()
        replacements = []
        index_ = cnt_.index("\\title")
        cnt = cnt_[index_:]
        for srch in cls.re_caps.finditer(cnt):
            grp = srch.group(0)
            pre = srch.group(1)
            caps = srch.group(2)
            post = srch.group(3)
            if grp in already_matched:
                continue
            already_matched.add(grp)
            replacements.append((grp, pre + "\\lspace{" + caps + "}" + post))
        for from_, to_ in replacements:
            cnt = cnt.replace(from_, to_)
        return cnt_[:index_] + cnt

    @classmethod
    def mark_items(cls, md_path):
        with _open(md_path, "r") as f:
            mdcontent = f.read()
        lines = mdcontent.split("\n")
        for i, line in enumerate(lines):
            srch = cls.re_list_item.search(line)
            if not srch:
                continue
            len_ = len(srch.group(0))
            lines[i] = line[:len_] + "ITEMSTART" + line[len_:] + "ITEMEND"
        with _open(md_path, "w") as f:
            f.write("\n".join(lines))

    def wrap_subprocess(self, args, cwd=None):
        proc = subprocess.run(
            args, check=False, capture_output=True, timeout=self.timeout, cwd=cwd
        )
        if proc.returncode:
            sys.stderr.write(
                f"process {args} finished with code {proc.returncode}: "
                f"stderr {wrap_bytes(proc.stderr)}, stdout {wrap_bytes(proc.stdout)}\n"
            )
            sys.exit(1)

    def fix_fonts(self, cnt, tmpd):
        for font_file in self.font_finder.fonts:
            path = self.font_finder.fonts[font_file]
            shutil.copy(path, tmpd)
        cnt = cnt.replace(
            r"\setmainfont[]{Source Serif 4}",
            r"""\setmainfont[
    BoldFont       = SourceSerif4-Bold.otf ,
    ItalicFont     = SourceSerif4-It.otf ,
    BoldItalicFont = SourceSerif4-BoldIt.otf
  ]{SourceSerif4-Regular.otf}""",
        )
        cnt = cnt.replace(
            r"\setmonofont[]{Source Code Pro}",
            r"""
            \setmonofont[
    BoldFont       = SourceCodePro-Bold.otf ,
    ItalicFont     = SourceCodePro-It.otf ,
    BoldItalicFont = SourceCodePro-BoldIt.otf
  ]{SourceCodePro-Regular.otf}
            """,
        )
        cnt = cnt.replace(
            r"\setmathfont[]{TeX Gyre Pagella Math}",
            r"""\setmathfont[]{texgyrepagella-math.otf}""",
        )
        return cnt

    def convert_file(
        self,
        *,
        source,
        target,
        output_format,
        sandbox=False,
        extra_args=None,
        source_format=None,
    ):
        args = [self.pandoc_path, source]
        with _open(source) as f:
            cnt = f.read()
        front_matter, _ = read_front_matter(cnt)
        source_format = (
            source_format or front_matter.get("source_format") or "markdown+mark"
        )
        if source_format:
            args.extend(["-f", source_format])
        args.extend(["-t", output_format, "-o", target])
        if not sandbox:
            args.extend(["--sandbox=false"])
        if extra_args:
            args.extend(extra_args)
        return subprocess.run(args, check=True, capture_output=True)

    @classmethod
    def fix_subsections(cls, cnt):
        lines = cnt.split("\n")
        for i, line in enumerate(lines):
            srch = cls.RE_SUBSECTION.search(line)
            srch2 = cls.RE_HYPERTARGET.search(line)
            if srch and srch2:
                lines[i] = srch.group(0) + """\\label{LABEL}{}""".replace(
                    "LABEL", srch2.group("number")
                )
        return "\n".join(lines)

    def latex_lfix_process(self, *, bn, dirname, source, target, extra_args, toc=False):
        tmpd = self.tmpd.name
        md_path = os.path.join(tmpd, f"{bn}.md")
        self.mark_items(md_path)
        new_filepath_tex = os.path.join(tmpd, f"{bn}.tex")
        new_filepath_pdf = os.path.join(tmpd, f"{bn}.pdf")
        _target = new_filepath_tex
        self.convert_file(
            source=source, output_format="latex", target=_target, extra_args=extra_args
        )
        with _open(new_filepath_tex) as f:
            cnt = f.read()
        cnt = cnt.replace(
            "ITEMSTART", "\\parbox[t]{\\linewidth}{\\strut \\raggedright "
        ).replace("ITEMEND", " \\strut}")
        cnt = self.wrap_latex_letterspace(cnt)
        cnt = self.fix_fonts(cnt, tmpd)
        cnt = self.fix_subsections(cnt)
        with _open(new_filepath_tex, "w") as f:
            f.write(cnt)
        if self.save_raw_tex:
            raw_tex_target = os.path.abspath(
                os.path.join(dirname, os.path.basename(tmpd))
            )
            shutil.copytree(tmpd, raw_tex_target)
            print(f"copied raw tex dir to {raw_tex_target}")
        print("we are in lfix mode")
        self.wrap_subprocess([self.latex_bin, new_filepath_tex], cwd=tmpd)
        if toc and "tectonic" not in self.latex_bin:
            self.wrap_subprocess([self.latex_bin, new_filepath_tex], cwd=tmpd)
        shutil.move(new_filepath_pdf, target)

    @classmethod
    def replace_extension(cls, filename, new_ext):
        bn, _ = os.path.splitext(filename)
        return bn + new_ext

    @classmethod
    def get_extension(cls, output_format):
        return cls.extension_dict.get(output_format) or f".{output_format}"

    @classmethod
    def gen_toc(cls, cnt):
        fm, inner_cnt = read_front_matter(cnt)
        headings = parse_headings(inner_cnt)
        toc = []
        min_level = min(h.level for h in headings)
        max_level = fm.get("toc_max_level") or 99
        for heading in headings:
            level = heading.level - min_level + 1
            if level > max_level:
                continue
            prefix = "    " * (level - 1)
            node = f"- [{heading.text}](#{heading.span_id})"
            toc.append(prefix + node)
        toc = "\n".join(toc)
        rendered = MarkdownIt("commonmark").render(toc)
        return '<div class="toc">' + rendered + "</div>"

    def process_file(
        self,
        src,
        output_format=None,
        source_from_string=False,
        target_filepath=None,
        template_file=None,
        pandoc_extra_args=None,
        latex_vargs=None,
        toc=False,
        add_pdf=False,
        latex_fix=True,
        save_raw_tex=False,
        config_path=None,
    ):
        self.output_format = output_format
        self.source_from_string = source_from_string
        self.target_filepath = target_filepath
        self.template_file = template_file
        self.pandoc_extra_args = pandoc_extra_args
        self.latex_vargs = latex_vargs
        self.toc = toc
        self.add_pdf = add_pdf
        self.latex_fix = latex_fix
        self.save_raw_tex = save_raw_tex
        self.config_path = config_path
        if self.output_format == "latex_raw":
            self.save_raw_tex = True
            self.output_format = "latex"
        tmpd = self.tmpd.name
        if self.source_from_string:
            assert self.target_filepath is not None
            basename = self.replace_extension(
                os.path.basename(self.target_filepath), ".md"
            )
            filepath = os.path.join(tmpd, basename)
            with _open(filepath, "w") as f:
                f.write(src)
            dirname = os.path.dirname(self.target_filepath)
        else:
            assert os.path.isfile(src)
            basename = os.path.basename(src)
            dirname = os.path.dirname(src)
            if not self.target_filepath:
                raise Exception("target_filepath not defined")
        with _open(filepath, "r") as f:
            cnt = f.read()
        front_matter, _ = read_front_matter(cnt)
        if self.pandoc_extra_args is None:
            self.pandoc_extra_args = []
        if self.latex_vargs is None:
            self.latex_vargs = []
        if self.output_format == "auto":
            if front_matter and "cpr_format" in front_matter:
                self.output_format = front_matter["cpr_format"]
            elif "pdf" in target_filepath.split("_"):
                self.output_format = "latex"
            else:
                self.output_format = "docx"
        if (
            self.output_format == "latex"
            and self.template_file is None
            and self.config_path is None
        ):
            self.config_path = os.path.join(get_resource_dir(), "latex_source.json")
        if self.config_path:
            self.config = load_config(self.config_path)
            for k, v in self.config.items():
                setattr(self, k, v)
        else:
            self.config = None
        if self.output_format == "latex" and self.template_file is None:
            self.template_file = os.path.join(get_resource_dir(), "template.tex")
        if self.output_format == "docx" and self.template_file is None:
            self.template_file = os.path.join(get_resource_dir(), "template.docx")
        extension = self.get_extension(self.output_format)

        source = filepath
        output_format = self.output_format
        extra_args = self.pandoc_extra_args or []
        extra_args.extend(["--resource-path", self.tmpd.name])
        extra_args.extend(["--wrap=none"])
        do_toc = (
            toc
            or (front_matter and front_matter.get("toc"))
            or "toc" in target_filepath.split("_")
        )
        if do_toc and "--toc" not in extra_args:
            extra_args.extend(["--toc", "--toc-depth=2"])
        if self.output_format == "docx":
            extra_args.extend(["--reference-doc", self.template_file])
        elif self.output_format == "html":
            extra_args.extend(["--standalone", "--mathjax"])
        elif self.output_format == "latex":
            extra_args.extend(
                ["--pdf-engine", "lualatex", "--template", self.template_file]
            )
            for arg in self.latex_vargs or []:
                extra_args.append("-V")
                extra_args.append(arg)
        orig_bn, _ = os.path.splitext(basename)
        bn = orig_bn
        if bn.endswith(".src"):
            bn = bn[: -len(".src")]
        if self.output_format in ("md", "markdown", "html_md"):
            extension = ".md"
            if bn == orig_bn:
                bn += ".out"
        if self.output_format == "html_water":
            extension = ".html"
        new_filepath_2 = os.path.join(dirname, f"{bn}{extension}")
        if do_toc and not output_format.startswith("latex"):
            with _open(source) as f:
                cnt = f.read()
            if self.TOC_MARKER in cnt:
                bn, ext = os.path.splitext(source)
                source2_name = bn + f".tmp{random.randint(1000, 5000)}" + ext
                cnt = cnt.replace(self.TOC_MARKER, self.gen_toc(cnt))
                with _open(source2_name, "w") as f:
                    f.write(cnt)
                source = source2_name
        if self.output_format == "latex" and latex_fix:
            self.latex_lfix_process(
                bn=bn,
                dirname=dirname,
                source=source,
                target=new_filepath_2,
                extra_args=extra_args,
                toc=do_toc,
            )
        elif self.output_format == "html_md":
            html_file = os.path.join(self.tmpd.name, bn + ".html")
            self.convert_file(
                source=source,
                output_format="html",
                target=html_file,
                extra_args=extra_args + ["--mathml"],
            )
            with _open(html_file) as f:
                soup = BeautifulSoup(f.read(), "html.parser")
            body = soup.find("body")
            if body:
                body = soup.body.unwrap()
            else:
                body = soup
            result = ""
            if front_matter:
                result += dump_front_matter(front_matter)
            result += str(body)
            with _open(new_filepath_2, "w") as f:
                f.write(result)
        elif self.output_format == "html_water":
            html_file = os.path.join(self.tmpd.name, bn + ".html")
            self.convert_file(
                source=source,
                output_format="html",
                target=html_file,
                extra_args=extra_args + ["--mathml"],
            )
            with _open(html_file) as f:
                cnt = f.read()
            cnt = WATER_HEADER + cnt + "</body></html>"
            with _open(new_filepath_2, "w") as f:
                f.write(cnt)
        elif self.output_format in ("md", "markdown"):
            if bn == orig_bn:
                bn += ".out"
            shutil.copy(source, new_filepath_2)
        else:
            self.convert_file(
                source=source,
                output_format=output_format,
                target=new_filepath_2,
                sandbox=False,
                extra_args=extra_args,
            )

        print(f"output file: {new_filepath_2}")
        if self.output_format == "docx" and self.add_pdf:
            self.wrap_subprocess(
                ["soffice", "--headless", "--convert-to", "pdf", new_filepath_2]
            )

    def cleanup(self):
        self.tmpd.cleanup()

    def __del__(self):
        self.cleanup()
