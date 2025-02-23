.. _libpulse-class:

LibPulse class
==============

`class LibPulse(name, server=None, flags=PA_CONTEXT_NOAUTOSPAWN)`

`name`
  Application name that will be passed to `pa_context_new()` upon instantiation.

`server` and `flags`
  They are passed to `pa_context_connect()` when called by the async context
  manager. See the `pa_context_connect() pulse documentation`_.

**LibPulse must not be instantiated directly**. It is instatiated by the async
context manager statement that connects to the PulseAudio or Pipewire server
when it is entered, see :ref:`context-manager-connection`. It must be
instanciated this way:

.. code-block:: python

    import asyncio
    import libpulse.libpulse as libpulse

    async def main():
        async with libpulse.LibPulse('my libpulse') as lp_instance:
            ...

    asyncio.run(main())

Class attributes
----------------
The pulse async functions are implemented as LibPulse methods that are
asyncio coroutines. Those methods are grouped in four lists according to their
signature and the signature of their callback:

`context_methods`:
  These methods return an object that should be checked against `None` or
  `PA_INVALID_INDEX` when the callback of the async function sets an
  index. An example of a method that returns an index is
  `pa_context_load_module()`.

  The `pa_context_send_message_to_object()` method is special in that it
  returns a list of two elements. The first one is an `int` of type
  `pa_operation_state` that is `PA_OPERATION_DONE` in case of success, and
  the second one is the response as a `bytes` object.

`context_success_methods`:
  These methods always return `PA_OPERATION_DONE` or raise
  `LibPulseOperationError` upon failure.

`context_list_methods`:
  These methods return a list of objects of the same type.

  Method names in this list that end with ``info_by_name``, ``info_by_index``,
  ``_info`` or ``_formats`` return a single object instead of a list.

`stream_success_methods`:
  One must refer to the PulseAudio documentation of the function.

The type of the object (or of the objects in a list) returned by these methods
is `int`, `float`, `bytes` or :ref:`PulseStructure`.

See also :ref:`error-handling`.


Instance attributes
-------------------
`c_context`
  ctypes object corresponding to the pulse `pa_context *` opaque pointer used as
  the first parameter of pulse functions whose name starts with ``pa_context``.

  It is used when calling a non-async function that needs it. It is not used
  when waiting on a LibPulse coroutine method when the C pulse async function
  does, as the LibPulse instance does set it instead. See
  :ref:`Pulse-methods-parameters`.

`libpulse_tasks`
 An instance of :ref:`AsyncioTasks`. The :ref:`session-management` section
 explains how to use this object for the creation of asyncio tasks.

`loop`
  The asyncio loop of this `LibPulse` instance.

`state`
  The pulse context state. A tuple whose first element is one of the constants
  of the `pa_context_state` enum as a string. The second element is one of the
  constants of the `pa_error_code` enum as a string.


Public methods
--------------
`async def get_current_instance()`
  A static method.

  There may be only one `LibPulse` instance per asyncio loop and one asyncio
  loop per thread. The libpulse implementation supports multiple threads with
  one `LibPulse` instance per thread.

  Return the current `LibPulse` instance, `None` if the async context manager
  has exited. Raise `LibPulseStateError` if the instance is not in the
  `PA_CONTEXT_READY` state.

  This is used by the `LibPulse` instance callbacks that are static methods to
  get the instance they are running on.

.. _`get_events_iterator`:

`get_events_iterator()`
  Return an Asynchronous Iterator of libpulse events. There can only be one such
  iterator at any given time.

  Use the iterator in an async for loop to loop over `PulseEvent` instances
  whose types have been selected by a previous call to the
  `pa_context_subscribe()` coroutine. `pa_context_subscribe()` may be called
  while the loop on the iterator is running to change the kind of events one is
  interested in. The async for loop may be terminated by invoking the
  `close()` method of the iterator from within the loop or from another asyncio
  task.

.. _`Pulse-methods-parameters`:

Pulse methods parameters
------------------------
Pulse methods are those coroutines that are listed in one of the `Class
attributes`_ and whose return values are also described there.

Some parameters of the Pulse methods are omitted upon invocation:

`pa_context * c`
  The type of the first parameter of the pulse async functions whose name starts
  with ``pa_context`` is `pa_context *`. This parameter is **omitted** upon
  invocation of the corresponding LibPulse method (the Libpulse instance already
  knows it as one of its attributes named `c_context`).


`pa_*_cb_t cb`
  One of the parameters of the pulse async functions is the type of the
  callback. This parameter is **omitted** upon invocation of the corresponding
  LibPulse method as the Libpulse instance already knows this type from the
  signature of the function in the :ref:`pulse_functions` module.

`void * userdata`
  The type of the last parameter of the pulse async functions is `void *`. The
  parameter is meant to be used to match the  callback invocation with the pulse
  function that triggered it when the implementation is done in C language. This
  last parameter is not needed and **omitted** upon invocation of the
  corresponding LibPulse method (the callback is implemented as a nested
  function in the method definition, more details at :ref:`Callbacks`).

For example `pa_context_get_server_info()` is invoked as:

.. code-block:: python

    server_info = await lp_instance.pa_context_get_server_info()

Not implemented
---------------
The following pulse async functions are not implemented as LibPulse methods:

`pa_signal_new()` and `pa_signal_set_destroy()`:
  Signals are handled by asyncio and the hook signal support built into the
  pulse main loop is not needed.

For the following async functions, the callback has to be implemented  by the
user of the libpulse API:

- `pa_context_rttime_new()`
- `pa_stream_write()`
- `pa_stream_write_ext_free()`

.. _`pa_context_connect() pulse documentation`:
   https://freedesktop.org/software/pulseaudio/doxygen/context_8h.html#a983ce13d45c5f4b0db8e1a34e21f9fce
