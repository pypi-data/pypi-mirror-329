from setuptools import setup


def get_version():
    version = {}
    with open("codex_processor/version.py") as f:
        exec(f.read(), version)
    return version["__version__"]


long_description = """**codex_processor** is a utility that provides
some wrappers around pandoc that help working with documents
that have numbered paragraphs with cross-links, such as
legal documents or tournament rulebooks.

Project home on gitlab: https://gitlab.com/peczony/codex_processor
"""


setup(
    name="codex_processor",
    version=get_version(),
    author="Alexander Pecheny",
    author_email="ap@pecheny.me",
    description="A pandoc wrapper with some helper scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/peczony/codex_processor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["codex_processor"],
    package_data={
        "codex_processor": [
            "resources/*.json",
            "resources/*.docx",
            "resources/*.tex",
        ]
    },
    entry_points={"console_scripts": ["cpr = codex_processor.__main__:main"]},
    install_requires=[
        "beautifulsoup4",
        "markdown-it-py",
        "pyaml",
        "pypandoc",
        "requests",
        "toml",
    ],
)
