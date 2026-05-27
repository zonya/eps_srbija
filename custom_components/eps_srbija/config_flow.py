import voluptuous as vol
from homeassistant import config_entries
from .eps_api import validate_login

class EPSConfigFlow(config_entries.ConfigFlow, domain="eps_srbija"):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # Provera kredencijala
            valid = await self.hass.async_add_executor_job(validate_login, user_input["email"], user_input["password"])
            if valid:
                return self.async_create_entry(title="EPS Srbija", data=user_input)
            errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("email"): str,
                vol.Required("password"): str,
            }),
            errors=errors
        )
