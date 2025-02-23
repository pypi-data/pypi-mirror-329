"""Example processing pulse events.

An asyncio task is started that processes all pulse events and put them into
an asyncio queue. The main() function loads a null-sink module and processes
the events received from the queue until it receives the event signaling the
creation of the module.

"""

import asyncio
from libpulse.libpulse import (LibPulse, PA_SUBSCRIPTION_MASK_ALL,
                               pa_context_subscribe, PulseEvent,
                               )

from pa_context_load_module import LoadModule, MODULE_ARG

async def get_events(lib_pulse, evt_queue, evt_ready):
    try:

        await lib_pulse.pa_context_subscribe(PA_SUBSCRIPTION_MASK_ALL)
        iterator = lib_pulse.get_events_iterator()
        # Signal main() that we are ready and processing events.
        evt_ready.set_result(True)

        async for event in iterator:
            await evt_queue.put(event)

        # Upon receiving CancelledError, the iterator raises StopAsyncIteration
        # to end the iteration.
        print('get_events(): asyncio task has been cancelled by main().')

    except Exception as e:
        await evt_queue.put(e)

async def main():
    evt_queue = asyncio.Queue()

    async with LibPulse('my libpulse') as lib_pulse:
        evt_ready = lib_pulse.loop.create_future()
        evt_task = asyncio.create_task(get_events(lib_pulse, evt_queue,
                                                  evt_ready))
        # Wait for the task to be ready.
        await evt_ready

        # Load the 'module-null-sink' module and process all pulse events
        # until we receive the event signaling the creation of this module.
        async with LoadModule(lib_pulse, 'module-null-sink',
                                  MODULE_ARG) as loaded_module:
            while True:
                event = await evt_queue.get()
                if isinstance(event, Exception):
                    raise event

                assert isinstance(event, PulseEvent)
                print('event:', event.facility, event.type, event.index)

                if (event.facility == 'module' and event.type == 'new' and
                            event.index == loaded_module.index):
                    evt_task.cancel()
                    print('Got the event triggered by loading the module.')
                    break

asyncio.run(main())
