from odoo import fields, models

DEFAULT_API_URL = "https://api.voicelogica.ai"


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    voicelogica_api_key = fields.Char(string="VoiceLogica API key", config_parameter="voicelogica.api_key")
    voicelogica_api_url = fields.Char(
        string="VoiceLogica server",
        config_parameter="voicelogica.api_url",
        default=DEFAULT_API_URL,
    )

    def action_voicelogica_test(self):
        self.set_values()
        return self.env["res.users"].voicelogica_test()
