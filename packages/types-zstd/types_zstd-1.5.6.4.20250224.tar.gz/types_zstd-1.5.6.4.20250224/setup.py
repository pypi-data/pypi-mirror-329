from setuptools import setup

name = "types-zstd"
description = "Typing stubs for zstd"
long_description = '''
## Typing stubs for zstd

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`zstd`](https://github.com/sergey-dryabzhinsky/python-zstd) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `zstd`. This version of
`types-zstd` aims to provide accurate annotations for
`zstd==1.5.6.4`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/zstd`](https://github.com/python/typeshed/tree/main/stubs/zstd)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`c27e41c33b47edc624ca456e673c7d29a46c7e5c`](https://github.com/python/typeshed/commit/c27e41c33b47edc624ca456e673c7d29a46c7e5c).
'''.lstrip()

setup(name=name,
      version="1.5.6.4.20250224",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/zstd.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['zstd-stubs'],
      package_data={'zstd-stubs': ['__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
