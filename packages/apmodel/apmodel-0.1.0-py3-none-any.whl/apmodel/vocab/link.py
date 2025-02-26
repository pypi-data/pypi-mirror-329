from ..core import Link

class Mention(Link):
    def __init__(self, **kwargs):
        super().__init__(type="Mention", **kwargs)

class Hashtag(Link):
    def __init__(self, **kwargs):
        super().__init__(type="Hashtag", **kwargs)