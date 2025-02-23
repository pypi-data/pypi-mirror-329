.. _`Ancillary-classes`:

Ancillary classes
=================

Exceptions
----------
- `LibPulseError(Exception)`
- `LibPulseClosedError(LibPulseError)`
- `LibPulseStateError(LibPulseError)`
- `LibPulseOperationError(LibPulseError)`
- `LibPulseClosedIteratorError(LibPulseError)`
- `LibPulseInstanceExistsError(LibPulseError)`
- `LibPulseArgumentError(LibPulseError)`

PulseEvent
----------
An instance of `PulseEvent` is returned by the async iterator returned by the
:ref:`get_events_iterator` method of a LibPulse instance.

Its attributes are:

- `facility`
    `str` - name of the facility, for example ``sink``.
- `index`
    `int` - index of the facility.
- `type`
    `str` - type of the event, either ``new``, ``change`` or ``remove``.

.. _`PulseStructure`:

PulseStructure
--------------
`class PulseStructure(c_struct, c_structure_type)`

- `c_struct`
    ctypes structure such as a ctypes pointer dereferenced using its
    `contents` attribute.
- `c_structure_type`
    subclass of ctypes `Structure`_ corresponding to the type of the `c_struct`
    structure. It is one of the values of the structures defined in the
    `struct_ctypes` dictionary, attribute of the libpulse module.

An instance of this class is the representation of a pulse ctypes structure.

Instantiating a `PulseStructure` class constructs a pure Python object as a deep
copy of a ctypes structure using the `_fields_` class attribute of the
corresponding subclass of the ctypes `Structure`_ class (one of the values of
the `struct_ctypes` dictionary, see the :ref:`pulse_structs` module and
the :ref:`ctypes-pulse-structures` section).

A deep copy of the pulse structure pointed to by one of the parameters of a
callback (one of the results of the corresponding `LibPulse` method) is
needed because the memory pointed to by the pointer is short-lived, only valid
during the execution of the callback.

The `PulseStructure` instance embeds `PulseStructure` instances for those of its
members that are nested pulse structures or pointers to other pulse structures
(recursively). The attributes names of the PulseStructure instance are the names
of the members of the pulse structure as listed in the :ref:`pulse_structs`
module. Their values are of type `int`, `float`, `bytes`, :ref:`PropList` or
`PulseStructure`.

This class is used internally by callbacks of the `LibPulse` class and by the
`to_pulse_structure()` method of the :ref:`CtypesPulseStructure`
class.

.. _`PropList`:

PropList
--------
When the type of the member of a pulse structure is `proplist *`, the
corresponding `PulseStructure` attribute is set to an instance of the `PropList`
class.

The `PropList` class is a subclass of `dict` and the elements of an instance can
be accessed as the elements of a dictionary. Instantiation of this class skips
all the elements of the proplist that are not of the `bytes` type. The keys and
values of the dictionary are strings (`bytes` are decoded to `str`).

.. _AsyncioTasks:

AsyncioTasks
------------
An instance of `AsyncioTasks` keeps track of the active asyncio tasks that have
been created using its `create_task()` method. It is also an iterator that can
iterate over these tasks. See the :ref:`session-management` section for how to
use it.

.. _CtypesPulseStructure:

CtypesPulseStructure
--------------------
An abstract class whose subclasses provide the reverse of what does the
`PulseStructure` class by building a ctypes structure whose pointer can be used
as the parameter of one of the pulse functions. Those subclasses are:

- `Pa_buffer_attr`
- `Pa_cvolume`
- `Pa_channel_map`
- `Pa_format_info`
- `Pa_sample_spec`

Instantiate one of these subclasses with a list of the pulse structure values
and use `byref()` to get the pointer. For example:

.. code-block:: python

   values = [3, 44100, 2]
   ptr = libpulse.Pa_sample_spec(*values).byref()

See also :ref:`ctypes-pulse-structures`.

.. _`Structure`:
   https://docs.python.org/3/library/ctypes.html#ctypes.Structure
