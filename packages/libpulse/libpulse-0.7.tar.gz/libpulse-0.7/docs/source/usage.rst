Usage
=====

.. _`context-manager-connection`:

Connecting to the sound server
------------------------------
Instantiation of the :ref:`libpulse-class` by the async context manager with the
`async with` statement does the following:

- The `LibPulse` instance is created and assigned as the target of the context
  manager.
- The instance connects to the sound server.
- The instance monitors the state of the connection by subscribing a callback to
  the sound server.
- The `c_context` instance attribute is available as parameter to non-async
  functions.
- The `state`  instance attribute is updated by the state monitor callback
  whenever the callback is invoked by the sound server.

The context manager may raise `LibPulseStateError` while attempting the
connection.

.. _session-management:

Session management
------------------
When the connection fails for any reason, the state monitor callback cancels the
asyncio task of the async context manager. This causes the async context manager
to terminate gracefully.

When the async context manager terminates because it got a CancelledError
exception or because it terminates normally or because it got any other
exception, all the asyncio tasks listed by `libpulse_tasks` are also cancelled
allowing those tasks to do some clean up on exit.

`libpulse_tasks` is an attribute of the `LibPulse` instance and an instance of
:ref:`AsyncioTasks`. The tasks listed by `libpulse_tasks` are the still active
asyncio tasks that have been created by its `create_task()` method.

So `libpulse_tasks` can also be used by any application built upon libpulse to
have tasks do some clean up upon termination of the async context manager. As an
example, in the following code the task of the *user_task* coroutine is
cancelled upon termination of the async context manager and *"user_task got
CancelledError"* is printed:

.. code-block:: python

    import asyncio
    import libpulse.libpulse as libpulse

    async def user_task(ready, cancelled):
        try:
            ready.set_result(True)
            # Run an infinite loop.
            while True:
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            print('user_task got CancelledError')
            cancelled.set_result(True)
            pass

    async def main():
        async with libpulse.LibPulse('my libpulse') as lp_instance:
            ready = lp_instance.loop.create_future()
            cancelled = lp_instance.loop.create_future()
            lp_instance.libpulse_tasks.create_task(user_task(ready, cancelled))

            # Wait for 'user_task' to be ready.
            await ready

        await cancelled

    asyncio.run(main())

.. _error-handling:

Error handling
--------------
The return value of a libpulse function corresponding to a non-async ``pulse``
function should be checked against `None` or `PA_INVALID_INDEX` when the
function returns an index.

All the LibPulse methods that are asyncio coroutines corresponding to ``pulse``
async functions **may raise** `LibPulseOperationError`.

See also the `Error Handling`_ section of the PulseAudio documentation.

.. _`ctypes-pulse-structures`:

ctypes pulse structures
-----------------------
The parameters of some pulse functions are pointers to pulse structures.
Here is an example showing how to build a ctypes pointer to the
`pa_sample_spec` structure:

.. code-block:: python

    import ctypes as ct
    import libpulse.libpulse as libpulse

    # The 'pa_sample_spec' ctypes subclass of ct.Structure.
    ct_struct_sample_spec = libpulse.struct_ctypes['pa_sample_spec']

    # Instantiate ct_struct_sample_spec with (3, 44100, 2)
    sample_spec = {'format': 3, 'rate': 44100, 'channels': 2}
    ct_sample_spec = ct_struct_sample_spec(*sample_spec.values())

    # 'ptr' may be used as a parameter of type 'pa_sample_spec *' of a ctypes
    # foreign function.
    # Using ctypes pointer() here to be able to print the pointer contents
    # below, but lightweight byref() is sufficient if only passing the pointer
    # as a function parameter.
    ptr = ct.pointer(ct_sample_spec)

    # Dereference the pointer.
    contents = ptr.contents

    # This will print 'format: 3, rate: 44100, channels: 2'.
    print(f'format: {contents.format}, rate: {contents.rate},'
          f' channels: {contents.channels}')

    # This will print '176400'.
    bps = libpulse.pa_bytes_per_second(ptr)
    print(bps)

    # Using ct.byref() instead of ct.pointer().
    # This will print '176400'.
    bps = libpulse.pa_bytes_per_second(ct.byref(ct_sample_spec))
    print(bps)

A simpler way is to instantiate one of the convenience classes `Pa_buffer_attr`,
`Pa_cvolume`, `Pa_channel_map`, `Pa_format_info` or `Pa_sample_spec` and call
its `byref()` method. See the :ref:`CtypesPulseStructure` section.

In that case the above example becomes:

.. code-block:: python

   ptr = libpulse.Pa_sample_spec(*sample_spec.values()).byref()

`examples/pa_stream_new.py`_ shows how to create instances of two structures and
pass their pointers to `pa_stream_new()`. The example shows also how to build
a `PulseStructure` from a pointer returned by `pa_stream_get_sample_spec()`. See
the :ref:`PulseStructure` section.

The implementation of the ``pactl`` module uses the `Pa_cvolume` and
`Pa_channel_map` classes to build ctypes `Structure`_ instances and pass their
pointer to some of the `pactl.py non-async functions`_.

.. _`Error Handling`:
   https://freedesktop.org/software/pulseaudio/doxygen/index.html#error_sec
.. _examples/pa_stream_new.py:
   https://gitlab.com/xdegaye/libpulse/-/blob/master/examples/pa_stream_new.py?ref_type=heads#L1
.. _`pactl.py non-async functions`:
   https://gitlab.com/xdegaye/libpulse/-/blob/master/libpulse/pactl.py?ref_type=heads#L30
.. _`Structure`:
   https://docs.python.org/3/library/ctypes.html#ctypes.Structure
