.. image:: images/coverage.png
   :alt: [libpulse test coverage]

Asyncio interface to the Pulseaudio and Pipewire pulse library.

Overview
--------
`libpulse`_ is a Python package based on `asyncio`_, that uses `ctypes`_ to
interface with the ``pulse`` library of the PulseAudio and PipeWire sound
servers.

The interface is meant to be complete. That is, all the constants, structures,
plain functions and async functions are made available by importing the libpulse
module of the libpulse package.

Async functions are those ``pulse`` functions that return results through a
callback. They are implemented as asyncio coroutines that return the callback
results. They have the same name as the corresponding pulse async function.

Non-async ``pulse`` functions have their corresponding ctypes foreign functions
defined in the libpulse module namespace under the same name as the
corresponding pulse function. They may be called directly.

Calling an async function or a plain function is simple:

.. code-block:: python

    import asyncio
    import libpulse.libpulse as libpulse

    async def main():
        async with libpulse.LibPulse('my libpulse') as lp_instance:
            # A plain function.
            server = libpulse.pa_context_get_server(lp_instance.c_context)
            print('server:', server.decode())

            # An async function.
            sink = await lp_instance.pa_context_get_sink_info_by_index(0)
            print('sample_spec rate:', sink.sample_spec.rate)
            print('proplist names:', list(sink.proplist.keys()))

    asyncio.run(main())

Another example processing ``pulse`` events:

.. code-block:: python

    import asyncio
    import libpulse.libpulse as libpulse

    async def main():
        async with libpulse.LibPulse('my libpulse') as lp_instance:
            await lp_instance.pa_context_subscribe(
                                    libpulse.PA_SUBSCRIPTION_MASK_ALL)
            iterator = lp_instance.get_events_iterator()

            async for event in iterator:
                # Start playing some sound to print the events.
                # 'event' is an instance of the PulseEvent class.
                print(event.__dict__)

    asyncio.run(main())

The libpulse package also includes the ``pactl-py`` command, which is a Python
implementation of the ``pactl`` command running on Pulseaudio and Pipewire. The
output of most ``pactl-py`` subcommands can be parsed by Python. When this
output is redirected to a file, the file can be imported as a Python module. For
example start an interactive Python session and inspect the ``cards`` object
with all its nested sructures and dereferenced pointers with:

.. code-block:: shell

    $ pactl-py list cards > cards.py && python -i cards.py

Requirements
------------
Python version 3.8 or more recent.

Documentation
-------------
The libpulse documentation is hosted at `Read the Docs`_:

 - The `stable documentation`_ of the last released version.
 - The `latest documentation`_ of the current GitLab development version.

To access the documentation as a pdf document one must click on the icon at the
down-right corner of any page. It allows to switch between stable and latest
versions and to select the corresponding pdf document.

The documentation describing the C language API of the ``pulse`` library is at
`PulseAudio Documentation`_.

Installation
------------
Install ``libpulse`` with pip::

  $ python -m pip install libpulse

.. _libpulse: https://gitlab.com/xdegaye/libpulse
.. _asyncio: https://docs.python.org/3/library/asyncio.html
.. _ctypes: https://docs.python.org/3/library/ctypes.html
.. _Read the Docs: https://about.readthedocs.com/
.. _stable documentation: https://libpulse.readthedocs.io/en/stable/
.. _latest documentation: https://libpulse.readthedocs.io/en/latest/
.. _`PulseAudio Documentation`:
   https://freedesktop.org/software/pulseaudio/doxygen/index.html
