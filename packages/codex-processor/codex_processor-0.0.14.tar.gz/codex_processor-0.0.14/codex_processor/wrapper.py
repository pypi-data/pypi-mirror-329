import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from codex_processor.codex_processor import CodexProcessor
from codex_processor.converter import Converter
from codex_processor.template_processor import TemplateProcessor
from codex_processor.utils import (
    FontFinder,
    _open,
    get_resource_dir,
    get_codex_processor_dir,
    load_config,
    copy_file,
)


class ProcessorWrapper:
    def __init__(
        self,
        source_path,
        config_path=None,
        target_path=None,
        add_file_prefix=None,
        output_format="auto",
        do_codex_processing=True,
        copy_md=False,
        # codex processor args
        remake_footnotes=False,
        resolve_external_links=False,
        typograph=True,
        # template processor args
        ctx=None,
        ctx_file=None,
        ctx_builder_module_path=None,
        ctx_builder_args=None,
        ctx_builder_kwargs=None,
        # converter args
        converter_config_path=None,
        template_file=None,
        pandoc_extra_args=None,
        latex_vargs=None,
        latex_bin=None,
        toc=False,
        add_pdf=False,
        latex_fix=True,
        save_raw_tex=False,
        parallel_processing=True,
        pandoc_path=None,
        tectonic_path=None,
        timeout=None,
    ):
        self.source_path = source_path
        self.target_path = target_path
        self.do_codex_processing = do_codex_processing
        self.copy_md = copy_md
        self.remake_footnotes = remake_footnotes
        self.resolve_external_links = resolve_external_links
        self.typograph = typograph
        self.ctx = ctx
        self.ctx_file = ctx_file
        self.ctx_builder_module_path = ctx_builder_module_path
        self.ctx_builder_args = ctx_builder_args
        self.ctx_builder_kwargs = ctx_builder_kwargs
        self.config_path = config_path
        self.add_file_prefix = add_file_prefix
        self.output_format = output_format
        self.converter_config_path = converter_config_path
        self.template_file = template_file
        self.parallel_processing = parallel_processing
        if (
            output_format == "latex"
            and self.template_file is None
            and self.converter_config_path is None
        ):
            self.converter_config_path = os.path.join(
                get_resource_dir(), "latex_source.json"
            )
        if output_format == "docx" and self.template_file is None:
            self.template_file = os.path.join(get_resource_dir(), "template.docx")
        self.pandoc_extra_args = pandoc_extra_args
        self.latex_vargs = latex_vargs
        self.latex_bin = latex_bin
        self.toc = toc
        self.add_pdf = add_pdf
        self.latex_fix = latex_fix
        self.save_raw_tex = save_raw_tex
        self.pandoc_path = pandoc_path
        self.tectonic_path = tectonic_path
        self.timeout = timeout
        if self.config_path:
            self.config = load_config(self.config_path)
            for k, v in self.config.items():
                setattr(self, k, v)
        else:
            self.config = None
        if os.path.isdir(self.source_path):
            dirname = os.path.abspath(self.source_path)
        elif os.path.isfile(self.source_path):
            dirname = os.path.dirname(os.path.abspath(self.source_path))
        else:
            raise Exception(f"{self.source_path} not found")
        self.tp = TemplateProcessor(
            dirname=dirname,
            ctx=ctx,
            ctx_file=ctx_file,
            ctx_builder_module_path=ctx_builder_module_path,
            ctx_builder_args=ctx_builder_args,
            ctx_builder_kwargs=ctx_builder_kwargs,
        )
        if output_format in ("latex", "latex_raw", "auto"):
            self.ff = FontFinder(get_codex_processor_dir())
        else:
            self.ff = None

    @classmethod
    def make_file_list(cls, source_path):
        file_list = []
        copy_list = []
        for fn in sorted(os.listdir(source_path)):
            if fn.startswith(("~", ".")):
                continue
            full_path = os.path.join(source_path, fn)
            if fn.endswith(".md"):
                file_list.append(full_path)
            else:
                copy_list.append(full_path)
        return file_list, copy_list

    def spawn_converter(self, dirname):
        return Converter(
            dirname=dirname,
            font_finder=self.ff,
            latex_bin=self.tectonic_path,
            timeout=self.timeout,
            pandoc_path=self.pandoc_path,
        )

    def process(self):
        source_path = self.source_path
        if os.path.isdir(source_path):
            if not self.target_path:
                source_dirname = os.path.abspath(os.path.dirname(source_path))
                output = os.path.join(source_dirname, "output")
                if os.path.isfile(output):
                    raise Exception("'output' is a file")
                if not os.path.isdir(output):
                    os.mkdir(output)
                    self.target_path = output
            if self.target_path and os.path.isfile(self.target_path):
                raise Exception(f"target path '{self.target_path}' is a file")
            if self.target_path and not os.path.exists(self.target_path):
                os.makedirs(self.target_path)
            file_list, copy_list = self.make_file_list(source_path)
            for filepath in copy_list:
                target_path = os.path.join(self.target_path, os.path.basename(filepath))
                copy_file(filepath, target_path)
            futures = []
            if self.parallel_processing:
                with ThreadPoolExecutor(max_workers=16) as executor:
                    for full_path in file_list:
                        futures.append(executor.submit(self.process_file, full_path))
                for fut in as_completed(futures):
                    fut.result()
            else:
                for full_path in file_list:
                    self.process_file(full_path)
        elif os.path.isfile(source_path):
            self.process_file(source_path)
        else:
            raise Exception(f"path '{source_path}' does not exist")
        if self.tp:
            self.tp.post_work()

    def convert_file(self, conv, src, trg):
        if self.copy_md:
            trg_md = conv.replace_extension(trg, ".md")
            with _open(trg_md, "w") as f:
                f.write(src)
        return conv.process_file(
            src,
            output_format=self.output_format,
            source_from_string=True,
            target_filepath=trg,
            template_file=self.template_file,
            pandoc_extra_args=self.pandoc_extra_args,
            latex_vargs=self.latex_vargs,
            toc=self.toc,
            add_pdf=self.add_pdf,
            latex_fix=self.latex_fix,
            save_raw_tex=self.save_raw_tex,
            config_path=self.converter_config_path,
        )

    def get_target_path(self, dirname, basename):
        output_basename = (self.add_file_prefix or "") + Converter.replace_extension(
            basename, Converter.get_extension(self.output_format)
        )
        if not self.target_path:
            final_target_path = os.path.join(dirname, output_basename)
        elif os.path.isdir(self.target_path):
            final_target_path = os.path.join(self.target_path, output_basename)
        return final_target_path

    def codex_processing(self, cnt):
        if self.do_codex_processing:
            cp = CodexProcessor(
                cnt,
                remake_footnotes=self.remake_footnotes,
                resolve_external_links=self.resolve_external_links,
                skip_output=True,
                source_from_string=True,
                typograph=self.typograph,
            )
            cnt = cp.process()
        return cnt

    def process_tup(self, tup, dirname):
        fn = tup[0]
        cnt = tup[1]
        cnt = self.codex_processing(cnt)
        final_target_path = self.get_target_path(dirname, fn)
        conv = self.spawn_converter(dirname)
        self.convert_file(conv, cnt, final_target_path)

    def process_file(self, source_file_path):
        dirname = os.path.abspath(os.path.dirname(source_file_path))
        basename = os.path.basename(source_file_path)
        final_target_path = self.get_target_path(dirname, basename)
        with _open(source_file_path, "r") as f:
            cnt = f.read()
        if self.tp:
            tp_output = self.tp.process_file(basename, replacement_content=cnt)
            if isinstance(tp_output, list):
                if self.parallel_processing:
                    futures = []
                    with ThreadPoolExecutor(max_workers=8) as executor:
                        for tup in tp_output:
                            futures.append(
                                executor.submit(self.process_tup, tup, dirname)
                            )
                    for fut in as_completed(futures):
                        fut.result()
                else:
                    for tup in tp_output:
                        self.process_tup(tup, dirname)
            else:
                tp_output = self.codex_processing(tp_output)
                conv = self.spawn_converter(dirname)
                self.convert_file(conv, tp_output, final_target_path)
        elif self.do_codex_processing:
            tp_output = self.codex_processing(cnt)
            conv = self.spawn_converter(dirname)
            self.convert_file(conv, tp_output, final_target_path)
        else:
            conv = self.spawn_converter(dirname)
            self.convert_file(conv, cnt, final_target_path)
