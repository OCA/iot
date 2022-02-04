odoo.define("iot_option.IotOptionView", function(require) {
    "use strict";

    var BasicView = require("web.BasicView");
    var IotOptionRenderer = require("iot_option.IotOptionRenderer");
    var view_registry = require("web.view_registry");
    var core = require("web.core");

    var _lt = core._lt;

    var IotOptionView = BasicView.extend({
        display_name: _lt("Iot Option"),
        viewType: "iot_option",
        config: _.extend({}, BasicView.prototype.config, {
            Renderer: IotOptionRenderer,
        }),
        multi_record: true,
        searchable: false,
    });

    view_registry.add("iot_option", IotOptionView);

    return IotOptionView;
});
