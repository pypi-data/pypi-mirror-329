##############################################################################
#
#    Redner Odoo module
#    Copyright © 2016, 2025 XCG Consulting <https://xcg-consulting.fr>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import _, api, fields, models  # type: ignore[import-untyped]
from odoo.addons import converter
from odoo.exceptions import ValidationError  # type: ignore[import-untyped]

from ..converter import ImageDataURL, ImageFile
from ..utils.sorting import parse_sorted_field, sortkey

FIELD = "field"
CONSTANT = "constant"
MAIL_TEMPLATE = "mail_template"
MAIL_TEMPLATE_DESERIALIZE = "mail_template+deserialize"
IMAGE_FILE = "image-file"
IMAGE_DATAURL = "image-data-url"
RELATION_2MANY = "relation-to-many"
RELATION_PATH = "relation-path"

CONVERTER_SELECTION = [
    (MAIL_TEMPLATE, "Odoo Template"),
    (MAIL_TEMPLATE_DESERIALIZE, "Odoo Template + Eval"),
    (FIELD, "Field"),
    (IMAGE_FILE, "Image file"),
    (IMAGE_DATAURL, "Image data url"),
    (RELATION_2MANY, "Relation to many"),
    (RELATION_PATH, "Relation Path"),
    (CONSTANT, "Constant value"),
]

DYNAMIC_PLACEHOLDER_ALLOWED_CONVERTERS = (
    FIELD,
    MAIL_TEMPLATE,
    MAIL_TEMPLATE_DESERIALIZE,
)


class Substitution(models.Model):
    """Substitution values for a Redner email message"""

    _name = "redner.substitution"
    _inherit = ["mail.render.mixin"]
    _description = "Redner Substitution"

    keyword = fields.Char(string="Variable", help="Template variable name")

    template_id = fields.Many2one(comodel_name="mail.template", string="Email Template")

    ir_actions_report_id = fields.Many2one(
        comodel_name="ir.actions.report", string="Report"
    )

    model = fields.Char(
        "Related Report Model",
        related="ir_actions_report_id.model",
        index=True,
        store=True,
        readonly=True,
    )

    value = fields.Char(string="Expression")

    converter = fields.Selection(selection=CONVERTER_SELECTION)

    depth = fields.Integer(string="Depth", compute="_compute_depth", store=True)

    value_placeholder = fields.Char(
        compute="_compute_value_placeholder", string="Placeholder Text"
    )

    hide_placeholder_button = fields.Boolean(
        compute="_compute_hide_placeholder_button", string="Hide Placeholder Button"
    )

    @api.onchange("converter")
    def _onchange_converter(self):
        if self.converter:
            self.value = False

    @api.depends("converter")
    def _compute_value_placeholder(self):
        """Compute placeholder text based on conversion type"""
        placeholder_map = {
            FIELD: _("e.g: name or partner_id.name"),
            MAIL_TEMPLATE: _("e.g: {{object.partner_id.name}}"),
            MAIL_TEMPLATE_DESERIALIZE: _("e.g: {{ object.get_partner_info() | safe }}"),
            RELATION_PATH: _(
                "e.g: partner_id/category_id/name ou partner_id/child_ids[]"
            ),
            RELATION_2MANY: _("e.g: tax_ids"),
            CONSTANT: _("e.g: www.orbeet.io"),
        }
        for record in self:
            record.value_placeholder = placeholder_map.get(record.converter, _("N/A"))

    @api.depends("value")
    def _compute_render_model(self):
        for substitution in self:
            if substitution.ir_actions_report_id:
                substitution.render_model = substitution.model
            elif substitution.template_id:
                substitution.render_model = substitution.template_id.model_id.model
            else:
                substitution.render_model = False

    @api.depends("keyword")
    def _compute_depth(self):
        for record in self:
            record.depth = record.keyword.count(".")

    @api.depends("converter")
    def _compute_hide_placeholder_button(self):
        """Determine if placeholder button should be hidden"""
        for record in self:
            record.hide_placeholder_button = (
                record.converter not in DYNAMIC_PLACEHOLDER_ALLOWED_CONVERTERS
            )

    def get_children(self):
        return self.search(
            [
                ("ir_actions_report_id", "=", self.ir_actions_report_id.id),
                ("keyword", "=like", self.keyword + ".%"),
                ("depth", "=", self.depth + 1),
            ]
        )

    def build_converter(self):
        d = {}
        for sub in self:
            if sub.converter == "mail_template":
                conv = converter.MailTemplate(sub.value, False)
            elif sub.converter == "mail_template+deserialize":
                conv = converter.MailTemplate(sub.value, True)
            elif sub.converter == "constant":
                conv = converter.Constant(sub.value)
            elif sub.converter == "field":
                if "." in sub.value:
                    path, name = sub.value.rsplit(".", 1)
                else:
                    path, name = None, sub.value
                conv = converter.Field(name)
                if path:
                    conv = converter.relation(path.replace(".", "/"), conv)
            elif sub.converter == "image-file":
                if "." in sub.value:
                    path, name = sub.value.rsplit(".", 1)
                else:
                    path, name = None, sub.value
                conv = ImageFile(name)
                if path:
                    conv = converter.relation(path.replace(".", "/"), conv)
            elif sub.converter == "image-data-url":
                conv = ImageDataURL(sub.value)
            elif sub.converter == "relation-to-many":
                # Unpack the result of finding a field with its sort order into
                # variable names.
                value, sorted = parse_sorted_field(sub.value)
                conv = converter.RelationToMany(
                    value,
                    None,
                    sortkey=sortkey(sorted) if sorted else None,
                    converter=sub.get_children().build_converter(),
                )
            elif sub.converter == "relation-path":
                conv = converter.relation(
                    sub.value, sub.get_children().build_converter()
                )
            elif sub.converter is False:
                continue
            else:
                raise ValidationError(_("invalid converter type: %s") % sub.converter)
            d[sub.keyword.rsplit(".", 2)[-1]] = conv

        return converter.Model(d)
