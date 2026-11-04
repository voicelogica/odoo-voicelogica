import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from .res_config_settings import DEFAULT_API_URL

TIMEOUT_SECONDS = 15


class ResUsers(models.Model):
    _inherit = "res.users"

    voicelogica_email = fields.Char(
        string="VoiceLogica email",
        help="The email you sign in to VoiceLogica with. Leave empty when it is the same as your Odoo email.",
    )

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + ["voicelogica_email"]

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + ["voicelogica_email"]

    @api.model
    def _voicelogica_request(self, method, path, payload=None):
        params = self.env["ir.config_parameter"].sudo()
        key = params.get_param("voicelogica.api_key")
        if not key:
            raise UserError(_("VoiceLogica is not connected yet. An administrator adds the API key in Settings."))
        base_url = params.get_param("voicelogica.api_url") or DEFAULT_API_URL
        try:
            response = requests.request(
                method,
                f"{base_url.rstrip('/')}/api/v1{path}",
                json=payload,
                headers={"x-api-key": key},
                timeout=TIMEOUT_SECONDS,
            )
        except requests.RequestException:
            raise UserError(_("VoiceLogica could not be reached. Try again in a moment.")) from None
        try:
            body = response.json()
        except ValueError:
            body = {}
        if not response.ok:
            reason = isinstance(body, dict) and (body.get("reason") or body.get("error"))
            if response.status_code in (401, 403) and not reason:
                reason = _("VoiceLogica did not accept the API key.")
            raise UserError(reason or _("VoiceLogica answered with error %s.", response.status_code))
        return body

    @api.model
    def voicelogica_test(self):
        company = self._voicelogica_request("GET", "/users/me").get("defaultCompany") or {}
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "type": "success",
                "message": _("Connected to VoiceLogica company %s.", company.get("name") or ""),
            },
        }

    @api.model
    def voicelogica_click_to_call(self, number, res_model=False, res_id=False):
        """Called by the phone field's VoiceLogica button. Places the call for the current user, the way
        their VoiceLogica profile says: their phones ring first, or an AI assistant calls and puts them through."""
        email = self.env.user.voicelogica_email or self.env.user.email or self.env.user.login
        payload = {"destinationNumber": number, "userEmail": (email or "").strip().lower()}
        if res_model and res_id:
            record = self.env[res_model].browse(int(res_id)).exists()
            if record:
                record.check_access("read")
                payload["contactName"] = (record.display_name or "")[:120]
        result = self._voicelogica_request("POST", "/phones/calls/click-to-call", payload)
        if result.get("method") == "ring_me":
            return _("Your phone is ringing. Pick up to be connected to %s.", number)
        return _("Your VoiceLogica assistant is calling %s and will put them through to you.", number)
