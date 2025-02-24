import copy
import importlib
import os
import re
import sys
from collections import defaultdict

from codex_processor.utils import _open, load_config, read_front_matter


class TemplateProcessor:
    re_template = re.compile("{{(?P<template_content>.+?)}}")
    re_template_file = re.compile("(`|```)(?P<filename>.+?\\.(md|docx))(`|```)")
    re_variant_start = re.compile("<var:(?P<varname>[a-z0-9_]+)>")

    def __init__(
        self,
        dirname,
        ctx=None,
        ctx_file=None,
        ctx_builder_module_path=None,
        ctx_builder_args=None,
        ctx_builder_kwargs=None,
    ):
        self.dirname = dirname
        self.current_basename = None
        if ctx:
            self.ctx = copy.deepcopy(ctx)
        elif not ctx and ctx_file:
            self.load_ctx_from_file(ctx_file)
        elif not ctx and ctx_builder_module_path:
            spec = importlib.util.spec_from_file_location(
                "builder", ctx_builder_module_path
            )
            builder = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(builder)
            if not ctx_builder_args:
                ctx_builder_args = []
            if not ctx_builder_kwargs:
                ctx_builder_kwargs = {}
            ctx_builder = builder.ContextBuilder(
                *ctx_builder_args, **ctx_builder_kwargs
            )
            self.ctx = ctx_builder.build_context()
        else:
            self.ctx = {}
        self.unresolved_templates = defaultdict(lambda: defaultdict(set))
        self.templates_resolved_to_bad_values = defaultdict(set)
        self.missing_template_files = set()

    def load_ctx_from_file(self, filepath):
        self.ctx = load_config(filepath)

    def eval_templates(self, cnt):
        ctx = self.ctx
        srch = self.re_template.search(cnt)
        while srch:
            span = srch.span()
            tc = srch.group("template_content")
            try:
                value = eval(tc, None, ctx)
                if tc not in (ctx.get("can_be_poor") or set()) and not value:
                    self.templates_resolved_to_bad_values[tc].add(value)
                    value = f"POORLY_RESOLVED_TEMPLATE({tc})"
            except Exception as e:
                value = f"UNRESOLVED_TEMPLATE({tc})"
                self.unresolved_templates[tc][f"{type(e)} {e}"].add(
                    self.current_basename
                )
            cnt = cnt[: span[0]] + str(value) + cnt[span[1] :]
            srch = self.re_template.search(cnt)
        return cnt

    def check_templates(self, outline, all_files):
        templates = sorted(
            {x.group("filename") for x in self.re_template_file.finditer(outline)}
        )
        for t in templates:
            md_file = f"{os.path.splitext(t)[0]}.md"
            if md_file not in all_files:
                self.missing_template_files.add(md_file)

    @classmethod
    def process_found_variant(
        cls, srch: re.Match, variant_group: list[str], cnt: str
    ) -> str:
        grp = srch.group(0)
        start, end = srch.span()
        var_end = grp[0] + "/" + grp[1:]
        var_end_len = len(var_end)
        closing_start = start + cnt[start:].index(var_end)
        closing_end = closing_start + var_end_len
        if srch.group("varname") in variant_group:
            cnt = cnt[:start] + cnt[end:closing_start] + cnt[closing_end:]
        else:
            cnt = cnt[:start] + cnt[closing_end:]
        return cnt

    def process_variants(self, cnt, fn):
        distinct_variants = sorted(
            {srch.group("varname") for srch in self.re_variant_start.finditer(cnt)}
        )
        result = []
        if self.front_matter and self.front_matter.get("cpr_variants"):
            variants = self.front_matter["cpr_variants"]
        else:
            variants = distinct_variants
        for variant_group in variants:
            if isinstance(variant_group, str):
                variant_group = [variant_group]
            var_cnt = cnt
            srch = self.re_variant_start.search(var_cnt)
            count = 0
            while srch:
                count += 1
                var_cnt = self.process_found_variant(srch, variant_group, var_cnt)
                srch = self.re_variant_start.search(var_cnt)
            var_cnt = self.eval_templates(var_cnt)
            bn, ext = os.path.splitext(fn)
            out_fn_md = f"{bn}_{'_'.join(variant_group)}{ext}"
            result.append((out_fn_md, var_cnt))
        return result

    def process_file(self, basename, replacement_content=None):
        self.current_basename = basename
        outline_file = self.ctx.get("outline_file")
        if outline_file is not None and outline_file in basename:
            if not replacement_content:
                with _open(basename, "r") as f:
                    outline = f.read()
            else:
                outline = replacement_content
            all_files = sorted(
                fn
                for fn in os.listdir(self.dirname)
                if not fn.startswith(("~", ".", "_"))
            )
            self.check_templates(outline, all_files)

        print(f"template processing {basename}...")
        if replacement_content:
            cnt = replacement_content
        else:
            with _open(os.path.join(self.dirname, basename), "r") as f:
                cnt = f.read()

        self.front_matter, _ = read_front_matter(cnt)
        if "ctx" in self.front_matter:
            self.ctx.update(self.front_matter["ctx"])
        if "<var:" in cnt:
            return self.process_variants(cnt, basename)
        else:
            return self.eval_templates(cnt)

    def post_work(self):
        if self.unresolved_templates:
            sys.stderr.write("The following templates were unresolved:\n\n")
            for t in sorted(self.unresolved_templates):
                errs = [
                    f"{k}: {sorted(v)}" for k, v in self.unresolved_templates[t].items()
                ]
                sys.stderr.write(f"{t}: {errs}\n")
        if self.templates_resolved_to_bad_values:
            sys.stderr.write("The following templates were resolved to bad values:\n\n")
            for t in sorted(self.templates_resolved_to_bad_values):
                values = ", ".join(
                    repr(x) for x in self.templates_resolved_to_bad_values[t]
                )
                sys.stderr.write(f"{t}: {values}\n")
        if self.missing_template_files:
            sys.stderr.write(
                f"The following template files were missing: {', '.join(sorted(self.missing_template_files))}"
            )
