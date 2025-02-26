from typing import Optional, Union

from ..core import Object
from ..security.cryptographickey import CryptographicKey

class Note(Object):
    def __init__(self, _misskey_quote: Optional[str] = None, quoteUrl: Optional[str] = None, **kwargs):
        kwargs["type"] = "Note"
        super().__init__(**kwargs)
        self._misskey_quote = _misskey_quote
        self.quoteUrl = quoteUrl

class Profile(Object):
    def __init__(self, describes: Optional[Object | dict] = None, **kwargs):
        from ..loader import StreamsLoader
        kwargs["type"] = "Profile"
        super().__init__(**kwargs)
        self.describes = StreamsLoader.load(describes) if isinstance(describes, dict) else describes

class Tombstone(Object):
    def __init__(self, formerType=None, deleted=None, **kwargs):
        kwargs["type"] = "Tombstone"
        super().__init__(**kwargs)
        self.deleted = deleted
        self.formerType = formerType


class Collection(Object):
    def __init__(
        self, items=None, totalItems=None, first=None, last=None, current=None, **kwargs
    ):
        kwargs["type"] = "Collection"
        super().__init__(**kwargs)
        self.items = items
        self.totalItems = totalItems
        self.first = first
        self.last = last
        self.current = current


class Person(Object):
    def __init__(self, name=None, url=None, inbox=None, outbox=None, sharedInbox=None, publicKey: Optional[dict] = None, discoverable: Optional[bool] = None, suspended: Optional[bool] = None, **kwargs):
        from ..loader import StreamsLoader
        kwargs["type"] = "Person"
        super().__init__(content=None, **kwargs)
        self.name = name
        self.url = url
        self.inbox = inbox or f"{url}/inbox" if url else None
        self.outbox = outbox or f"{url}/outbox" if url else None
        self.sharedInbox = sharedInbox or f"{url}/inbox" if url else None

        # extensional types
        self.publicKey: CryptographicKey = StreamsLoader.load(publicKey) if isinstance(publicKey, dict) else publicKey # type: ignore
        self.discoverable = discoverable
        self.suspended = suspended

    def to_dict(self):
        data = super().to_dict()

        if self.name:
            data["name"] = self.name
        if self.url:
            data["url"] = self.url
        if self.inbox:
            data["inbox"] = self.inbox
        if self.outbox:
            data["outbox"] = self.outbox

        return data
    
class Group(Object):
    def __init__(self, name=None, url=None, inbox=None, outbox=None, sharedInbox=None, publicKey: Optional[dict] = None, discoverable: Optional[bool] = None, suspended: Optional[bool] = None, **kwargs):
        from ..loader import StreamsLoader
        kwargs["type"] = "Group"
        super().__init__(content=None, **kwargs)
        self.name = name
        self.url = url
        self.inbox = inbox or f"{url}/inbox" if url else None
        self.outbox = outbox or f"{url}/outbox" if url else None
        self.sharedInbox = sharedInbox or f"{url}/inbox" if url else None

        # extensional types
        self.publicKey: CryptographicKey = StreamsLoader.load(publicKey) if isinstance(publicKey, dict) else publicKey # type: ignore
        self.discoverable = discoverable
        self.suspended = suspended

    def to_dict(self):
        data = super().to_dict()

        if self.name:
            data["name"] = self.name
        if self.url:
            data["url"] = self.url
        if self.inbox:
            data["inbox"] = self.inbox
        if self.outbox:
            data["outbox"] = self.outbox

        return data
    
class Application(Object):
    def __init__(self, name=None, url=None, inbox=None, outbox=None, sharedInbox=None, publicKey: Optional[dict] = None, discoverable: Optional[bool] = None, suspended: Optional[bool] = None, **kwargs):
        from ..loader import StreamsLoader
        kwargs["type"] = "Application"
        super().__init__(content=None, **kwargs)
        self.name = name
        self.url = url
        self.inbox = inbox or f"{url}/inbox" if url else None
        self.outbox = outbox or f"{url}/outbox" if url else None
        self.sharedInbox = sharedInbox or f"{url}/inbox" if url else None

        # extensional types
        self.publicKey: CryptographicKey = StreamsLoader.load(publicKey) if isinstance(publicKey, dict) else publicKey # type: ignore
        self.discoverable = discoverable
        self.suspended = suspended

    def to_dict(self):
        data = super().to_dict()

        if self.name:
            data["name"] = self.name
        if self.url:
            data["url"] = self.url
        if self.inbox:
            data["inbox"] = self.inbox
        if self.outbox:
            data["outbox"] = self.outbox

        return data
    
class Service(Object):
    def __init__(self, name=None, url=None, inbox=None, outbox=None, sharedInbox=None, publicKey: Optional[dict] = None, discoverable: Optional[bool] = None, suspended: Optional[bool] = None, **kwargs):
        from ..loader import StreamsLoader
        kwargs["type"] = "Service"
        super().__init__(content=None, **kwargs)
        self.name = name
        self.url = url
        self.inbox = inbox or f"{url}/inbox" if url else None
        self.outbox = outbox or f"{url}/outbox" if url else None
        self.sharedInbox = sharedInbox or f"{url}/inbox" if url else None

        # extensional types
        self.publicKey: CryptographicKey = StreamsLoader.load(publicKey) if isinstance(publicKey, dict) else publicKey # type: ignore
        self.discoverable = discoverable
        self.suspended = suspended

    def to_dict(self):
        data = super().to_dict()

        if self.name:
            data["name"] = self.name
        if self.url:
            data["url"] = self.url
        if self.inbox:
            data["inbox"] = self.inbox
        if self.outbox:
            data["outbox"] = self.outbox

        return data
    
class Organization(Object):
    def __init__(self, name=None, url=None, inbox=None, outbox=None, sharedInbox=None, publicKey: Optional[dict] = None, discoverable: Optional[bool] = None, suspended: Optional[bool] = None, **kwargs):
        from ..loader import StreamsLoader
        kwargs["type"] = "Organization"
        super().__init__(content=None, **kwargs)
        self.name = name
        self.url = url
        self.inbox = inbox or f"{url}/inbox" if url else None
        self.outbox = outbox or f"{url}/outbox" if url else None
        self.sharedInbox = sharedInbox or f"{url}/inbox" if url else None

        # extensional types
        self.publicKey: CryptographicKey = StreamsLoader.load(publicKey) if isinstance(publicKey, dict) else publicKey # type: ignore
        self.discoverable = discoverable
        self.suspended = suspended

    def to_dict(self):
        data = super().to_dict()

        if self.name:
            data["name"] = self.name
        if self.url:
            data["url"] = self.url
        if self.inbox:
            data["inbox"] = self.inbox
        if self.outbox:
            data["outbox"] = self.outbox

        return data

Actor = Union[Application,Group,Organization,Person,Service]