#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import sys

from codex_processor.install import health_check, install
from codex_processor.utils import parse_json
from codex_processor.wrapper import ProcessorWrapper


def health_check_wrapper():
    health_check_result = health_check()
    if (
        not health_check_result.tectonic_ok
        or not health_check_result.pandoc_ok
        or not health_check_result.fonts_ok
    ):
        sys.stderr.write(
            "health check was not successful. errors: "
            + "\n".join(health_check_result.errors)
            + "\n"
        )
        sys.stderr.write("You might want to run `cpr install`")
        sys.exit(1)
    return health_check_result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_path")
    parser.add_argument("--config", "-c")
    parser.add_argument("--target", "-t")
    parser.add_argument("--add-file-prefix", "-p")
    parser.add_argument("--output-format", "-o", default="auto")
    parser.add_argument("--template-file", "-tmpl")
    parser.add_argument(
        "--do-codex-processing", default=True, action=argparse.BooleanOptionalAction
    )
    parser.add_argument(
        "--resolve-external-links", default=True, action=argparse.BooleanOptionalAction
    )
    parser.add_argument(
        "--remake-footnotes", default=True, action=argparse.BooleanOptionalAction
    )
    parser.add_argument(
        "--typograph", default=True, action=argparse.BooleanOptionalAction
    )
    parser.add_argument("--ctx", "-ctx")
    parser.add_argument("--ctx-file", "-ctxf")
    parser.add_argument("--ctx-builder-module-path", "-ctxmod")
    parser.add_argument("--ctx-builder-args", "-ctxargs")
    parser.add_argument("--ctx-builder-kwargs", "-ctxkwargs")
    parser.add_argument("--converter-config", "-cc")
    parser.add_argument("--pandoc-extra-args", "-pargs")
    parser.add_argument("--latex-vargs", "-lvargs")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--latex-bin", default="lualatex")
    parser.add_argument("--toc", default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument(
        "--copy-md", default=False, action=argparse.BooleanOptionalAction
    )
    parser.add_argument(
        "--add-pdf", default=False, action=argparse.BooleanOptionalAction
    )
    parser.add_argument(
        "--latex-fix", default=True, action=argparse.BooleanOptionalAction
    )
    parser.add_argument(
        "--save-raw-tex", default=False, action=argparse.BooleanOptionalAction
    )
    parser.add_argument(
        "--parallel-processing", default=True, action=argparse.BooleanOptionalAction
    )
    parser.add_argument("--skip-on-error", action="store_true")
    parser.add_argument("--ctan-mirror-override")
    args = parser.parse_args()

    assert args.source_path
    if args.source_path == "install":
        install(
            skip_on_error=args.skip_on_error,
            ctan_mirror_override=args.ctan_mirror_override,
        )
        sys.exit(0)
    elif args.source_path == "healthcheck":
        health_check_wrapper()
        print("health check successful!")
        sys.exit(0)
    assert args.output_format

    health_check_result = health_check_wrapper()
    os.environ.setdefault("PYPANDOC_PANDOC", health_check_result.pandoc_path)

    pw = ProcessorWrapper(
        source_path=args.source_path,
        config_path=args.config,
        target_path=args.target,
        add_file_prefix=args.add_file_prefix,
        output_format=args.output_format,
        template_file=args.template_file,
        do_codex_processing=args.do_codex_processing,
        copy_md=args.copy_md,
        # codex processor args
        remake_footnotes=args.remake_footnotes,
        resolve_external_links=args.resolve_external_links,
        typograph=args.typograph,
        # template processor args
        ctx=parse_json(args.ctx),
        ctx_file=args.ctx_file,
        ctx_builder_module_path=args.ctx_builder_module_path,
        ctx_builder_args=parse_json(args.ctx_builder_args),
        ctx_builder_kwargs=parse_json(args.ctx_builder_kwargs),
        # converter args
        converter_config_path=args.converter_config,
        pandoc_extra_args=parse_json(args.pandoc_extra_args),
        latex_vargs=parse_json(args.latex_vargs),
        latex_bin=args.latex_bin,
        toc=args.toc,
        add_pdf=args.add_pdf,
        latex_fix=args.latex_fix,
        save_raw_tex=args.save_raw_tex,
        parallel_processing=args.parallel_processing,
        pandoc_path=health_check_result.pandoc_path,
        tectonic_path=health_check_result.tectonic_path,
        timeout=args.timeout,
    )
    pw.process()


if __name__ == "__main__":
    main()
