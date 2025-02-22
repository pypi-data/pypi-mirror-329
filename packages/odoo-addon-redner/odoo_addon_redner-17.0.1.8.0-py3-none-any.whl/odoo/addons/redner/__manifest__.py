##############################################################################
#
#    Redner Odoo module
#    Copyright © 2016, 2023-2025 XCG Consulting <https://xcg-consulting.fr>
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

{
    "name": "Redner",
    "license": "AGPL-3",
    "version": "17.0.1.8.0",
    "category": "Reporting",
    "author": "XCG Consulting",
    "website": "https://orbeet.io/",
    "summary": "Odoo addon to use redner (producer of reports and emails)",
    # converter: https://orus.io/xcg/odoo-modules/converter
    "depends": ["converter", "mail", "web"],
    "data": [
        "wizard/mail_compose_message_views.xml",
        "wizard/template_list_view.xml",
        "security/ir.model.access.csv",
        "views/redner_template.xml",
        "views/mail_template.xml",
        "views/ir_actions_report.xml",
        "views/menu.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "redner/static/src/js/redner_report_action.esm.js",
            "redner/static/src/components/**/*",
        ],
    },
    "installable": True,
    "external_dependencies": {"python": ["requests_unixsocket"]},
    "images": ["static/description/thumbnail.png"],
}
