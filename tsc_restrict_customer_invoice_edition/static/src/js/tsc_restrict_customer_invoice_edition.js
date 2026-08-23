odoo.define('tsc_restrict_customer_invoice_edition.restrict_line', function (require) {
"use strict";

var FieldRegistry = require('web.field_registry');
var FormRenderer = require('web.FormRenderer');
var FieldOne2Many = FieldRegistry.get('one2many');
var SectionAndNoteFieldOne2Many = FieldRegistry.get('section_and_note_one2many');

// Patch FormRenderer to toggle tsc_hide_line_controls class on the main form view element
if (FormRenderer) {
    FormRenderer.include({
        _render: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                if (self.state && self.state.data && self.state.data.tsc_is_restricted_user) {
                    if (self.$el) {
                        self.$el.addClass('tsc_hide_line_controls');
                    }
                } else if (self.$el) {
                    self.$el.removeClass('tsc_hide_line_controls');
                }
            });
        },
    });
}

function checkAndToggleRestrictions(self) {
    if (self.name === 'invoice_line_ids') {
        var isRestricted = !!(self.recordData && self.recordData.tsc_is_restricted_user);
        if (self.$el) {
            self.$el.toggleClass('tsc_hide_line_controls', isRestricted);
        }
        if (self.renderer) {
            self.renderer.activeActions.create = !isRestricted;
            self.renderer.activeActions.delete = !isRestricted;
            self.renderer.addCreateControl = !isRestricted;
            self.renderer.addTrashIcon = !isRestricted;
        }
        self.activeActions.create = !isRestricted;
        self.activeActions.delete = !isRestricted;
    }
}

function patchWidget(WidgetClass) {
    if (!WidgetClass) return;
    WidgetClass.include({
        _getRendererParams: function () {
            var params = this._super.apply(this, arguments);
            if (this.name === 'invoice_line_ids' && this.recordData && this.recordData.tsc_is_restricted_user) {
                params.activeActions = _.extend({}, params.activeActions, {
                    create: false,
                    delete: false,
                });
                params.addCreateControl = false;
                params.addTrashIcon = false;
            }
            return params;
        },
        _render: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                checkAndToggleRestrictions(self);
            });
        },
        reset: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                checkAndToggleRestrictions(self);
            });
        },
    });
}

patchWidget(FieldOne2Many);
if (SectionAndNoteFieldOne2Many && SectionAndNoteFieldOne2Many !== FieldOne2Many) {
    patchWidget(SectionAndNoteFieldOne2Many);
}

});
