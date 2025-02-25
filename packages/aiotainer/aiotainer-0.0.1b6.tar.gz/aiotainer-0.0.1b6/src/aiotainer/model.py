"""Models for Portainer API data."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from mashumaro import DataClassDictMixin, field_options


class Mode(Enum):
    """Enumeration for different modes."""

    EMPTY = ""
    RW = "rw"
    Z = "z"


class Propagation(Enum):
    """Enumeration for different propagation modes."""

    EMPTY = ""
    RPRIVATE = "rprivate"


class MountType(Enum):
    """Enumeration for different mount types."""

    BIND = "bind"
    VOLUME = "volume"


class PortType(Enum):
    """Enumeration for different port types."""

    TCP = "tcp"


class State(Enum):
    """Enumeration for container states."""

    CREATED = "created"
    DEAD = "dead"
    EXITED = "exited"
    RUNNING = "running"
    RESTARTING = "restarting"
    PAUSED = "paused"


@dataclass
class Container(DataClassDictMixin):
    """Dataclass for container information."""

    id: str = field(metadata=field_options(alias="Id"))
    name: str = field(
        metadata=field_options(
            alias="Names", deserialize=lambda x: x[0].strip("/").capitalize()
        )
    )
    image: str = field(metadata=field_options(alias="Image"))
    state: State = field(metadata=field_options(alias="State"))


@dataclass
class DockerSnapshotRaw(DataClassDictMixin):
    """Dataclass for raw Docker snapshot data."""

    containers: dict[str, Container] = field(
        metadata=field_options(
            alias="Containers",
            deserialize=lambda containers_list: {
                container_data["Id"]: Container.from_dict(container_data)
                for container_data in containers_list
            },
        )
    )


@dataclass
class Snapshot(DataClassDictMixin):
    """Dataclass for snapshot information."""

    time: int = field(metadata=field_options(alias="Time"))
    docker_version: str = field(metadata=field_options(alias="DockerVersion"))
    swarm: bool = field(metadata=field_options(alias="Swarm"))
    total_cpu: int = field(metadata=field_options(alias="TotalCPU"))
    total_memory: int = field(metadata=field_options(alias="TotalMemory"))
    running_container_count: int = field(
        metadata=field_options(alias="RunningContainerCount")
    )
    stopped_container_count: int = field(
        metadata=field_options(alias="StoppedContainerCount")
    )
    healthy_container_count: int = field(
        metadata=field_options(alias="HealthyContainerCount")
    )
    unhealthy_container_count: int = field(
        metadata=field_options(alias="UnhealthyContainerCount")
    )
    volume_count: int = field(metadata=field_options(alias="VolumeCount"))
    image_count: int = field(metadata=field_options(alias="ImageCount"))
    service_count: int = field(metadata=field_options(alias="ServiceCount"))
    stack_count: int = field(metadata=field_options(alias="StackCount"))
    docker_snapshot_raw: DockerSnapshotRaw = field(
        metadata=field_options(alias="DockerSnapshotRaw")
    )
    node_count: int = field(metadata=field_options(alias="NodeCount"))


@dataclass
class NodeData(DataClassDictMixin):
    """Dataclass for node data."""

    id: int = field(metadata=field_options(alias="Id"))
    name: str = field(metadata=field_options(alias="Name"))
    snapshots: list[Snapshot] = field(metadata=field_options(alias="Snapshots"))
    type: int = field(metadata=field_options(alias="Type"), default=0)
    url: str | None = field(metadata=field_options(alias="URL"), default=None)
    group_id: int = field(metadata=field_options(alias="GroupId"), default=0)
    public_url: str | None = field(
        metadata=field_options(alias="PublicURL"), default=None
    )
    gpus: list[Any] | None = field(metadata=field_options(alias="Gpus"), default=None)
    status: int = field(metadata=field_options(alias="Status"), default=0)
    authorized_users: str | None = field(
        metadata=field_options(alias="AuthorizedUsers"), default=None
    )
    authorized_teams: str | None = field(
        metadata=field_options(alias="AuthorizedTeams"), default=None
    )
    tags: str | None = field(metadata=field_options(alias="Tags"), default=None)
    is_edge_device: bool = field(
        metadata=field_options(alias="IsEdgeDevice"), default=False
    )
    enable_gpu_management: bool = field(
        metadata=field_options(alias="EnableGPUManagement"), default=False
    )


@dataclass
class PortainerList(DataClassDictMixin):
    """DataClass for a list of all portainers."""

    data: list[NodeData]
