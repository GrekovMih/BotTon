# -*- encoding: utf-8 -*-
import inspect

__all__ = (
    'State',
)


class State:
    def __init__(self):
        self.type = None
        self.step = None
        self.data = {}

    @staticmethod
    def from_dict(json):
        state = State()
        if json is None:
            return state

        for name in state_field_names:
            value = json.get(name, None)

            if value is not None:
                setattr(state, name, value)

        return state

    def to_dict(self):
        result = {}

        for name in state_field_names:
            result[name] = getattr(self, name)

        return result


state_field_names = [
    name
    for name, type_ in inspect.getmembers(State())
    if not name.startswith('_') and not inspect.ismethod(type_) and not inspect.isfunction(type_)
]
