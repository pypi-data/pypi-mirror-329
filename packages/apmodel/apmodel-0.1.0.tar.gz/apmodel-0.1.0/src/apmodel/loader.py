from typing import Any

from .core import Activity, Link, Object
from .vocab.link import Mention
from .vocab.document import Document, Page, Audio, Image, Video
from .vocab.object import Profile, Tombstone, Collection, Person, Note
from .vocab.activity import Accept, Reject, TentativeReject, Remove, Undo, Create, Delete, Update, Follow, View, Listen, Read, Move, Travel, Announce, Block, Flag, Like, Dislike, IntransitiveActivity, Question

# For Federation
from .security.cryptographickey import CryptographicKey
from .schema.propertyvalue import PropertyValue
from .ext.emoji import Emoji
from .vocab.link import Hashtag

base_mapper = {
    "Object": Object,
    "Activity": Activity,
    "Link": Link,
    "Mention": Mention,
    "Accept": Accept,
    "Reject": Reject,
    "TentativeReject": TentativeReject,
    "Remove": Remove,
    "Undo": Undo,
    "Create": Create,
    "Delete": Delete,
    "Update": Update,
    "Follow": Follow,
    "View": View,
    "Listen": Listen,
    "Read": Read,
    "Move": Move,
    "Travel": Travel,
    "Announce": Announce,
    "Block": Block,
    "Flag": Flag,
    "Like": Like,
    "Dislike": Dislike,
    "IntransitiveActivity": IntransitiveActivity,
    "Question": Question,
    "Document": Document,
    "Page": Page,
    "Audio": Audio,
    "Image": Image,
    "Video": Video,
    "Profile": Profile,
    "Tombstone": Tombstone,
    "Collection": Collection,
    "Person": Person,
    "Note": Note
}

fedi_mapper = {
    **base_mapper,
    "CryptographicKey": CryptographicKey,
    "Key": CryptographicKey,
    "PropertyValue": PropertyValue,
    "Emoji": Emoji,
    "Hashtag": Hashtag
}

class StreamsLoader:
    @staticmethod
    def load(object: dict[Any, Any], custom_mapper: dict = fedi_mapper) -> Object | Link | dict: # type: ignore
        type = object.get("type")
        cls = custom_mapper.get(type)
        if cls:
            return cls(**object)
        return object