import datetime

from odoo import models


class Metric(models.Model):
    _inherit = "ir.metric"

    def _default_domains(self):
        domain = super(Metric, self)._default_domains()
        if self.name == "last_update_incoming_mail":
            domain = [
                "&",
                (
                    "nextcall",
                    "<=",
                    (datetime.datetime.now() - datetime.timedelta(days=2)).strftime(
                        "%Y-%m-%d"
                    ),
                ),
                ("active", "=", True),
                ("id", "=", 6),
            ]
        return domain
