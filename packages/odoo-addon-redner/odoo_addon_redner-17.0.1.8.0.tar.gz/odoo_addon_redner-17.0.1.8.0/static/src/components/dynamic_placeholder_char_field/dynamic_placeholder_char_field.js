/** @odoo-module **/

import {CharField, charField} from "@web/views/fields/char/char_field";
import {useDynamicPlaceholder} from "@web/views/fields/dynamic_placeholder_hook";
import {patch} from "@web/core/utils/patch";
import {useExternalListener, useEffect} from "@odoo/owl";

// Adding a new property for dynamic placeholder button visibility
CharField.props = {
    ...CharField.props,
    placeholderField: {type: String, optional: true},
    buttonVisibilityField: {type: String, optional: true},
    converterTypeField: {type: String, optional: true},
};

// Extending charField to extract the new property
const charExtractProps = charField.extractProps;
charField.extractProps = (fieldInfo) => {
    return Object.assign(charExtractProps(fieldInfo), {
        placeholderField: fieldInfo.options?.placeholder_field || "",
        buttonVisibilityField: fieldInfo.options?.button_visibility_field || "",
        converterTypeField: fieldInfo.options?.converter_type_field || "",
    });
};

// Patch CharField for dynamic placeholder support
patch(CharField.prototype, {
    setup() {
        super.setup();
        if (this.props.dynamicPlaceholder) {
            this.dynamicPlaceholder = useDynamicPlaceholder(this.input);
            useExternalListener(document, "keydown", this.dynamicPlaceholder.onKeydown);
            useEffect(() =>
                this.dynamicPlaceholder.updateModel(
                    this.props.dynamicPlaceholderModelReferenceField
                )
            );
        }
    },
    get placeholder() {
        return (
            this.props.record.data[this.props.placeholderField] ||
            this.props.placeholder
        );
    },
    get showPlaceholderButton() {
        return (
            this.props.dynamicPlaceholder &&
            !this.props.readonly &&
            this.props.record.data[this.props.buttonVisibilityField]
        );
    },
    get activeConverterType() {
        return this.props.record.data[this.props.converterTypeField] || "";
    },

    async onDynamicPlaceholderOpen() {
        await this.dynamicPlaceholder.open({
            validateCallback: this.handlePlaceholderInsert.bind(this),
        });
    },
    async handlePlaceholderInsert(chain, defaultValue) {
        if (chain) {
            this.input.el.focus();

            // Build placeholder based on converter type
            let placeholder;
            switch (this.activeConverterType) {
                case "field":
                    placeholder = chain;
                    break;
                // Add other converter types here
                default:
                    const defaultValuePart = defaultValue?.length
                        ? ` ||| ${defaultValue}`
                        : "";
                    placeholder = `{{object.${chain}${defaultValuePart}}}`;
                    break;
            }

            this.input.el.setRangeText(
                placeholder,
                this.selectionStart,
                this.selectionStart,
                "end"
            );
            this.input.el.dispatchEvent(new InputEvent("input"));
            this.input.el.dispatchEvent(new KeyboardEvent("keydown"));
            this.input.el.focus();
        }
    },
});
