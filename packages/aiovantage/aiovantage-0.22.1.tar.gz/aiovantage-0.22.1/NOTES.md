# New Controllers?

## Overview

- Group objects by their primary interface
- Allow objects to exist in multiple groups
- Store objects in a single client-level object store

## Tricky ones

- button_parent / station / keypad

## Stateless collections

- `vantage.controllers`
  - Fetches: `Master`
  - Vantage Master Controllers

- `vantage.modules`
  - Fetches [`Module`, `ModuleGen2`] (or maybe `ModuleInterface`?)
  - Vantage Dimmer/Relay Modules

- `vantage.parent_devices`
  - Fetches `ParentDevice.subclasses()`
  - Vantage "Hub" devices

- `vantage.power_profile`
  - Fetches `PowerProfile.subclasses()`
  - Vantage Power Profiles

- `vantage.back_boxes`
  - Fetches `BackBox.subclasses()`
  - Vantage Back Boxes

## Stateful collections

Grouped by their "primary" interface.

- `vantage.blinds`
  - Implements: `BlindInterface`
  - Fetches: `BlindInterface.implementers()`
  - Querysets:
    - `vantage.blinds.blind_groups` (`isinstance(obj, BlindGroup)`)

- `vantage.buttons`
  - Implements: `ButtonInterface`
  - Fetches: `ButtonInterface.implementers()`
  - Querysets:
    - `vantage.buttons.dry_contacts` (`isinstance(obj, DryContact)`)
    - `vantage.buttons.buttons` (`isinstance(obj, Button)`)

- `vantage.loads`
  - Implements: `LoadInterface`
  - Fetches: `LoadInterface.implementers()`
  - Querysets:
    - `vantage.loads.load_groups` `isinstance(obj, LoadGroup)`
    - `vantage.loads.relays` (`isinstance(obj, Load) and obj.is_relay`)
    - `vantage.loads.lights`

      ```python
      if (isinstance(obj, Load) and obj.load_type in [...])
          or isinstance(obj, RGBLoadInterface)
          or isinstance(obj, ColorTemperatureInterface):
          ...
      ```

    - `vantage.loads.motors` (`isinstance(obj, Load) and obj.is_motor`)
    - `vantage.loads.rgb_lights` (`isiinstance(obj, RGBLoadInterface)`)

- `vantage.thermostats`
  - Implements: `ThermostatInterface`
  - Fetches: `ThermostatInterface.implementers()`
  - Querysets:
    - `vantage.thermostats.humidistats` (`isinstance(obj, HumidityInterface)`)
    - `vantage.thermostats.fans` (`isinstance(obj, FanInterface)`)

- `vantage.sensors`
  - Implements: `SensorInterface`
  - Querysets:
    - `vantage.sensors.anemo_sensors` (`type is AnemoSensor`)
    - `vantage.sensors.light_sensors` (`type is LightSensor`)
    - `vantage.sensors.omni_sensors` (`type is OmniSensor`)

- `vantage.tasks`
  - Implements: `TaskInterface`

- `vantage.variables`
  - Implements: `GMemInterface`

## Alternatively

```python
from aiovantage import Vantage
from aiovantage.config_client.requests import get_objects
from aiovantage.object_interfaces.base import Interface
from aiovantage.objects import SystemObject

v = Vantage("10.2.0.103", "administrator", "ZZuUw76CnL")


async def fetch_interface_objects(interface: Interface, filter: Callable[[Any], bool] = None):
    implementers = interface.implementers()
    element_names = [cls.element_name() for cls in implementers if issubclass(cls, SystemObject)]
    async for obj in get_objects(v.config_client, types=element_names):
        if filter is None or filter(obj):
          yield obj

```

## Cool "user store" object stuff

```python
# Get the first master controller
master = vantage.masters.first()

# Create a new GMem object in the "user store"
vid = await master.create_object("GMem")

# Get the GMem object
await vantage.gmem.initialize()
gmem = vantage.gmem.get(vid)

# Set some properties
await gmem.set_property_ex("Name", "My GMem")
```

## Mirroring Design Center

- Area
  - Loads
  - Color Loads
  - Dry Contacts
  - Thermostats
  - ...
- Enclosure
  - Enclosures
  - Controllers
  - Modules
  - DINStations
- Bus (all subclasses of StationBus)
  - WireLink
  - EthernetLink
  - RadioLink
  - ...
- Programming
  - Task
  - GMem
  - LoadGroup (for some reason)
- Profile
  - KeypadStyle
  - ButtonStyle
  - LEDStyle
  - PowerProfile
  - DCPowerProfile
  - RFLCPowerProfile
  - PWMPowerProfile
  - FixtureDefintion
  - EQCtrlStyle
  - EQUXStyle
