================
Files to folders
================


.. image:: https://img.shields.io/pypi/v/files_to_folders.svg
        :target: https://pypi.python.org/pypi/files_to_folders

.. image:: https://img.shields.io/travis/d0m1987/files_to_folders.svg
        :target: https://travis-ci.com/d0m1987/files_to_folders

.. image:: https://readthedocs.org/projects/files-to-folders/badge/?version=latest
        :target: https://files-to-folders.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Move files into folders based on their filename / filepath using regular expressions.


* Free software: MIT license
* Documentation: https://files-to-folders.readthedocs.io.


Features
--------

* Sort files into folders based on their filename / filepath using regular expressions
* Can be used in the command line, e.g. in scripts or for piping

Installation
------------

```console
$ pip install git+https://github.com/d0m1987/files_to_folders.git
```

Examples
--------

Assuming the following folder structure (that can be found in examples/first_simple_example)...
```console
.
├── test_123.txt
└── test_124.txt
```

we run the following command in the folder with the structure above
```console````
$ files_to_folders --regexes "([a-z]*)_([0-9]*).txt" test_123.txt test_124.txt
```

This gives us the following folder structure:
```console
.
├── files_to_folders.log
└── test
    ├── 123
    │   └── test_123.txt
    └── 124
        └── test_124.txt
```

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
