from ._version import version as __version__
try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

from imaging_server_kit.client import Client
from imaging_server_kit.server import Server, Parameters
from imaging_server_kit.registry import Registry
from imaging_server_kit.encoding import encode_contents, decode_contents
from imaging_server_kit.serialization import (
    serialize_result_tuple,
    deserialize_result_tuple,
)
from imaging_server_kit.geometry import (
    mask2features,
    instance_mask2features,
    features2mask,
    features2instance_mask,
    boxes2features,
    features2boxes,
    points2features,
    features2points,
    vectors2features,
    features2vectors,
)
