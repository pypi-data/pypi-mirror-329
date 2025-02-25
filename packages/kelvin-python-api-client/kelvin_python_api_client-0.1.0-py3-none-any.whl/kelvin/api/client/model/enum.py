from __future__ import annotations

from enum import Enum


class AppType(Enum):
    app = "app"
    importer = "importer"
    exporter = "exporter"
    docker = "docker"


class GatewayMode(Enum):
    socket = "socket"
    legacy = "legacy"


class Way(Enum):
    output = "output"
    input_cc = "input-cc"
    input_cc_output = "input-cc+output"
    input = "input"
    output_cc = "output-cc"
    input_output_cc = "input+output-cc"


class Storage(Enum):
    node_and_cloud = "node-and-cloud"
    node = "node"
    none = "none"


class DynamicIOOwnership(Enum):
    both = "both"
    owned = "owned"
    remote = "remote"


class DynamicIOType(Enum):
    both = "both"
    data = "data"
    control = "control"


class DeploymentType(Enum):
    standard = "standard"
    staged_instant_apply = "staged+instant-apply"
    staged_only = "staged-only"


class LivenessProbeType(Enum):
    http_get = "http_get"
    tcp_socket = "tcp_socket"
    exec = "exec"


class URIScheme(Enum):
    http = "http"
    https = "https"


class PortType(Enum):
    host = "host"
    service = "service"


class VolumeType(Enum):
    persistent = "persistent"
    host = "host"
    text = "text"


class VolumeEncoding(Enum):
    utf_8 = "utf-8"
    ascii = "ascii"
    latin_1 = "latin_1"


class AppStatus(Enum):
    running = "running"
    stopped = "stopped"
    updating = "updating"
    requires_attention = "requires_attention"


class ParameterType(Enum):
    number = "number"
    string = "string"
    boolean = "boolean"


class ParameterScheduleState(Enum):
    scheduled = "scheduled"
    scheduled_revert = "scheduled-revert"
    completed = "completed"
    error = "error"


class WorkloadDownloadStatus(Enum):
    pending = "pending"
    scheduled = "scheduled"
    processing = "processing"
    downloading = "downloading"
    ready = "ready"
    failed = "failed"


class WorkloadStatus(Enum):
    pending_deploy = "pending_deploy"
    pending_update = "pending_update"
    pending_start = "pending_start"
    pending_stop = "pending_stop"
    pending_apply = "pending_apply"
    deploying = "deploying"
    running = "running"
    stopping = "stopping"
    stopped = "stopped"
    failed = "failed"
    starting = "starting"
    applying = "applying"
    received = "received"
    downloading = "downloading"
    ready = "ready"
    unreachable = "unreachable"
    staged = "staged"


class GuardrailRelativeType(Enum):
    VALUE = "value"
    PERCENTAGE = "percentage"


class AssetState(Enum):
    online = "online"
    offline = "offline"
    unknown = "unknown"


class PropertyType(Enum):
    boolean = "boolean"
    number = "number"
    string = "string"
    timestamp = "timestamp"


class ControlChangeState(Enum):
    pending = "pending"
    ready = "ready"
    sent = "sent"
    processed = "processed"
    applied = "applied"
    failed = "failed"
    rejected = "rejected"


class RecommendationState(Enum):
    pending = "pending"
    accepted = "accepted"
    auto_accepted = "auto_accepted"
    rejected = "rejected"
    expired = "expired"
    error = "error"


class ControlChangeSource(Enum):
    bridge = "bridge"
    ccm = "ccm"


class DataType(Enum):
    boolean = "boolean"
    number = "number"
    object = "object"
    string = "string"


class ClusterType(Enum):
    k3s = "k3s"
    kubernetes = "kubernetes"
    docker = "docker"


class OrchestrationClusterStatus(Enum):
    pending_provision = "pending_provision"
    pending = "pending"
    online = "online"
    unreachable = "unreachable"
    requires_attention = "requires_attention"


class OrchestrationNodeStatus(Enum):
    online = "online"
    unreachable = "unreachable"
    not_ready = "not_ready"


class ResourceType(Enum):
    asset = "asset"
    datastream = "datastream"
    app = "app"
    parameter = "parameter"


class RolePolicyAction(Enum):
    field_ = "*"
    create = "create"
    read = "read"
    update = "update"
    delete = "delete"


class LegacyAppType(Enum):
    kelvin = "kelvin"
    docker = "docker"
    bridge = "bridge"
