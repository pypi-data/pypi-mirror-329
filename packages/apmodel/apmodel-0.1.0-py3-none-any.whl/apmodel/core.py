# from datetime import datetime
import re
import uuid
from typing import TYPE_CHECKING, Union, Optional, Dict, Any, List

from pyfill import datetime

if TYPE_CHECKING:
    from .vocab.document import Image
    from .vocab.object import Collection


def merge_contexts(
    urls: Union[str, List[Union[str, Dict[str, Any]]]],
    additional_data: Union[str, List[Union[str, Dict[str, Any]]]],
) -> List[Union[str, Dict[str, Any]]]:
    result = []
    merged_dict = {}

    if isinstance(urls, str):
        result.append(urls)
    else:
        for item in urls:
            if isinstance(item, dict):
                merged_dict.update(item)
            else:
                result.append(item)

    if isinstance(additional_data, str):
        result.append(additional_data)
    else:
        for item in additional_data:
            if isinstance(item, dict):
                merged_dict.update(item)
            else:
                result.append(item)

    result.append(merged_dict)

    return result


class Object:
    def __init__(
        self,
        _context: Union[str, list] = "https://www.w3.org/ns/activitystreams",
        type: str = "Object",
        id: Optional[str] = None,
        attachment: Optional[Union["Object", "Link", dict]] = None,
        attributedTo: Optional[Union["Object", "Link"]] = None,
        audience: Optional[Union["Object", "Link"]] = None,
        content: Optional[str] = None,
        context: Optional[Union["Object", "Link"]] = None,
        name: Optional[str] = None,
        endTime: Optional[str] = None,
        generator: Optional[Union["Object", "Link"]] = None,
        icon: Optional[Union["Image", "Link"]] = None,
        image: Optional["Image"] = None,
        inReplyTo: Optional[Union["Image", "Link"]] = None,
        location: Optional[Union["Image", "Link"]] = None,
        preview: Optional[Union["Object", "Link"]] = None,
        published: Optional[str] = None,
        replies: Optional["Collection"] = None,
        startTime: Optional[str] = None,
        summary: Optional[str] = None,
        tag: Optional[Union["Object", "Link"]] = None,
        updated: Optional[str] = None,
        url: Optional[Union[str, "Link"]] = None,
        to: Optional[Union["Object", "Link"]] = None,
        bto: Optional[Union["Object", "Link"]] = None,
        cc: Optional[Union["Object", "Link"]] = None,
        bcc: Optional[Union["Object", "Link"]] = None,
        mediaType: Optional[str] = None,
        duration: Optional[str] = None,
        sensitive: Optional[bool] = None,
        **kwargs,
    ):
        from .loader import StreamsLoader

        ctx = kwargs.get("@context")
        self._context = merge_contexts(_context, ctx) if ctx else []
        self.type = type
        self.id = id
        self.attachment = (
            StreamsLoader.load(attachment)
            if isinstance(attachment, dict)
            else attachment
        )
        self.attributedTo = (
            StreamsLoader.load(attributedTo)
            if isinstance(attributedTo, dict)
            else attributedTo
        )
        self.audience = (
            StreamsLoader.load(audience) if isinstance(audience, dict) else audience
        )
        self.content = content
        self.context = (
            StreamsLoader.load(context) if isinstance(context, dict) else context
        )
        self.name = name
        self.endTime = (
            (
                endTime
                if isinstance(endTime, datetime.datetime.datetime)
                else datetime.datetime.datetime.strptime(
                    endTime, "%Y-%m-%dT%H:%M:%S.%fZ"
                )
            )
            if endTime
            else endTime
        )
        self.generator = (
            StreamsLoader.load(generator) if isinstance(generator, dict) else generator
        )
        self.icon = StreamsLoader.load(icon) if isinstance(icon, dict) else icon
        self.image = image
        self.inReplyTo = (
            StreamsLoader.load(inReplyTo) if isinstance(inReplyTo, dict) else inReplyTo
        )
        self.location = (
            StreamsLoader.load(location) if isinstance(location, dict) else location
        )
        self.preview = (
            StreamsLoader.load(preview) if isinstance(preview, dict) else preview
        )
        self.published = (
            (
                published
                if isinstance(published, datetime.datetime.datetime)
                else datetime.datetime.datetime.strptime(
                    published, "%Y-%m-%dT%H:%M:%S.%fZ"
                )
            )
            if published
            else published
        )
        self.replies = (
            StreamsLoader.load(replies) if isinstance(replies, dict) else replies
        )
        self.startTime = (
            (
                startTime
                if isinstance(startTime, datetime.datetime.datetime)
                else datetime.datetime.datetime.strptime(
                    startTime, "%Y-%m-%dT%H:%M:%S.%fZ"
                )
            )
            if startTime
            else startTime
        )
        self.summary = summary
        self.tag = StreamsLoader.load(tag) if isinstance(tag, dict) else tag
        self.updated = updated
        self.url = StreamsLoader.load(url) if isinstance(url, dict) else url
        self.to = StreamsLoader.load(to) if isinstance(to, dict) else to
        self.bto = StreamsLoader.load(bto) if isinstance(bto, dict) else bto
        self.cc = StreamsLoader.load(cc) if isinstance(cc, dict) else cc
        self.bcc = StreamsLoader.load(bcc) if isinstance(bcc, dict) else bcc
        self.mediaType = mediaType
        self.duration = duration

        # --- Extend Value
        self.sensitive = sensitive
        # ---

        self._extras = {}
        for key, value in kwargs.items():
            self._extras[key] = value

    def to_dict(self, _extras: Optional[dict] = None, build_context: bool = True):
        if not _extras:
            _extras = self._extras.copy()
        instance_vars = vars(self).copy()

        ctx = self._context.copy()
        if build_context:
            attrs = dir(self)

            ctx2 = []
            ctx2_d = {}
            if _extras.get("publicKey") or "publicKey" in attrs:
                ctx2.append("https://w3id.org/security/v1")

            # Mastodon
            if _extras.get("featured") or "featured" in attrs:
                ctx2_d["featured"] = {
                    "@id": "http://joinmastodon.org/ns#featured",
                    "@type": "@id",
                }
            if _extras.get("featuredTags") or "featuredTags" in attrs:
                ctx2_d["featuredTags"] = {
                    "@id": "http://joinmastodon.org/ns#featuredTags",
                    "@type": "@id",
                }
            if _extras.get("discoverable") or "discoverable" in attrs:
                if not ctx2_d.get("toot"):
                    ctx2_d["toot"] = "http://joinmastodon.org/ns#"
                ctx2_d["discoverable"] = "toot:discoverable"
            if _extras.get("discoverable") or "discoverable" in attrs:
                if not ctx2_d.get("toot"):
                    ctx2_d["toot"] = "http://joinmastodon.org/ns#"
                ctx2_d["discoverable"] = "toot:discoverable"
            if _extras.get("manuallyApprovesFollowers") or "manuallyApprovesFollowers" in attrs:
                ctx2_d["manuallyApprovesFollowers"] = "as:manuallyApprovesFollowers"

            # Misskey
            if (
                _extras.get("_misskey_content")
                or _extras.get("_misskey_summary")
                or _extras.get("_misskey_quote")
                or _extras.get("_misskey_reaction")
                or _extras.get("_misskey_votes")
                or _extras.get("_misskey_talk")
                or _extras.get("isCat")
                or _extras.get("_misskey_followedMessage")
                or _extras.get("_misskey_requireSigninToViewContents")
                or _extras.get("_misskey_makeNotesFollowersOnlyBefore")
                or _extras.get("_misskey_makeNotesHiddenBefore")
                or _extras.get("_misskey_license")
            ):
                ctx2_d["misskey"] = "https://misskey-hub-net/ns#"

            ctx2.append(ctx2_d)

        context: Optional[list] = instance_vars.get("@context")
        if context:
            context = merge_contexts(merge_contexts(ctx, context), ctx2)
        else:
            context = ctx
        data: Dict[str, Any] = {
            "@context": context,
        }

        if self.content is not None:
            data["content"] = self.content

        for key, value in instance_vars.items():
            if value is not None:
                if not key.startswith("_") and key != "content":
                    if isinstance(value, datetime.datetime.datetime):
                        data[key] = value.isoformat() + "Z"
                    elif isinstance(value, Object):
                        data[key] = value.to_dict(_extras=value._extras)
                    elif isinstance(value, list):
                        data[key] = [
                            item.to_dict(_extras=item._extras)
                            if hasattr(item, "to_dict")
                            else item
                            for item in value
                        ]
                    elif (
                        isinstance(value, dict)
                        or isinstance(value, int)
                        or isinstance(value, bool)
                    ):
                        data[key] = value
                    else:
                        data[key] = str(value)

        _extras = _extras or {}
        for key, value in self._extras.items():
            if value is not None:
                if isinstance(value, datetime.datetime.datetime):
                    data[key] = value.isoformat() + "Z"
                elif isinstance(value, Object):
                    data[key] = value.to_dict(_extras=value._extras)
                elif isinstance(value, list):
                    data[key] = [
                        item.to_dict(_extras=item._extras)
                        if hasattr(item, "to_dict")
                        else item
                        for item in value
                    ]
                elif (
                    isinstance(value, dict)
                    or isinstance(value, int)
                    or isinstance(value, bool)
                ):
                    data[key] = value
                else:
                    data[key] = str(value)
        return data


class Link:
    def __init__(
        self,
        _context: Union[str, list] = "https://www.w3.org/ns/activitystreams",
        type: str = "Link",
        id: Optional[str] = None,
        href: Optional[str] = None,
        rel: Optional[list[str]] = None,
        mediaType: Optional[str] = None,
        name: Optional[str] = None,
        hreflang: Optional[str] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
        preview: Optional[Union[Object, "Link"]] = None,
        **kwargs,
    ):
        if href:
            if not re.fullmatch(r"(%(?![0-9A-F]{2})|#.*#)", href):
                raise ValueError("href must be xsd:anyURI")
        if height:
            if height < 0:
                raise ValueError("height must be greater than or equal to 0")
        if width:
            if width < 0:
                raise ValueError("width must be greater than or equal to 0")
        ctx = kwargs.get("@context")
        self._context = merge_contexts(_context, ctx) if ctx else []
        self.type = type
        self.id = id
        self.href = href
        self.rel = rel
        self.media_type = mediaType
        self.name = name
        self.hreflang = hreflang
        self.height = height
        self.preview = preview
        self._extras = {}
        for key, value in kwargs.items():
            self._extras[key] = value

    def to_dict(self, _extras: Optional[dict] = None, build_context: bool = False):
        if not _extras:
            _extras = self._extras.copy()
        instance_vars = vars(self).copy()

        ctx = self._context.copy()
        context = instance_vars.get("@context")

        if build_context:
            attrs = dir(self)

            ctx2 = []
            ctx2_d = {}
            if _extras.get("publicKey") or "publicKey" in attrs:
                ctx2.append("https://w3id.org/security/v1")

            # Mastodon
            if _extras.get("featured") or "featured" in attrs:
                ctx2_d["featured"] = {
                    "@id": "http://joinmastodon.org/ns#featured",
                    "@type": "@id",
                }
            if _extras.get("featuredTags") or "featuredTags" in attrs:
                ctx2_d["featuredTags"] = {
                    "@id": "http://joinmastodon.org/ns#featuredTags",
                    "@type": "@id",
                }
            if _extras.get("discoverable") or "discoverable" in attrs:
                if not ctx2_d.get("toot"):
                    ctx2_d["toot"] = "http://joinmastodon.org/ns#"
                ctx2_d["discoverable"] = "toot:discoverable"
            if _extras.get("discoverable") or "discoverable" in attrs:
                if not ctx2_d.get("toot"):
                    ctx2_d["toot"] = "http://joinmastodon.org/ns#"
                ctx2_d["discoverable"] = "toot:discoverable"
            if _extras.get("manuallyApprovesFollowers") or "manuallyApprovesFollowers" in attrs:
                ctx2_d["manuallyApprovesFollowers"] = "as:manuallyApprovesFollowers"

            # Misskey
            if (
                _extras.get("_misskey_content")
                or _extras.get("_misskey_summary")
                or _extras.get("_misskey_quote")
                or _extras.get("_misskey_reaction")
                or _extras.get("_misskey_votes")
                or _extras.get("_misskey_talk")
                or _extras.get("isCat")
                or _extras.get("_misskey_followedMessage")
                or _extras.get("_misskey_requireSigninToViewContents")
                or _extras.get("_misskey_makeNotesFollowersOnlyBefore")
                or _extras.get("_misskey_makeNotesHiddenBefore")
                or _extras.get("_misskey_license")
            ):
                if not ctx2_d.get("misskey"):
                    ctx2_d["misskey"] = "https://misskey-hub-net/ns#"

            ctx2.append(ctx2_d)
        if context:
            context = merge_contexts(merge_contexts(ctx, context), ctx2)
        else:
            context = ctx
        data: Dict[str, Any] = {
            "@context": context,
        }
        for key, value in instance_vars.items():
            if value is not None:
                if not key.startswith("_") and key != "content":
                    if isinstance(value, datetime.datetime.datetime):
                        data[key] = value.isoformat() + "Z"
                    elif isinstance(value, Object):
                        data[key] = value.to_dict(_extras=value._extras)
                    elif isinstance(value, list):
                        data[key] = [
                            item.to_dict(_extras=item._extras)
                            if hasattr(item, "to_dict")
                            else item
                            for item in value
                        ]
                    elif (
                        isinstance(value, dict)
                        or isinstance(value, int)
                        or isinstance(value, bool)
                    ):
                        data[key] = value
                    else:
                        data[key] = str(value)

        _extras = _extras or {}
        for key, value in self._extras.items():
            if value is not None:
                if isinstance(value, datetime.datetime.datetime):
                    data[key] = value.isoformat() + "Z"
                elif isinstance(value, Object):
                    data[key] = value.to_dict(_extras=value._extras)
                elif isinstance(value, list):
                    data[key] = [
                        item.to_dict(_extras=item._extras)
                        if hasattr(item, "to_dict")
                        else item
                        for item in value
                    ]
                elif (
                    isinstance(value, dict)
                    or isinstance(value, int)
                    or isinstance(value, bool)
                ):
                    data[key] = value
                else:
                    data[key] = str(value)
        return data


class Activity(Object):
    def __init__(
        self,
        type: str = "Activity",
        id: Optional[str] = None,
        actor: Optional[Union[Object, Link, str, dict]] = None,
        object: Optional[Union[Object, dict]] = None,
        target: Optional[Union[Object, Link]] = None,
        result: Optional[Union[Object, Link]] = None,
        origin: Optional[Union[Object, Link]] = None,
        instrument: Optional[Union[Object, Link]] = None,
        **kwargs,
    ):
        from .loader import StreamsLoader

        super().__init__(type="Activity", content=None)
        self.type = type
        self.id = id if id else str(uuid.uuid4())
        self.published = datetime.utcnow().isoformat() + "Z"
        self.actor = StreamsLoader.load(actor) if isinstance(actor, dict) else actor
        self.object = StreamsLoader.load(object) if isinstance(object, dict) else object
        self.target = target
        self.result = result
        self.origin = origin
        self.instrument = instrument
        self._extras = {}
        for key, value in kwargs.items():
            self._extras[key] = value

    def to_dict(self):
        data = super().to_dict()

        if self.type:
            data["type"] = self.type
        if self.actor:
            data["actor"] = (
                self.actor.to_dict()
                if isinstance(self.actor, Object)
                else str(self.actor)
            )
        if self.object:
            data["object"] = (
                self.object.to_dict()
                if isinstance(self.object, Object)
                else str(self.object)
            )
        if self.target:
            data["target"] = (
                self.target.to_dict()
                if isinstance(self.target, Object)
                else str(self.target)
            )

        return data
