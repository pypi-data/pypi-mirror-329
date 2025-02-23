from setuptools import setup

name = "types-zxcvbn"
description = "Typing stubs for zxcvbn"
long_description = '''
## Typing stubs for zxcvbn

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`zxcvbn`](https://github.com/dwolfhub/zxcvbn-python) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `zxcvbn`. This version of
`types-zxcvbn` aims to provide accurate annotations for
`zxcvbn==4.5.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/zxcvbn`](https://github.com/python/typeshed/tree/main/stubs/zxcvbn)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`a61270c38c1aa59c6f10298e0161235ccb7d31d9`](https://github.com/python/typeshed/commit/a61270c38c1aa59c6f10298e0161235ccb7d31d9).
'''.lstrip()

setup(name=name,
      version="4.5.0.20250223",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/zxcvbn.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['zxcvbn-stubs'],
      package_data={'zxcvbn-stubs': ['__init__.pyi', 'adjacency_graphs.pyi', 'feedback.pyi', 'frequency_lists.pyi', 'matching.pyi', 'scoring.pyi', 'time_estimates.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
