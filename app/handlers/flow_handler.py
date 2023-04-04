# -*- encoding: utf-8 -*-
from app.handlers.help import send_help_message

__all__ = (
    'FlowHandler',
    'FlowHandlerStep',
)


class FlowHandlerStep:
    async def before(self, context):
        pass

    async def ignore(self, context):
        return False

    async def handle(self, context):
        pass


class FlowHandler:
    FLOWS = {}

    def __init__(self, type_, steps):
        assert type_ not in FlowHandler.FLOWS
        FlowHandler.FLOWS[type_] = self

        self.type = type_
        self.steps = [step() for step in steps]

        for step in steps:
            assert issubclass(step, FlowHandlerStep)

    async def start(self, context, prepare=None):
        await context.start_flow(self)

        if prepare is not None:
            await prepare(context)

        await self.steps[0].before(context)

    async def handle(self, context):
        step = context.state.step

        if len(self.steps) > step:
            res = await self.steps[step].handle(context)

            if res is True:
                if len(self.steps) - 1 == step:
                    await context.clear_state()
                else:
                    next_step = step + 1

                    while next_step < len(self.steps):
                        ignore_step = await self.steps[next_step].ignore(context)

                        if ignore_step is True:
                            next_step += 1
                        else:
                            break

                    if next_step >= len(self.steps):  # last step
                        await context.clear_state()
                    else:
                        context.state.step = next_step
                        await self.steps[next_step].before(context)

        else:
            await context.send_message('I have missed the state, restarting')
            await context.clear_state()
            await send_help_message(context)
