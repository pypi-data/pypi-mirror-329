from dataclasses import dataclass
from typing import Dict
from typing import List, Tuple


@dataclass
class LoginRequestSchema:
    email: str


@dataclass
class LoginResponseSchema:
    uid: str
    email: str
    master_key_encrypted: str
    public_key: str
    private_key_encrypted: str
    access_token_encrypted: str
    fernet_key_encrypted: str


@dataclass
class ListResponseSchema:
    items: list
    count: int


@dataclass
class ThingSchema:
    type_name: str
    source_uri: str
    thing_uuid: str
    uri: str
    status: str
    thing_meta_uuid: str
    meta_id: str = None
    uuid: str = None
    source_host: str = None


@dataclass
class ThingMetaSchema:
    type_name: str
    meta_id: str
    meta_info: Dict


@dataclass
class ThingWithMetaSchema:
    type_name_uri_sha256_hash: str
    type_name_source_host_source_uri_sha256_hash: str
    type_name: str
    source_uri: str
    thing_uuid: str
    uri: str
    status: str
    meta_id: str
    uuid: str
    source_host: str
    thing_meta_uuid: str
    thing_meta_info: dict


@dataclass
class SearchThingRequestSchema:
    keywords: list[str]

    type_name: str = None
    source_host: str = None


@dataclass
class SearchThingResponseSchema(ListResponseSchema):
    items: list[ThingSchema]

    def __post_init__(self):
        self.items = [ThingSchema(**_e) for _e in self.items]


@dataclass
class RequestThingSourceMetaSchema:
    type_name: str
    source_host: str
    source_uri: str


"""
Request Thing
"""

@dataclass
class RequestThingRequestSchema:
    type_name: str
    source_protocol: str
    source_host: str
    source_uri: str


@dataclass
class RequestThingResponseSchema:
    thing_uuid: str
    task_uuid: str


"""
Download Thing
"""


@dataclass
class DownloadThingRequestSchema:
    thing_uuid: str


@dataclass
class ResourceSchema:
    uuid: str
    size: int
    sha256_hash: str
    sha256_hash_storage: str
    url: str
    pieces_num: int
    pieces_urls: List[str]


@dataclass
class DownloadThingResponseSchema:
    thing_uuid: str
    thing_status: str
    type_name: str
    source_host: str
    source_uri: str
    uri: str
    resources: Dict
    status: str


@dataclass
class UserSyncDeviceHeartbeatRequestSchema:
    public_key: str
    addrs: List[Tuple[str, str]]
    derp_region: int


@dataclass
class UserSyncDeviceHeartbeatResponseSchema:
    pass

"""
User Query Device
"""

@dataclass
class UserQueryDeviceRequestSchema:
    public_key: str


@dataclass
class UserQueryDeviceResponseSchema:
    public_key: str
    addrs: List[Tuple[str, str]]
    derp_region: int


"""Sync Thing To Sbc"""


@dataclass
class SyncThingToSbcRequestSchema:
    thing: ThingSchema
    thing_meta: ThingMetaSchema


@dataclass
class SyncThingToSbcResponseSchema:
    pass
