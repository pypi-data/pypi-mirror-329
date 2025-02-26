from ..core import Activity

class Accept(Activity):
    def __init__(self, **kwargs):
        super().__init__("Accept", **kwargs)


class Reject(Activity):
    def __init__(self, **kwargs):
        super().__init__("Reject", **kwargs)


class TentativeReject(Activity):
    def __init__(self, **kwargs):
        super().__init__("TentativeReject", **kwargs)


class Remove(Activity):
    def __init__(self, **kwargs):
        super().__init__("Remove", **kwargs)


class Undo(Activity):
    def __init__(self, **kwargs):
        super().__init__("Undo", **kwargs)


class Create(Activity):
    def __init__(self, **kwargs):
        del kwargs["type"]
        super().__init__("Create", **kwargs)


class Delete(Activity):
    def __init__(self, **kwargs):
        super().__init__("Delete", **kwargs)


class Update(Activity):
    def __init__(self, **kwargs):
        super().__init__("Update", **kwargs)


class Follow(Activity):
    def __init__(self, **kwargs):
        super().__init__("Follow", **kwargs)


class View(Activity):
    def __init__(self, **kwargs):
        super().__init__("View", **kwargs)


class Listen(Activity):
    def __init__(self, **kwargs):
        super().__init__("Listen", **kwargs)


class Read(Activity):
    def __init__(self, **kwargs):
        super().__init__("Read", **kwargs)


class Move(Activity):
    def __init__(self, **kwargs):
        super().__init__("Move", **kwargs)


class Travel(Activity):
    def __init__(self, **kwargs):
        super().__init__("Travel", **kwargs)


class Announce(Activity):
    def __init__(self, **kwargs):
        super().__init__("Announce", **kwargs)


class Block(Activity):
    def __init__(self, **kwargs):
        super().__init__("Block", **kwargs)


class Flag(Activity):
    def __init__(self, **kwargs):
        super().__init__("Flag", **kwargs)

class Like(Activity):
    def __init__(self, **kwargs):
        super().__init__("Like", **kwargs)

class Dislike(Activity):
    def __init__(self, **kwargs):
        super().__init__("Dislike", **kwargs)

class IntransitiveActivity(Activity):
    def __init__(
        self,
        actor=None,
        target=None,
        result=None,
        origin=None,
        instrument=None,
        **kwargs,
    ):
        super().__init__(
            "IntransitiveActivity", actor, target, result, origin, instrument, **kwargs
        )


class Question(IntransitiveActivity):
    def __init__(self, **kwargs):
        super().__init__("Question", **kwargs)