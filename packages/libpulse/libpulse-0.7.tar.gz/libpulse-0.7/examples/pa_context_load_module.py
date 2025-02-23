"""Example using LibPulse async methods.

The 'LoadModule' async context manager is used to ensure that the module is
unloaded before exiting.

A null-sink is created by loading the 'module-null-sink' module and
different async methods are used to get the 'pa_sink_info' structure of the
newly created null-sink.

Note the restrictions in the naming of the null-sink and of its description (see
the comments).

"""

import sys
import asyncio
from libpulse.libpulse import (LibPulse, PA_INVALID_INDEX,
                               pa_context_load_module,
                               pa_context_unload_module,
                               pa_context_get_sink_info_by_name,
                               pa_context_get_sink_info_by_index,
                               pa_context_get_sink_info_list,
                               )

# NOTE: Space characters are NOT ALLOWED in the sink name.
SINK_NAME = 'my-null-sink'

# NOTE: Space characters in the value of a property MUST be escaped with a
#       backslash.
MODULE_ARG = (f'sink_name="{SINK_NAME}" '
              r'sink_properties=device.description="my\ description"')

class LoadModule:
    def __init__(self, lib_pulse, name, argument):
        self.lib_pulse = lib_pulse
        self.name = name
        self.argument = argument
        self.index = PA_INVALID_INDEX

    async def __aenter__(self):
        self.index = await self.lib_pulse.pa_context_load_module(
                                                self.name, self.argument)
        if self.index == PA_INVALID_INDEX:
            print(f'Error: cannot load module {self.name}', file=sys.stderr)
            sys.exit(1)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.index != PA_INVALID_INDEX:
            await self.lib_pulse.pa_context_unload_module(self.index)

async def main():
    async with LibPulse('my libpulse') as lib_pulse:

        # Create a null sink.
        async with LoadModule(lib_pulse, 'module-null-sink', MODULE_ARG):

            # Get the pa_sink_info structure by name.
            sink_info = (await
                    lib_pulse.pa_context_get_sink_info_by_name(SINK_NAME))

            # Get the pa_sink_info structure by index.
            index = sink_info.index
            print(f"sink '{sink_info.name}' at index {index}")
            sink_info = (await
                         lib_pulse.pa_context_get_sink_info_by_index(index))

            # 'proplist' is a dict.
            description = sink_info.proplist['device.description']
            print(f"device.description: '{description}'")

            # Get the pa_sink_info structure as element of the list.
            sink_infos = await lib_pulse.pa_context_get_sink_info_list()
            for sink_info in sink_infos:
                if sink_info.index == index:
                    print('sink_info:\n', sink_info)
                    break
            else:
                assert False, 'Cannot find our null sink in the list !'

if __name__ == '__main__':
    asyncio.run(main())
