{
    "name": "VoiceLogica AI Calls",
    "version": "19.0.1.0.0",
    "category": "Productivity/VOIP",
    "summary": "Click to call any phone number in Odoo with VoiceLogica AI phone agents",
    "description": """
Click to call from Odoo with VoiceLogica.

Requires a VoiceLogica account (external service). When a user clicks the call
button, the phone number, the record name and the user's email are sent to
VoiceLogica to place the call.
""",
    "author": "VoiceLogica",
    "website": "https://voicelogica.ai",
    "support": "support@voicelogica.ai",
    "license": "LGPL-3",
    "depends": ["base_setup", "mail"],
    "external_dependencies": {"python": ["requests"]},
    "data": [
        "views/res_config_settings_views.xml",
        "views/res_users_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "voicelogica/static/src/phone_field/*",
        ],
    },
    "images": ["static/description/main_screenshot.png"],
    "installable": True,
    "application": False,
}
