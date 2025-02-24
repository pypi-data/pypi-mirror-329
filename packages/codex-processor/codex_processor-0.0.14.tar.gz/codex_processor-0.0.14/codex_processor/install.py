import functools
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import zipfile
from typing import NamedTuple

import requests
from pypandoc.pandoc_download import download_pandoc

from codex_processor.utils import FontFinder, get_codex_processor_dir


class HealthCheckResult(NamedTuple):
    pandoc_path: str
    pandoc_ok: bool
    tectonic_path: str
    tectonic_ok: bool
    font_finder: FontFinder
    fonts_ok: bool
    errors: list[str]


def health_check():
    errors = []
    system = platform.system()

    if system == "Darwin":
        pandoc_path = os.path.join(
            os.path.expanduser("~"), "Applications", "pandoc", "pandoc"
        )
    elif system == "Windows":
        pandoc_path = os.path.join(
            os.path.expanduser("~"), "AppData", "Local", "pandoc", "pandoc.exe"
        )
    else:
        pandoc_path = os.path.join(os.path.expanduser("~"), "bin", "pandoc")

    pandoc_ok = False
    if os.path.isfile(pandoc_path):
        try:
            proc = subprocess.run(
                [pandoc_path, "--version"], capture_output=True, check=True
            )
            decoded_stdout = proc.stdout.decode(sys.stdout.encoding, errors="replace")
            pandoc_ok = proc.returncode == 0 and decoded_stdout.startswith("pandoc")
        except subprocess.CalledProcessError as e:
            errors.append(f"pandoc --version failed: {type(e)} {e}")
        if not decoded_stdout.startswith("pandoc"):
            errors.append(f"bad stdout from pandoc: {decoded_stdout}")
    else:
        errors.append(f"pandoc not found at {pandoc_path}")

    cpdir = get_codex_processor_dir()
    if system == "Windows":
        tectonic_path = os.path.join(cpdir, "tectonic.exe")
    else:
        tectonic_path = os.path.join(cpdir, "tectonic")

    tectonic_ok = False
    if os.path.isfile(tectonic_path):
        try:
            proc = subprocess.run(
                [tectonic_path, "--version"], capture_output=True, check=True
            )
            tectonic_ok = proc.returncode == 0 and proc.stdout.decode(
                "utf8"
            ).lower().startswith("tectonic")
        except subprocess.CalledProcessError as e:
            errors.append(f"tectonic --version failed: {type(e)} {e}")

    ff = FontFinder(cpdir)
    if ff.not_found:
        errors.append(f"fonts were not found: {ff.not_found}")
    return HealthCheckResult(
        pandoc_path=pandoc_path,
        pandoc_ok=pandoc_ok,
        tectonic_path=tectonic_path,
        tectonic_ok=tectonic_ok,
        font_finder=ff,
        fonts_ok=not ff.not_found,
        errors=errors,
    )


def github_get_latest_release(repo):
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    req = requests.get(url)
    assets_url = req.json()["assets_url"]
    assets_req = requests.get(assets_url)
    return {asset["name"]: asset["browser_download_url"] for asset in assets_req.json()}


def darwin_is_emulated():
    sub = subprocess.run(
        ["sysctl", "-n", "sysctl.proc_translated"], capture_output=True, check=True
    )
    out = sub.stdout.decode("utf8").strip()
    return int(out)


def parse_tectonic_archive_name(archive_name):
    if archive_name.endswith(".tar.gz"):
        archive_name = archive_name[: -len(".tar.gz")]
    elif archive_name.endswith(".zip"):
        archive_name = archive_name[: -len(".zip")]
    else:
        return
    sp = archive_name.split("-")
    result = {
        "version": sp[1],
        "arch": sp[2],
        "manufacturer": sp[3],
        "system": sp[4],
    }
    if len(sp) > 5:
        result["toolchain"] = sp[5]
    return result


# download_file function taken from https://stackoverflow.com/a/39217788
def download_file(url):
    print(f"downloading from {url}...")
    local_filename = url.split("/")[-1]
    with requests.get(url, stream=True) as resp:
        resp.raw.read = functools.partial(resp.raw.read, decode_content=True)
        with open(local_filename, "wb") as f:
            shutil.copyfileobj(resp.raw, f, length=16 * 1024 * 1024)
    return local_filename


def extract_zip(zip_file, dirname=None):
    if dirname is None:
        dirname = zip_file[:-4]
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(dirname)
    os.remove(zip_file)


def extract_tar(tar_file, dirname=None):
    if dirname is None:
        dirname = tar_file[: tar_file.lower().index(".tar")]
    tf = tarfile.open(tar_file)
    tf.extractall(dirname)
    os.remove(tar_file)


def extract_archive(filename, dirname=None):
    if filename.lower().endswith((".tar", ".tar.gz")):
        extract_tar(filename, dirname=dirname)
    elif filename.lower().endswith(".zip"):
        extract_zip(filename, dirname=dirname)


def install_tectonic():
    system = platform.system()
    proc = platform.processor()
    assets = github_get_latest_release("tectonic-typesetting/tectonic")
    archive_url = None
    if system == "Darwin":
        if proc == "arm" or (proc == "i386" and darwin_is_emulated()):
            arch = "aarch64"
        else:
            arch = "x86_64"
        for k, v in assets.items():
            parsed = parse_tectonic_archive_name(k)
            if not parsed:
                continue
            if parsed["arch"] == arch and parsed["system"] == "darwin":
                archive_url = v
    elif system == "Windows":
        for k, v in assets.items():
            parsed = parse_tectonic_archive_name(k)
            if not parsed:
                continue
            if (
                parsed["arch"] == "x86_64"
                and parsed["system"] == "windows"
                and parsed["toolchain"] == "msvc"
            ):
                archive_url = v
    elif system == "Linux":
        for k, v in assets.items():
            parsed = parse_tectonic_archive_name(k)
            if not parsed:
                continue
            if (
                parsed["arch"] == proc
                and parsed["system"] == "linux"
                and parsed["toolchain"] == "musl"
            ):
                archive_url = v
    downloaded = download_file(archive_url)
    dirname = "tectonic_folder"
    extract_archive(downloaded, dirname=dirname)
    if system == "Windows":
        filename = "tectonic.exe"
    else:
        filename = "tectonic"
    target_path = os.path.join(get_codex_processor_dir(), filename)
    shutil.move(os.path.join(dirname, filename), target_path)
    shutil.rmtree(dirname)
    return target_path


def install_font(url):
    fn = url.split("/")[-1].split("?")[0]
    bn, ext = os.path.splitext(fn)
    if "." in bn:
        new_fn = bn.replace(".", "_") + ext
    else:
        new_fn = fn
    dir_name = new_fn[:-4]
    dir_name_base = dir_name.split(os.pathsep)[-1]
    fonts_dir = os.path.join(get_codex_processor_dir(), "fonts")
    if not os.path.exists(fonts_dir):
        os.makedirs(fonts_dir)
    target_dir = os.path.join(fonts_dir, dir_name_base)
    if os.path.isdir(target_dir):
        print(f"{target_dir} already exists")
        return
    download_file(url)
    if fn != new_fn:
        os.rename(fn, new_fn)
    extract_archive(new_fn, dirname=dir_name)
    if not os.path.isdir(target_dir):
        shutil.copytree(dir_name, target_dir)
    shutil.rmtree(dir_name)


def install_font_from_github_wrapper(repo):
    latest = github_get_latest_release(repo)
    for k, v in latest.items():
        if k.endswith(".zip"):
            install_font(v)
            break


def wrap_install_command(func, args=None, kwargs=None, skip_on_error=False):
    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}
    try:
        return func(*args, **kwargs)
    except Exception as e:
        sys.stderr.write(f"error while trying to {func} {args} {kwargs}: {type(e)} {e}")
        if not skip_on_error:
            raise


def install(skip_on_error=False, ctan_mirror_override=None):
    wrap_install_command(install_tectonic)
    wrap_install_command(
        install_font_from_github_wrapper,
        ["alerque/libertinus"],
        skip_on_error=skip_on_error,
    )
    print("installed libertinus font")
    if ctan_mirror_override is None:
        ctan_mirror_override = "mirrors.ctan.org"
    wrap_install_command(
        install_font,
        [f"https://{ctan_mirror_override}/fonts/tex-gyre-math.zip"],
        skip_on_error=skip_on_error,
    )
    print("installed tex gyre math fonts")
    wrap_install_command(
        install_font_from_github_wrapper,
        ["adobe-fonts/source-serif"],
        skip_on_error=skip_on_error,
    )
    print("installed source serif font")
    wrap_install_command(
        install_font_from_github_wrapper,
        ["adobe-fonts/source-code-pro"],
        skip_on_error=skip_on_error,
    )
    print("installed source code pro font")
    wrap_install_command(download_pandoc, skip_on_error=skip_on_error)
