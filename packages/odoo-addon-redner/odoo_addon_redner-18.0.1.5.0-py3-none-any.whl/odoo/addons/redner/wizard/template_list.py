import base64

from odoo import fields, models  # type: ignore[import-untyped]


class TemplateListWizard(models.TransientModel):
    _name = "template.list.wizard"
    _description = "Template List Wizard"

    name = fields.Char(
        string="Name",
        required=True,
        help="Name of the redner template",
    )

    description = fields.Char(
        string="Description",
        help="Description of the template",
    )

    preview = fields.Binary(
        string="Preview",
        help=("The PNG preview of the template"),
    )

    def populate(self, templates):
        self.search([]).unlink()
        template = self.env["redner.template"].browse(self.env.context.get("active_id"))
        for t in templates:
            p = template.get_preview(t["name"])
            b64 = base64.b64encode(p.content)
            self.create(
                {
                    "name": t["name"],
                    "description": t["description"],
                    "preview": b64,
                }
            )

    def action_select_template(self):
        template = self.env["redner.template"].browse(self.env.context.get("active_id"))
        t_name = self.env.context.get("template_id")
        template.write(
            {
                "name": t_name,
                "redner_id": t_name,
                "active": True,
                "source": "redner",
                "allow_modification_from_odoo": False,
            }
        )
        return {
            "type": "ir.actions.act_window",
            "res_model": "redner.template",
            "view_mode": "form",
            "res_id": template.id,
            "target": "current",
        }
