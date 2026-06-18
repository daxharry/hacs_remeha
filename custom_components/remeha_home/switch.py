"""Platform for switch integration."""

from __future__ import annotations
import logging


from homeassistant.components.switch import (
    SwitchDeviceClass,
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import RemehaHomeAPI
from .const import DOMAIN
from .coordinator import RemehaHomeUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Remeha Home switch entities from a config entry."""
    api = hass.data[DOMAIN][entry.entry_id]["api"]
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    entities = []
    for appliance in coordinator.data["appliances"]:
        for climate_zone in appliance["climateZones"]:
            climate_zone_id = climate_zone["climateZoneId"]
            entities.append(
                RemehaHomeFireplaceModeSwitch(api, coordinator, climate_zone_id)
            )

        for hot_water_zone in appliance["hotWaterZones"]:
            hot_water_zone_id = hot_water_zone["hotWaterZoneId"]
            entities.append(
                RemehaHomeHotWaterComfortSwitch(api, coordinator, hot_water_zone_id)
            )

    async_add_entities(entities)


class RemehaHomeSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a switch."""

    _attr_has_entity_name = True

    def __init__(
        self,
        api: RemehaHomeAPI,
        coordinator: RemehaHomeUpdateCoordinator,
        climate_zone_id: str,
        entity_description: SwitchEntityDescription,
    ) -> None:
        """Create a Remeha Home switch entity."""
        super().__init__(coordinator)
        self.api = api
        self.climate_zone_id = climate_zone_id
        self.entity_description = entity_description

        self._attr_unique_id = "_".join(
            [DOMAIN, self.climate_zone_id, entity_description.key]
        )

    @property
    def _data(self):
        """Return the climate zone data for this switch."""
        return self.coordinator.get_by_id(self.climate_zone_id)

    @property
    def is_on(self) -> bool:
        """Return the state of this switch."""
        return self._data[self.entity_description.key]

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for this device."""
        return self.coordinator.get_device_info(self.climate_zone_id)


class RemehaHomeHotWaterComfortSwitch(CoordinatorEntity, SwitchEntity):
    """Switch to force hot water zone into continuous comfort mode."""

    _attr_has_entity_name = True
    _attr_name = "Force Water Comfort"
    _attr_icon = "mdi:water-boiler"
    _attr_device_class = SwitchDeviceClass.SWITCH

    def __init__(
        self,
        api: RemehaHomeAPI,
        coordinator: RemehaHomeUpdateCoordinator,
        hot_water_zone_id: str,
    ) -> None:
        """Create a Remeha Home hot water comfort switch."""
        super().__init__(coordinator)
        self.api = api
        self.hot_water_zone_id = hot_water_zone_id
        self._attr_unique_id = f"{DOMAIN}_{hot_water_zone_id}_force_water_comfort"

    @property
    def _data(self):
        return self.coordinator.get_by_id(self.hot_water_zone_id)

    @property
    def is_on(self) -> bool:
        """Return True when hot water zone is in continuous comfort mode."""
        return self._data.get("dhwZoneMode") == "ContinuousComfort"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for this switch."""
        return self.coordinator.get_device_info(self.hot_water_zone_id)

    async def async_turn_on(self, **kwargs):
        """Switch hot water to continuous comfort mode."""
        _LOGGER.debug("Enable hot water continuous comfort mode")
        await self.api.async_set_dhw_comfort(self.hot_water_zone_id)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Switch hot water back to schedule mode."""
        _LOGGER.debug("Disable hot water continuous comfort mode (back to schedule)")
        await self.api.async_set_dhw_schedule(self.hot_water_zone_id)
        await self.coordinator.async_request_refresh()


class RemehaHomeFireplaceModeSwitch(RemehaHomeSwitch):
    """Representation of a fireplace mode switch."""

    def __init__(
        self,
        api: RemehaHomeAPI,
        coordinator: RemehaHomeUpdateCoordinator,
        climate_zone_id: str,
    ) -> None:
        """Create a Remeha Home fireplace mode switch entity."""
        super().__init__(
            api,
            coordinator,
            climate_zone_id,
            SwitchEntityDescription(
                key="firePlaceModeActive",
                name="Fireplace Mode",
                device_class=SwitchDeviceClass.SWITCH,
            ),
        )

    @property
    def icon(self):
        """Return the icon for this switch."""
        if self.is_on:
            return "mdi:fireplace"
        return "mdi:fireplace-off"

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        _LOGGER.debug("Enable fireplace mode")
        await self.api.async_set_fireplace_mode(self.climate_zone_id, True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        _LOGGER.debug("Disable fireplace mode")
        await self.api.async_set_fireplace_mode(self.climate_zone_id, False)
        await self.coordinator.async_request_refresh()
