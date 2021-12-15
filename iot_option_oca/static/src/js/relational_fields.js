odoo.define("iot_option.relational_fields", function(require) {
    "use strict";

    var IotOptionRenderer = require("iot_option.IotOptionRenderer");
    var relational_fields = require("web.relational_fields");

    relational_fields.FieldOne2Many.include({
        _getRenderer: function() {
            if (this.view.arch.tag === "iot_option") {
                return IotOptionRenderer;
            }
            return this._super.apply(this, arguments);
        },
        _updateCustomInfoItem: function(data) {
            var result = {
                value_float: data.value_float,
                value_str: data.value_str,
                value_int: data.value_int,
                value_bool: data.value_bool,
                value_date: data.value_date,
            };
            return result;
        },
        _saveIotOption: function() {
            var self = this;
            _.each(this.renderer.recordWidgets, function(widget) {
                self._setValue({
                    operation: "UPDATE",
                    id: widget.dataPointID,
                    data: self._updateCustomInfoItem(widget.recordData),
                });
            });
        },
        commitChanges: function() {
            if (this.renderer && this.renderer.viewType === "iot_option") {
                var self = this;
                this.renderer.commitChanges().then(function() {
                    return self._saveIotOption();
                });
            }
            return this._super.apply(this, arguments);
        },
        activate: function() {
            var result = this._super.apply(this, arguments);
            if (result && this.renderer.viewType === "iot_option") {
                if (this.renderer.recordWidgets.length > 0) {
                    this.renderer.recordWidgets[0].$input.focus();
                }
            }
            return result;
        },
    });
});
