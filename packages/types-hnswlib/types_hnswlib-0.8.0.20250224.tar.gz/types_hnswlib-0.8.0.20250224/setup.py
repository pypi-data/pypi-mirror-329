from setuptools import setup

name = "types-hnswlib"
description = "Typing stubs for hnswlib"
long_description = '''
## Typing stubs for hnswlib

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`hnswlib`](https://github.com/nmslib/hnswlib) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `hnswlib`. This version of
`types-hnswlib` aims to provide accurate annotations for
`hnswlib==0.8.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/hnswlib`](https://github.com/python/typeshed/tree/main/stubs/hnswlib)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`c27e41c33b47edc624ca456e673c7d29a46c7e5c`](https://github.com/python/typeshed/commit/c27e41c33b47edc624ca456e673c7d29a46c7e5c).
'''.lstrip()

setup(name=name,
      version="0.8.0.20250224",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/hnswlib.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['numpy>=1.20'],
      packages=['hnswlib-stubs'],
      package_data={'hnswlib-stubs': ['__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
