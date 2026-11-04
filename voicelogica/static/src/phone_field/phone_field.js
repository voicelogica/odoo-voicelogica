import { Component } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { PhoneField } from "@web/views/fields/phone/phone_field";

/** "Call" next to every phone number: places the call through VoiceLogica, the way the user's profile says. */
export class VoiceLogicaCallButton extends Component {
    static template = "voicelogica.CallButton";
    static props = ["*"];

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.title = _t("Call with VoiceLogica");
    }

    get number() {
        return this.props.record.data[this.props.name];
    }

    async onClick() {
        const { record } = this.props;
        try {
            const message = await this.orm.call("res.users", "voicelogica_click_to_call", [
                this.number,
                record.resModel,
                record.resId || false,
            ]);
            this.notification.add(message, { type: "success" });
        } catch (error) {
            // A UserError (no key, phone not registered, ...) is already shown by the RPC error dialog.
            if (!error?.data) {
                this.notification.add(_t("The call could not be started."), { type: "danger" });
            }
        }
    }
}

patch(PhoneField, {
    components: { ...PhoneField.components, VoiceLogicaCallButton },
});
