odoo.define('check_concurrent_update', function (require) {
  "use strict";
  var BasicModel = require('web.BasicModel');

  BasicModel.include({
    _getContext: function (element, options) {
      var context = this._super.apply(this, arguments);
      if (element.data.__last_update) {
        context.__last_update = {
          [element.model + "," + element.res_id]: element.data.__last_update
        }}
      return context;
    },
  })
});
