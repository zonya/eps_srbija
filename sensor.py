from homeassistant.components.sensor import SensorEntity
from datetime import datetime
from .eps_api import get_eps_full_data

async def async_setup_entry(hass, entry, async_add_entities):
    """Postavljanje senzora kroz konfiguracionu jedinicu."""
    async_add_entities([EPSSensor(hass, entry)])

class EPSSensor(SensorEntity):
    def __init__(self, hass, entry):
        self._hass = hass
        self._entry = entry
        self._attr_name = "EPS Podaci"
        self._attr_unique_id = "eps_srbija_sensor"
        # Ikona koja će se videti kada senzor postane aktivan u HA
        self._attr_icon = "mdi:lightning-bolt"
        
        # Inicijalno stanje sa praznim strukturama
        self._data = {
            "finansije": {"iznos": 0.0, "poziv_na_broj": "", "rok_dospeca": ""},
            "status_duga": {"balance_amount": 0.0, "commercial_contracts_number": ""},
            "opomene": [],
            "poruke": [],
            "potrosnja_kwh": [],
            "potrosnja_rsd": [],
            "last_updated": None
        }

    @property
    def state(self):
        """Vraća iznos duga kao stanje senzora."""
        return self._data.get("finansije", {}).get("iznos", 0.0)

    @property
    def unit_of_measurement(self):
        return "RSD"

    @property
    def extra_state_attributes(self):
        """Mapiranje podataka u atribute senzora za tvoj dashboard."""
        return {
            "finansije": self._data.get("finansije", {}),
            "status_duga": self._data.get("status_duga", {}),
            "opomene": self._data.get("opomene", []),
            "poruke": self._data.get("poruke", []),
            "potrosnja_kwh": self._data.get("potrosnja_kwh", []),
            "potrosnja_rsd": self._data.get("potrosnja_rsd", []),
            "last_updated": self._data.get("last_updated")
        }

    async def async_update(self):
        """Asinhrono osvežavanje podataka sa EPS API-ja."""
        email = self._entry.data.get("email")
        password = self._entry.data.get("password")
        
        # Pozivanje API-ja u posebnom thread-u
        data = await self._hass.async_add_executor_job(get_eps_full_data, email, password)
        
        if data and data.get("status") == "OK":
            data["last_updated"] = datetime.now().strftime("%d.%m.%Y. %H:%M")
            self._data = data
