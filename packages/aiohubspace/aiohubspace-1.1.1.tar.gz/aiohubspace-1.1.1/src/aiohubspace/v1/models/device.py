from dataclasses import dataclass, field

from .resource import DeviceInformation, ResourceTypes
from .sensor import HubspaceSensor


@dataclass
class Device:
    """Representation of a Hubspace parent item"""

    id: str  # ID used when interacting with Hubspace
    available: bool

    sensors: dict[str, HubspaceSensor] = field(default_factory=dict)
    binary_sensors: dict[str, HubspaceSensor] = field(default_factory=dict)
    device_information: DeviceInformation = field(default_factory=DeviceInformation)

    type: ResourceTypes = ResourceTypes.PARENT_DEVICE
