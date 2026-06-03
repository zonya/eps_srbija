from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

DOMAIN = "eps_srbija"


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        EPSSensorRacun(coordinator),
        EPSSensorPotrosnja(coordinator),
    ])


def _last_month_kwh(data):
    if not data:
        return 0.0
    model = (data.get("potrosnja_kwh") or {}).get("consumptionListForLastTwelveMonthsModel", [])
    return round(sum(
        t["monthlyConsumption"][-1]["value"]
        for t in model if t.get("monthlyConsumption")
    ), 2)


class EPSSensorRacun(CoordinatorEntity, SensorEntity):
    """Iznos poslednjeg računa / tekući dug u RSD."""

    _attr_name = "EPS Srbija Račun"
    _attr_unique_id = "eps_srbija_sensor"  # zadržano radi kompatibilnosti
    _attr_icon = "mdi:currency-rsd"
    _attr_native_unit_of_measurement = "RSD"

    @property
    def state(self):
        data = self.coordinator.data or {}
        return data.get("finansije", {}).get("iznos", 0.0)

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data or {}
        return {
            "finansije": data.get("finansije", {}),
            "status_duga": data.get("status_duga", {}),
            "opomene": data.get("opomene", []),
            "poruke": data.get("poruke", []),
            "potrosnja_kwh": data.get("potrosnja_kwh", []),
            "potrosnja_rsd": data.get("potrosnja_rsd", []),
            "last_updated": data.get("last_updated"),
        }


class EPSSensorPotrosnja(CoordinatorEntity, SensorEntity):
    """Potrošnja prošlog meseca u kWh."""

    _attr_name = "EPS Srbija Potrošnja"
    _attr_unique_id = "eps_srbija_potrosnja_kwh"
    _attr_icon = "mdi:lightning-bolt"
    _attr_native_unit_of_measurement = "kWh"

    @property
    def state(self):
        return _last_month_kwh(self.coordinator.data)

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data or {}
        return {
            "potrosnja_kwh": data.get("potrosnja_kwh", []),
            "last_updated": data.get("last_updated"),
        }
