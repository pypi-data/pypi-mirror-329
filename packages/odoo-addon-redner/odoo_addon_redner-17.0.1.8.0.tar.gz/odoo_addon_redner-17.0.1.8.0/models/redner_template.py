##############################################################################
#
#    Redner Odoo module
#    Copyright © 2016 XCG Consulting <https://xcg-consulting.fr>
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

import base64
import logging

from odoo import _, api, fields, models  # type: ignore[import-untyped]
from odoo.exceptions import ValidationError  # type: ignore[import-untyped]
from odoo.tools.cache import ormcache  # type: ignore[import-untyped]

from ..redner import REDNER_API_PATH, Redner
from ..utils.mimetype import get_file_extension

logger = logging.getLogger(__name__)

_redner = None

LANGUAGE_MJML_MUSTACHE = "text/mjml|mustache"
LANGUAGE_TYPST_MUSTACHE = "application/typst|mustache"
LANGUAGE_OPENDOCUMENT_MUSTACHE = "application/vnd.oasis.opendocument.text|od+mustache"
DEFAULT_LANGUAGE = LANGUAGE_MJML_MUSTACHE
COMPUTED_FIELDS = [
    "body",
    "description",
    "slug",
    "is_mjml",
    "language",
    "locale_id",
]
EDITABLE_FIELDS = [
    "redner_id",
    "name",
]


class RednerTemplate(models.Model):
    _name = "redner.template"
    _description = "Redner Template"

    cache = {}

    source = fields.Selection(
        string="Source",
        selection=[
            ("redner", "Redner"),
            ("odoo", "Odoo"),
        ],
        required=True,
        default="odoo",
        help=("Source of the template, created in Odoo or imported from Redner."),
    )

    allow_modification_from_odoo = fields.Boolean(
        string="Allow modification from odoo",
        required=True,
        default=True,
        help=(
            "If Odoo can edit the template. If the source is redner,"
            " by default Odoo can't edit the template."
            "It is invisible and set to True if the source is Odoo."
        ),
    )

    preview = fields.Binary(
        string="Preview",
        default="New",
        compute="_compute_preview",
        help="This is a preview of the template",
    )

    name = fields.Char(
        string="Name",
        default="New",
        required=True,
        help=(
            "The name of the template. Once the template is created, "
            "updating the name is not allowed. To change the name, "
            "delete the template and create a new one."
        ),
    )

    description = fields.Char(
        string="Description",
        help="Description of the template",
        readonly=False,
        compute="_compute_template",
    )

    body = fields.Text(
        string="Template body",
        translate=True,
        help="Code for the mjml redner template must be added here",
        readonly=False,
        compute="_compute_template",
    )

    slug = fields.Char(
        string="Slug",
        readonly=False,
        compute="_compute_template",
    )

    active = fields.Boolean(
        string="Active",
        default=True,
        help=(
            "If unchecked, it will allow you to hide the template without removing it."
        ),
    )

    is_mjml = fields.Boolean(
        string="Is MJML",
        default=True,
        help="set to false if your template doesn't contain MJML",
        readonly=False,
        compute="_compute_template",
    )

    detected_keywords = fields.Text(
        string="Variables", readonly=True, compute="_compute_keywords"
    )

    language = fields.Selection(
        string="Language",
        selection=[
            ("text/html|mustache", "HTML + mustache"),
            (LANGUAGE_MJML_MUSTACHE, "MJML + mustache"),
            (LANGUAGE_TYPST_MUSTACHE, "Typst + mustache"),
            (
                LANGUAGE_OPENDOCUMENT_MUSTACHE,
                "OpenDocument + mustache",
            ),
        ],
        default="text/html|mustache",
        help="templating language",
        readonly=False,
        compute="_compute_template",
    )

    redner_id = fields.Char(string="Redner ID", readonly=True)

    locale_id = fields.Many2one(
        comodel_name="res.lang",
        string="Locale",
        help="Optional translation language (ISO code).",
        readonly=False,
        default=lambda self: self.env.ref("base.lang_fr").id,
        compute="_compute_template",
    )

    template_data = fields.Binary(
        string="Libreoffice Template",
        readonly=False,
        compute="_compute_template_data",
        inverse="_inverse_template_data",
    )

    template_data_filename = fields.Char(
        string="Libreoffice Template Filename",
        compute="_compute_template_data_filename",
    )

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends("body", "template_data")
    def _compute_keywords(self):
        for record in self:
            record.detected_keywords = "\n".join(record.template_varlist_fetch())

    @api.depends("body", "template_data")
    def _compute_preview(self):
        for record in self:
            if record.body or record.template_data:
                response = self.get_preview(record.redner_id)

                # Check if response is valid and has content
                if response and hasattr(response, "content"):
                    record.preview = base64.b64encode(response.content)
                else:
                    record.preview = False  # If no valid response, set preview to False
            else:
                record.preview = False

    def _compute_template(self):
        """
        Computes the template values for the records and applies cached or fetched data.
        """
        for record in self:
            if not record.id or not record.redner_id:
                continue

            # Fetch the cached template
            cached_template = self._get_cached_template(record.id)

            if not any([getattr(record, f) for f in COMPUTED_FIELDS]):
                # If all computed fields are undefined, populate them
                # from the cached template.
                for f in COMPUTED_FIELDS + EDITABLE_FIELDS:
                    if f in cached_template:
                        setattr(record, f, cached_template[f])
            else:
                # If at least one field is defined, populate only undefined fields
                for f in COMPUTED_FIELDS:
                    if not getattr(record, f):
                        setattr(record, f, cached_template.get(f, None))

    def _inverse_template_data(self):
        """
        Inverse function for `template_data`. Called when `template_data` is"
        manually set.
        """
        for record in self:
            if not record.template_data or not record.id or not record.language:
                continue
            try:
                # Update the external system with the new data
                self._set_cached_template(record.id, record.template_data)
            except Exception as e:
                logger.error("Failed to update template data in Redner: %s", e)
                raise ValidationError(
                    _(
                        "Unable to update the template data. Please check the logs "
                        "for more details."
                    )
                ) from e

    def _compute_template_data(self):
        for record in self:
            # Skip records that do not have a redner_id or are missing essential data
            if not record.id or not record.redner_id:
                continue

            if (
                not record.template_data
                and record.language == LANGUAGE_OPENDOCUMENT_MUSTACHE
            ):
                cached_template = self._get_cached_template(record.id)

                template_data = (
                    cached_template.get("template_data") if cached_template else None
                )
                if template_data:
                    try:
                        # Perform base64 encoding and store the result
                        record.template_data = base64.b64encode(template_data).decode(
                            "utf-8"
                        )
                    except Exception as e:
                        logger.error(
                            "Failed to encode redner template data for record %s: %s",
                            record.id,
                            e,
                        )
                        continue  # Proceed with next record if encoding fails

    @api.depends("template_data")
    def _compute_template_data_filename(self):
        """Compute the template filename based on the template data"""
        for record in self:
            if not record.id or not record.redner_id or not record.template_data:
                record.template_data_filename = (
                    f"{record.name}.odt" if record.name else "template.odt"
                )
            else:
                try:
                    # Attempt to extract the file extension from the base64 data
                    ext = get_file_extension(record.template_data)
                    record.template_data_filename = f"{record.name}{ext}"

                except Exception:
                    logger.error("Error while computing template filename")
                    record.template_data_filename = False

    @property
    def redner(self):
        """
        Returns a Redner instance.
        Recomputes the instance if any system parameter changes.
        Uses a global variable to cache the instance across sessions.
        """
        global _redner, _redner_params

        # Fetch current system parameters
        config_model = self.env["ir.config_parameter"].sudo()
        current_params = {
            "api_key": config_model.get_param("redner.api_key"),
            "server_url": config_model.get_param("redner.server_url"),
            "account": config_model.get_param("redner.account"),
            "timeout": int(config_model.get_param("redner.timeout", default="20")),
        }

        # Check if parameters have changed or if _redner is None
        if _redner is None or _redner_params != current_params:
            # Recompute the Redner instance
            _redner = Redner(
                current_params["api_key"],
                current_params["server_url"],
                current_params["account"],
                current_params["timeout"],
            )
            _redner_params = current_params  # Update the stored parameters

        return _redner

    # -------------------------------------------------------------------------
    # LOW-LEVEL METHODS
    # -------------------------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        """Overwrite create to create redner template"""

        for vals in vals_list:
            # If "name" is missing or equals "New", set the source and
            # proceed with creation.
            if not vals.get("name", False) or vals["name"] == "New":
                vals["source"] = "redner"
                continue  # Continue processing the next record

            # Prepare template params according to the selected language.
            # Use template data field if the selected language is "od";
            # otherwise the body field is used.
            produces, language = vals.get("language", DEFAULT_LANGUAGE).split("|")
            body, body_format = (
                (vals.get("template_data", ""), "base64")
                if language == "od+mustache"
                else (vals.get("body"), "text")
            )

            locale = self.env["res.lang"].browse(vals.get("locale_id")).code

            # We depend on the API for consistency here
            # So raised error should not result with a created template
            if language and body:
                template = self.redner.templates.account_template_add(
                    language=language,
                    body=body,
                    name=vals.get("name"),
                    description=vals.get("description"),
                    produces=produces,
                    body_format=body_format,
                    version=fields.Datetime.to_string(fields.Datetime.now()),
                    locale=locale if locale else "fr_FR",
                )
                vals["redner_id"] = template["name"]
            else:
                # If the language and body are not defined, we return early
                # to prevent saving an incomplete template and sending it
                # to the Redner server.
                return self

        return super().create(vals_list)

    def write(self, vals):
        """Overwrite write to update redner template"""

        # Determine if we should update redner or not
        should = self._should_update_redner(vals)

        # Perform the write operation
        ret = super().write(vals)

        # Update Redner templates if applicable
        if should:
            for record in self:
                if (
                    not self.env.context.get("importing")  # Skip during imports
                    and record.allow_modification_from_odoo
                ):
                    record._sync_with_redner()

        return ret

    def unlink(self):
        """Overwrite unlink to delete redner template"""

        # We do NOT depend on the API for consistency here
        # So raised error should not result block template deletion
        for record in self:
            if record.redner_id and record.allow_modification_from_odoo:
                try:
                    self.redner.templates.account_template_delete(record.redner_id)
                except Exception as e:
                    logger.warning(
                        "Failed to delete Redner template with ID %s. Reason: %s",
                        record.redner_id,
                        e,
                    )
        self.env.registry.clear_cache()
        return super().unlink()

    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {}, name=_("%s (copy)") % self.name)
        return super().copy(default)

    # ------------------------------------------------------------
    # ACTIONS / BUSINESS
    # ------------------------------------------------------------

    def _should_update_redner(self, vals):
        """
        Determine if Redner should be updated based on the modified fields.
        """
        for field in COMPUTED_FIELDS + ["template_data"]:
            if field in vals:
                current_value = getattr(self, field)
                if vals[field] != current_value and vals[field]:
                    return True
        return False

    def _sync_with_redner(self):
        """
        Sync the current record's template with Redner.
        """
        self.ensure_one()
        try:
            # Check if 'language' is a valid string before splitting
            if isinstance(self.language, str) and "|" in self.language:
                produces, language = self.language.split("|")
            else:
                logger.warning(
                    "Invalid language format for record %s: %s",
                    self.id,
                    self.language,
                )
            body, body_format = (
                (self.template_data.decode(), "base64")
                if language == "od+mustache"
                else (self.body, "text")
            )

            # Use the existing `redner_id`
            redner_id = self.redner_id

            self._update_redner_template(
                template_id=redner_id,
                language=language,
                body=body,
                name=self.name,
                description=self.description,
                produces=produces,
                body_format=body_format,
                version=fields.Datetime.to_string(self.write_date),
                locale=self.locale_id.code,
            )
        except Exception as e:
            logger.error("Failed to sync with Redner template: %s", e)
            raise ValidationError(_("Failed to update Redner template, %s") % e) from e

    def _update_redner_template(self, **kwargs):
        """
        Perform the Redner `account_template_update` API call.

        :param kwargs: Payload for the `account_template_update` API.
        """
        try:
            self.redner.templates.account_template_update(**kwargs)
            self.env.registry.clear_cache()
        except Exception as e:
            logger.error("Redner API update failed: %s", e)
            raise ValueError("Unable to update the Redner template.") from e

    @ormcache("redner_id")
    def get_preview(self, redner_id):
        """
        Retrieve the preview of a Redner template by its ID.
        Returns None if the redner_id is not provided or if the preview
        cannot be retrieved.
        """
        if not redner_id:
            return None

        result = None
        try:
            result = self.redner.templates.account_template_preview(redner_id)
        except Exception as e:
            logger.error(
                "Failed to get preview of Redner template with ID %s: %s", redner_id, e
            )
        return result

    def _to_odoo_template(self, template):
        """
        Convert the external template to the Odoo format.
        """
        language = "{}|{}".format(template.get("produces"), template.get("language"))

        odoo_template = {
            "name": template.get("name"),
            "description": template.get("description", ""),
            "redner_id": template.get("name"),
            "locale_id": self.env["res.lang"].search(
                [("code", "=", template.get("locale", "fr_FR"))], limit=1
            ),
            "language": language,
            "slug": template.get("slug"),
            "is_mjml": language == LANGUAGE_MJML_MUSTACHE,
            "body": "",
            "template_data": False,
        }
        match template.get("body-format"):
            case "base64":
                body = base64.b64decode(template.get("body", ""))
            case _:
                body = template.get("body", "")
        if template.get("language") == "od+mustache":
            odoo_template["template_data"] = body
        else:
            odoo_template["body"] = body
        return odoo_template

    @ormcache("record_id")
    def _get_cached_template(self, record_id):
        """
        Retrieves and caches the template from Redner for a given record.
        """
        record = self.browse(record_id)
        if not record.redner_id:
            return {}
        try:
            # Fetch the template from the external system
            template = self.redner.templates.account_template_read(record.redner_id)
            # Convert the template to Odoo's format
            return self._to_odoo_template(template)
        except Exception as e:
            logger.error("Failed to read Redner template: %s", e)
            return {}

    @ormcache("record_id", "new_template_data")
    def _set_cached_template(self, record_id, new_template_data):
        """
        Sets and caches the template in Redner for a given record.
        """
        record = self.browse(record_id)
        if not record.redner_id:
            raise ValueError("The record must have a valid Redner ID.")

        try:
            produces, language = record.language.split("|")
            body, body_format = (
                (new_template_data.decode(), "base64")
                if language == "od+mustache"
                else (record.body, "text")
            )

            # Send the updated template to the external system
            self.redner.templates.account_template_update(
                template_id=record.redner_id,
                language=language,
                body=body,
                name=record.name,
                description=record.description,
                produces=produces,
                body_format=body_format,
                version=fields.Datetime.to_string(record.write_date),
                locale=record.locale_id.code,
            )

            self.env.registry.clear_cache()

            return True
        except Exception as e:
            logger.error("Failed to set Redner template: %s", e)
            raise ValueError("Unable to update the Redner template.") from e

    def import_from_redner(self):
        tl_wizard = self.env["template.list.wizard"]
        templates = self.list_external_templates()
        tl_wizard.populate(templates)

        return {
            "type": "ir.actions.act_window",
            "res_model": "template.list.wizard",
            "view_mode": "list",
            "view_id": self.env.ref("redner.view_template_list_wizard_tree").id,
            "target": "new",
            #'context': self.env.context,
        }

    @api.model
    def get_keywords(self):
        """Return template redner keywords"""
        self.ensure_one()

        varlist = self.template_varlist_fetch()

        for name in varlist:
            while "." in name:
                name = name[: name.rfind(".")]
                if name not in varlist:
                    varlist.append(name)

        varlist.sort()

        return varlist

    @api.model
    @ormcache("self.redner_id")
    def template_varlist_fetch(self):
        """Retrieve the list of variables present in the template."""
        self.ensure_one()
        try:
            if not self.redner_id:
                return []

            return self.redner.templates.account_template_varlist(self.redner_id)

        except Exception as e:
            logger.warning("Failed to fetch account template varlist: %s", e)
            return []

    def list_external_templates(self):
        try:
            template_list = self.redner.templates.account_template_list()
        except Exception as e:
            logger.error("Failed to list redner templates :%s", e)
            return []
        # Get the IDs of the templates that already exist in Odoo
        existing_template_ids = (
            self.env["redner.template"].search([]).mapped("redner_id")
        )
        new_templates = []
        for template in template_list:
            # Filter out templates that already exist in Odoo
            if template["name"] not in existing_template_ids:
                new_templates.append(self._to_odoo_template(template))
        return new_templates

    def redner_url(self):
        if self.redner_id is None:
            return ""

        return (
            self.redner.server_url.removesuffix(REDNER_API_PATH)
            + "template/"
            + self.redner.account
            + "/"
            + self.redner_id
        )

    def view_in_redner(self):
        return {
            "type": "ir.actions.act_url",
            "url": self.redner_url(),
            "target": "new",
        }
