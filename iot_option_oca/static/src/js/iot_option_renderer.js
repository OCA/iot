odoo.define("iot_option.IotOptionRenderer", function (require) {
    "use strict";

    var BasicRenderer = require("web.BasicRenderer");
    var field_registry = require("web.field_registry");
    var core = require("web.core");
    var qweb = core.qweb;

    var IotOptionRenderer = BasicRenderer.extend({
        init: function (parent, state, params) {
            var safeParam = _.defaults({}, params, {
                viewType: "iot_option",
            });
            this._super(parent, state, safeParam);
            if (
                parent !== undefined &&
                parent.mode === "edit" &&
                safeParam.mode === undefined
            ) {
                this.mode = "edit";
            }
            this.recordWidgets = [];
        },
        _getWidgetOptions: function (data) {
            var mode = this.mode;
            if (data.data.readonly) {
                mode = "readonly";
            }
            var options = {
                attrs: {
                    options: {},
                    modifiers: {},
                },
                mode: mode,
                viewType: this.viewType,
            };
            if (data.data.required) {
                options.attrs.modifiers.required = true;
            }
            if (data.data.widget === "many2one") {
                options.attrs.options.no_create_edit = true;
                options.attrs.options.no_open = true;
            }
            return options;
        },
        _renderView: function () {
            var self = this;
            var $table = $(qweb.render("iot_option.table"));
            var $body = $table.find("tbody");
            this.$el.empty();
            this.recordWidgets = [];
            $table.appendTo(this.$el);
            _.each(this.state.data, function (data) {
                var element = $(
                    qweb.render("iot_option.item", {
                        widget: self,
                        data: data,
                    })
                );
                var Widget = field_registry.get(data.data.widget);
                if (Widget !== undefined) {
                    self._renderIotOptionWidget(Widget, element, data);
                }
                element.appendTo($body);
            });
            return this._super();
        },
        _renderIotOptionWidget: function (Widget, element, data) {
            var options = this._getWidgetOptions(data);
            var widget = new Widget(
                this,
                "value_" + data.data.field_type,
                data,
                options
            );
            this.recordWidgets.push(widget);
            this._registerModifiers(widget, data, element, _.pick(options, "mode"));
            var node = element.find(".result_data");
            widget.appendTo(node);
        },
        _onNavigationMove: function (ev) {
            var currentIndex = -1;
            if (ev.data.direction === "next") {
                currentIndex = this.recordWidgets.indexOf(ev.data.target || ev.target);
                if (currentIndex + 1 >= (this.recordWidgets || []).length) {
                    return;
                }
                ev.stopPropagation();
                this._activateNextIotOptionWidget(currentIndex);
            } else if (ev.data.direction === "previous") {
                currentIndex = this.recordWidgets.indexOf(ev.data.target);
                if (currentIndex <= 0) {
                    return;
                }
                ev.stopPropagation();
                this._activatePreviousIotOptionWidget(currentIndex);
            }
        },
        _activateNextIotOptionWidget: function (currentIndex) {
            var activatedIndex = this._activateIotOptionWidget(
                (currentIndex + 1) % (this.recordWidgets || []).length,
                {inc: 1}
            );
            if (activatedIndex === -1) {
                // No widget have been activated, we should go to the edit/save buttons
                this.trigger_up("focus_control_button");
                this.lastActivatedFieldIndex = -1;
            } else {
                this.lastActivatedFieldIndex = activatedIndex;
            }
            return this.lastActivatedFieldIndex;
        },
        _activatePreviousIotOptionWidget: function (currentIndex) {
            var safeCurrentIndex = currentIndex
                ? currentIndex - 1
                : (this.recordWidgets || []).length - 1;
            return this._activateIotOptionWidget(safeCurrentIndex, {inc: -1});
        },
        _activateIotOptionWidget: function (currentIndex, options) {
            var safeOptions = options || {};
            _.defaults(safeOptions, {inc: 1, wrap: false});
            // Do not allow negative currentIndex
            var index = Math.max(0, currentIndex);

            for (var i = 0; i < this.recordWidgets.length; i++) {
                var activated = this.recordWidgets[index].activate({
                    event: safeOptions.event,
                    noAutomaticCreate: safeOptions.noAutomaticCreate || false,
                });
                if (activated) {
                    return index;
                }

                index += safeOptions.inc;
                if (index >= this.recordWidgets.length) {
                    if (safeOptions.wrap) {
                        index -= this.recordWidgets.length;
                    } else {
                        return -1;
                    }
                } else if (index < 0) {
                    if (safeOptions.wrap) {
                        index += this.recordWidgets.length;
                    } else {
                        return -1;
                    }
                }
            }
            return -1;
        },
    });

    return IotOptionRenderer;
});
