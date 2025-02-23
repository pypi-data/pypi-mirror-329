"""Example using ctypes pulse structures.

  1) Two structures are built from scratch using their ctypes types.
  2) pa_stream_new() is called using pointers to these structures and returns
     an opaque pointer.
  3) pa_stream_get_sample_spec() returns a ctypes pointer that is used to
     build a PulseStructure instance. The type of a PulseStructure instance is
     a mapping type and printing its content shows that it matches the content
     of the pa_sample_spec structure used to create the stream.

Note:
-----
pa_stream_get_sample_spec() is a plain function (not a coroutine method of the
LibPulse instance) and the PulseStructure instantiation must be done
manually. This is not needed for the methods of the LibPulse instance whose
async functions return a structure or a list of structures.

"""

import sys
import asyncio
import ctypes as ct
from libpulse.libpulse import (LibPulse, PulseStructure, struct_ctypes,
                               pa_stream_new, pa_stream_unref,
                               pa_stream_get_sample_spec,
                               Pa_sample_spec, Pa_channel_map,
                               )

async def main():
    async with LibPulse('my libpulse') as lib_pulse:
        # Build the pa_sample_spec structure.
        sample_spec = Pa_sample_spec(3, 44100, 2)

        # Build the pa_channel_map structure.
        channel_map = Pa_channel_map(2, [1, 2])

        # Create the stream.
        ct_pa_stream = pa_stream_new(lib_pulse.c_context, b'some name',
                                     sample_spec.byref(),
                                     channel_map.byref())

        # From the ctypes documentation: "NULL pointers have a False
        # boolean value".
        if not ct_pa_stream:
            print('Error: cannot create a new stream', file=sys.stderr)
            sys.exit(1)

        try:
            # Get the pa_sample_spec structure as a PulseStructure instance.
            ct_sample_spec = pa_stream_get_sample_spec(ct_pa_stream)
            sample_spec = PulseStructure(ct_sample_spec.contents,
                                         struct_ctypes['pa_sample_spec'])

            # Print the attributes of sample_spec.
            # This will print:
            #   {'format': 3, 'rate': 44100, 'channels': 2}
            print(sample_spec.__dict__)
        finally:
            pa_stream_unref(ct_pa_stream)

asyncio.run(main())
