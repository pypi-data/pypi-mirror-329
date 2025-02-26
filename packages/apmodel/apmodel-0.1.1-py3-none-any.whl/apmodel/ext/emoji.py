from ..core import Object

class Emoji(Object):
    def __init__(self, **kwargs):
        kwargs["type"] = "Emoji"
        super().__init__(**kwargs)