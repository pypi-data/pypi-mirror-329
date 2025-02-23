Modules
=======

libpulse
--------
List of the main objects defined by the libpulse module, excluding the
:ref:`libpulse-class` and :ref:`Ancillary-classes`:

- The constants that are defined by enums in the pulse headers and that are
  listed by :ref:`pulse_enums`.
- The following constants that are defined by the pulse headers as macros:

  + `PA_INVALID_INDEX`
  + `PA_VOLUME_NORM`
  + `PA_VOLUME_MUTED`
  + `PA_VOLUME_MAX`
  + `PA_VOLUME_INVALID`
  + `PA_CHANNELS_MAX`

- The ctypes foreign functions corresponding to (and having the same name as)
  the non-async pulse functions. That is, all the keys in the `signatures`
  dictionary of the :ref:`pulse_functions` module whose signature does not have
  a callback as one of its parameters.
- `CTX_STATES`, `OPERATION_STATES`, `EVENT_FACILITIES` and `EVENT_TYPES`
  dictionaries that map constant values to their symbolic names.
- `struct_ctypes` a dictionary mapping the name of each pulse structure
  defined by the pulse headers (see the :ref:`pulse_structs` module) to the
  corresponding subclass of the ctypes `Structure`_ class.

libpulse_ctypes
---------------
The libpulse_ctypes module is executed when its `PulseCTypes` class is
instantiated by the mainloop module. This occurs when the libpulse module
imports the mainloop module on startup.

The libpulse_ctypes module uses the `pulse_types`, :ref:`pulse_structs` and
:ref:`pulse_functions` modules to build the following ctypes objects:

- The ctypes foreign functions corresponding to the pulse
  functions.
- The subclasses of the ctypes `Structure`_ class corresponding to the pulse
  structures.

The libpulse_ctypes module uses the :ref:`pulse_enums` module to set variables
corresponding to the constants of the enums of the pulse library.

These four ``pulse_*`` modules are generated from the headers of the pulse
library and may be re-generated using ``gcc`` and the ``pyclibrary`` package as
explained in the :ref:`Development` section although this is not necessary, the
ABI of the pulse library being pretty much stable. Using recent versions of
Pulseaudio and Pipewire generates the same modules.

mainloop
--------
The mainloop module implements the pulse Main Loop using the asyncio event loop.

The implementation supports multiple threads with one asyncio loop per thread
using a dictionary to map the asyncio `loop` instance to the libpulse `MainLoop`
instance.

.. _pulse_enums:

pulse_enums
-----------
The `pulse_enums` dictionary holds all the pulse enum types whose values are
themselves a dictionary of the enum constant names and their values. All
constant names are different making it possible to have each defined as a
constant in the libpulse module.

.. _pulse_functions:

pulse_functions
---------------
The `pulse_functions['signatures']` dictionary holds the signatures of all the
pulse functions that are not callbacks. Async functions are those functions
whose signature has a callback as one of its parameter, the callback signature
being one of the values of the `pulse_functions['callbacks']` dictionary.

The signatures are used to build ctypes `Function prototypes`_ that are
instantiated to create the foreign functions to be used as the corresponding
non-async functions, `LibPulse` coroutines or callbacks. Foreign functions are
Python callables.

.. _pulse_structs:

pulse_structs
-------------
The `pulse_structs` dictionary holds the definitions of the pulse structures
used to build the ctypes `Structure`_ subclasses that are available in the
`struct_ctypes` dictionary which is an attribute of the libpulse module.

.. _`Structure`:
   https://docs.python.org/3/library/ctypes.html#ctypes.Structure
.. _`Function prototypes`:
   https://docs.python.org/3/library/ctypes.html#function-prototypes
