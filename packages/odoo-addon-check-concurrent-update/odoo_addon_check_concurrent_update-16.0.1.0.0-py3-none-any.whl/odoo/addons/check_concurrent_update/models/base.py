from odoo import models, api, _
from odoo.exceptions import ValidationError

class BaseModelExtend(models.AbstractModel):
    _name = 'basemodel.extend'

    def _register_hook(self):
        def _check_concurrency(self):
            if not (self._log_access and self._context.get(self.CONCURRENCY_CHECK_FIELD)):
                return
            check_clause = "(id = %s AND %s < SUBSTRING(COALESCE(write_date, create_date, (now() at time zone 'UTC'))::VARCHAR FROM 1 FOR 19)::TIMESTAMP)"  # noqa
            for sub_ids in self._cr.split_for_in_conditions(self.ids):
                nclauses = 0
                params = []
                for id in sub_ids:
                    id_ref = "%s,%s" % (self._name, id)
                    update_date = self._context[self.CONCURRENCY_CHECK_FIELD].pop(id_ref, None)
                    if update_date:
                        nclauses += 1
                        params.extend([id, update_date])
                if not nclauses:
                    continue
                query = "SELECT id FROM %s WHERE %s" % (self._table, " OR ".join([check_clause] * nclauses))
                self._cr.execute(query, tuple(params))
                res = self._cr.fetchone()
                if res:
                    # mention the first one only to keep the error message readable
                    raise ValidationError(
                            _('A document was modified since you last viewed it (%s:%d)') % (self._description, res[0])  # noqa
                            )

        models.BaseModel._check_concurrency = _check_concurrency
        return super(BaseModelExtend, self)._register_hook()
