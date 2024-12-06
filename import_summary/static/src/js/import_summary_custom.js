odoo.define('import_summary.DecoratorExtension', function (require) {
    "use strict";

    var ListRenderer = require('web.ListRenderer');

    ListRenderer.include({
        /**
         * Override the _renderRow method to customize the row based on the record's data.
         *
         * @override
         */
        _renderRow: function (record, index) {
            var $row = this._super.apply(this, arguments);

            if (record.model == "import.summary") {
                if (record.data.row_color) {
                    $row.addClass("import_summary_" + record.data.row_color + "-row");
                }
            }

            return $row;
        }
    });
});