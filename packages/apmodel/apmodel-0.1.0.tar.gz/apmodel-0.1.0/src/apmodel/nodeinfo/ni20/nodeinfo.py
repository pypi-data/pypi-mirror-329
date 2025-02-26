from typing import List, Optional, Any, Dict
from .enums import OutboundServicesEnum, InboundServicesEnum, ProtocolEnum

class Software:
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version

    @classmethod
    def from_dict(cls, data: dict):
        return cls(name=data["name"], version=data["version"])

    def to_dict(self):
        return {
            "name": self.name,
            "version": self.version
        }

class Services:
    def __init__(self, inbound: List[InboundServicesEnum], outbound: List[OutboundServicesEnum]):
        self.inbound = inbound
        self.outbound = outbound
        
    @classmethod
    def from_dict(cls, data: dict):
        inbound_services = [InboundServicesEnum(service) for service in data["inbound"]]
        outbound_services = [OutboundServicesEnum(service) for service in data["outbound"]]
        return cls(inbound=inbound_services, outbound=outbound_services)

    def to_dict(self):
        return {
            "inbound": [service.value for service in self.inbound],
            "outbound": [service.value for service in self.outbound]
        }

class Users:
    def __init__(self, total: int, active_halfyear: int, active_month: int):
        self.total = total
        self.active_halfyear = active_halfyear
        self.active_month = active_month

    @classmethod
    def from_dict(cls, data: dict):
        return cls(total=data["total"], active_halfyear=data["activeHalfyear"], active_month=data["activeMonth"])

    def to_dict(self):
        return {
            "total": self.total,
            "activeHalfyear": self.active_halfyear,
            "activeMonth": self.active_month
        }

class Usage:
    def __init__(self, users: Users, local_posts: Optional[int] = None, local_comments: Optional[int] = None):
        self.users = users
        self.local_posts = local_posts
        self.local_comments = local_comments

    @classmethod
    def from_dict(cls, data: dict):
        users = Users.from_dict(data["users"])
        local_posts = data.get("localPosts")
        local_comments = data.get("localComments")
        return cls(users=users, local_posts=local_posts, local_comments=local_comments)

    def to_dict(self):
        data: Dict[str, Any] = {
            "users": self.users.to_dict(),
        }
        if self.local_posts is not None:
            data["localPosts"] = self.local_posts
        if self.local_comments is not None:
            data["localComments"] = self.local_comments
        return data

class NodeInfo:
    def __init__(self, software: Software, protocols: List[ProtocolEnum],
                 services: Services, open_registrations: bool, usage: Usage, metadata: Optional[Dict[str, Any]] = None):
        self.version = "2.0"
        self.software = software
        self.protocols = protocols
        self.services = services
        self.open_registrations = open_registrations
        self.usage = usage
        self.metadata = metadata or {}

    @classmethod
    def from_dict(cls, data: dict):
        software = Software.from_dict(data["software"])
        protocols = [ProtocolEnum(protocol) for protocol in data["protocols"]]
        services = Services.from_dict(data["services"])
        open_registrations = data["openRegistrations"]
        usage = Usage.from_dict(data["usage"])
        metadata = data.get("metadata", {})
        return cls(software, protocols, services, open_registrations, usage, metadata)

    def to_dict(self):
        return {
            "version": self.version,
            "software": self.software.to_dict(),
            "protocols": [protocol.value for protocol in self.protocols],
            "services": self.services.to_dict(),
            "openRegistrations": self.open_registrations,
            "usage": self.usage.to_dict(),
            "metadata": self.metadata
        }