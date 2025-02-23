.. _Development:

Development
===========

.. _Callbacks:

Callbacks
---------
All the LibPulse async methods ultimately call either `_pa_get()` or
`_pa_get_list()`. Both coroutines follow the same design:

- Define a nested function as the callback.
- Create the ctypes function pointer for this callback.
- Create an asyncio future.
- Call the ``pulse`` ctypes foreign function and wait on the future that is
  set by the callback upon invocation.
- Return the result.

*So what happens when two asyncio tasks running concurrently are both waiting on
their own future for the completion of the same callback ?*

There is no concurrency issue. The ``ctypes`` pakage creates the ctypes function
pointer for the callback by calling `PyCFuncPtr_new()`_ which in turn calls
`_ctypes_alloc_callback()`_. This last function uses ``libffi`` to allocate a
closure (quoting the ``libffi`` documentation [#]_: `closures work by
assembling a tiny function at runtime`). So each one of the two callbacks is
allocated its own closure and gets a different function pointer.

Requirements
------------
**Development**

* GNU ``gcc`` and `pyclibrary`_ are used to parse the libpulse headers and
  create the ``pulse_types``, ``pulse_enums``, ``pulse_structs`` and
  ``pulse_functions`` modules of the libpulse package. To re-create those
  modules using the current libpulse headers run [#]_::

    $ python -m tools.libpulse_parser libpulse

* The ``coverage`` Python package is used to get the test suite coverage.
* `python-packaging`_ is used to set the development version name as conform to
  PEP 440.
* `flit`_ is used to publish libpulse to PyPi and may be used to install
  libpulse locally.

  At the root of the libpulse git repository, use the following command to
  install libpulse locally::

    $ flit install --symlink [--python path/to/python]

  This symlinks libpulse into site-packages rather than copying it, so that you
  can test changes.

**Documentation**

* `Sphinx`_ [#]_.
* `Read the Docs theme`_.
* Building the pdf documentation:

  - The latex texlive package group.
  - Imagemagick version 7 or more recent.

Documentation
-------------
To build locally the documentation follow these steps:

- Fetch the GitLab test coverage badge::

    $ curl -o images/coverage.svg "https://gitlab.com/xdegaye/libpulse/badges/master/coverage.svg?min_medium=85&min_acceptable=90&min_good=90"
    $ magick images/coverage.svg images/coverage.png

- Build the html and pdf documentation::

    $ make -C docs clean html latexpdf

Updating the development version
--------------------------------
Run the following commands to update the version name at `latest documentation`_
after a bug fix or a change in the features::

    $ python -m tools.set_devpt_version_name
    $ make -C docs clean html latexpdf
    $ git commit -m "Update development version name"
    $ git push

Releasing
---------
* Run the test suite from the root of the project [#]_::

    $ python -m unittest --verbose --catch --failfast

* Get the test suite coverage::

    $ coverage run --include="./*" -m unittest
    $ coverage report -m

* Update ``__version__`` in libpulse/__init__.py.
* Update docs/source/history.rst if needed.
* Build locally the documentation, see the previous section.
* Commit the changes::

    $ git commit -m 'Version 0.n'
    $ git push

* Tag the release and push::

    $ git tag -a 0.n -m 'Version 0.n'
    $ git push --tags

* Publish the new version to PyPi::

    $ flit publish

.. _PyCFuncPtr_new():
    https://github.com/python/cpython/blob/38a25e9560cf0ff0b80d9e90bce793ff24c6e027/Modules/_ctypes/_ctypes.c#L3826
.. _`_ctypes_alloc_callback()`:
    https://github.com/python/cpython/blob/38a25e9560cf0ff0b80d9e90bce793ff24c6e027/Modules/_ctypes/callbacks.c#L348
.. _Read the Docs theme:
    https://docs.readthedocs.io/en/stable/faq.html#i-want-to-use-the-read-the-docs-theme-locally
.. _Sphinx: https://www.sphinx-doc.org/
.. _flit: https://pypi.org/project/flit/
.. _unittest command line options:
    https://docs.python.org/3/library/unittest.html#command-line-options
.. _latest documentation: https://libpulse.readthedocs.io/en/latest/
.. _pyclibrary: https://pypi.org/project/pyclibrary/
.. _python-packaging: https://github.com/pypa/packaging

.. rubric:: Footnotes

.. [#] The ``libffi`` documentation is included in the ``libffi`` package as a
       texinfo document to be browsed by the ``ìnfo`` utility or by ``emacs``.
.. [#] The shell commands in this section are all run from the root of the
       repository.
.. [#] Required versions at ``docs/requirements.txt``.
.. [#] See `unittest command line options`_.
