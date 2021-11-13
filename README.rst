elective
--------

A configuration option loader for python.

.. image:: https://badge.fury.io/py/elective.svg
   :target: https://badge.fury.io/py/elective
   :alt: PyPI Version
.. image:: https://readthedocs.org/projects/elective/badge/?version=latest
   :target: https://elective.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

What is elective?
~~~~~~~~~~~~~~~~~

``elective`` is a Python program configuration loader generator that
can leverage environment variables, configuration files (TOML, JSON,
YAML, BespON), and the command line (via ``argparse``) to generate a
custom loader module to use in your Python application with a goal of
being able to specify any configurable option identically via any
generation method.  ``elective`` supports customization of the
providers file formats and of the method of combining the results from
all providers.

Roadmap
~~~~~~~

* Allow for configurable provider precedence.
* Allow for configurable file format precedence.
* Allow for configurable provider combination.
* Create left merge, right merge, and join provider combiners.
* Generate boolean options.
* Generate string options.
* Generate number options.
* Generate list options.
* Generate hash options.
* Create configuration object interface.
* Generate dependency requirements for parent projects (pip).
* Generate dependency requirements for parent projects (poetry).
* Allow for configurable file format dependencies.
* Create TOML configuration to generate configuration generators.
* Bootstrap to self-host the ``elective`` configuration generator.

Installation
~~~~~~~~~~~~

Install elective with::

  pip install elective
  pip freeze > requirements.txt

or with poetry::

  poetry add elective

Usage
~~~~~

In code::

  >>> import elective

See the source and `documentation
<https://elective.readthedocs.io/en/latest/>`_ for more information.

Copyright and License
=====================

SPDX-License-Identifier: `MIT <https://spdx.org/licenses/MTI.html>`_

django-loader:  a configuration variable and secrets loader for Django
apps.

Copyright (C) 2021 `Jeremy A Gray <gray@flyquackswim.com>`_.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Author
~~~~~~

`Jeremy A Gray <jeremy.a.gray@gmail.com>`_
