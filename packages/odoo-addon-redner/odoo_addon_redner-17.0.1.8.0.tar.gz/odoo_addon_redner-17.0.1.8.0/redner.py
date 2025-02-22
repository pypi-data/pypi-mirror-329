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

import logging
import time
from urllib.parse import quote

import requests
import requests_unixsocket
from odoo import _  # type: ignore[import-untyped]
from odoo.exceptions import ValidationError  # type: ignore[import-untyped]

_logger = logging.getLogger(__name__)

REDNER_API_PATH = "api/v1/"


class Redner:
    def __init__(self, api_key, server_url, account, timeout):
        """Initialize the API client

        Args:
           api_key(str): provide your Redner API key.
           server_url(str): Redner server URL or socket path.
               For example: http://localhost:30001/
           timeout(float): Timeout per Redner call, in seconds.
        """

        self.api_key = api_key
        self.account = account
        self.timeout = timeout

        if server_url.startswith("/"):
            self.session = requests_unixsocket.Session()
            self.server_url = "http+unix://{}/".format(quote(server_url, safe=""))
        else:
            self.session = requests.sessions.Session()
            self.server_url = server_url
        if not self.server_url.endswith("/"):
            self.server_url += "/"
        self.server_url += REDNER_API_PATH

        self.templates = Templates(self)

    def call(self, path, http_verb="post", json=True, **params):
        """Call redner with the specified parameters.
        Delegate to ``call_impl``; this is a wrapper to have some retries
        before giving up as redner sometimes mistakenly rejects our queries.
        """

        MAX_REDNERD_TRIES = 3
        for retry_counter in range(MAX_REDNERD_TRIES):
            try:
                if json:
                    return self.call_impl_json(path, http_verb=http_verb, **params)
                return self.call_impl(path, http_verb=http_verb, **params)
            except Exception as error:
                if retry_counter == MAX_REDNERD_TRIES - 1:
                    _logger.error("Redner error: %s", str(error))
                    raise error

    def call_impl_json(self, path, http_verb="post", **params):
        """Actually make the API call with the given params -
        this should only be called by the namespace methods
        This tries to unmarshal the response

        Args:
            path(str): URL path to query, eg. '/template/'
            http_verb(str): http verb to use, default: 'post'
            params(dict): json payload

        This method can raise anything; callers are expected to catch.
        """
        r = self.call_impl(path, http_verb, **params)
        _logger.debug("Redner: Received %s", r.text)

        try:
            response = r.json()
        except Exception:
            # If we cannot decode JSON then it's an API error
            # having response as text could help debugging with sentry
            response = r.text

        if not str(r.status_code).startswith("2"):
            _logger.error("Bad response from Redner: %s", response)
            raise ValidationError(_("Unexpected redner error: %r") % response)

        return r.json()

    def call_impl(self, path, http_verb="post", **params):
        """Actually make the API call with the given params -
        this should only be called by the namespace methods

        Args:
            path(str): URL path to query, eg. '/template/'
            http_verb(str): http verb to use, default: 'post'
            params(dict): json payload

        This method can raise anything; callers are expected to catch.
        """

        if not self.server_url:
            raise ValidationError(
                _(
                    "Cannot find redner config url. "
                    "Please add it in odoo.conf or in ir.config_parameter"
                )
            )

        url = self.server_url + path

        _http_verb = http_verb.upper()
        _logger.info("Redner: Calling %s...", _http_verb)
        _logger.debug("Redner: Sending to %s > %s", url, params)
        start = time.time()

        r = getattr(self.session, http_verb, "post")(
            url,
            json=params,
            headers={"Rednerd-API-Key": self.api_key},
            timeout=self.timeout,
        )

        complete_time = time.time() - start
        _logger.info(
            "Redner: Received %s in %.2fms.",
            r.status_code,
            complete_time * 1000,
        )
        return r

    def ping(self):
        """Try to establish a connection to server"""
        conn = self.session.get(self.server_url, timeout=self.timeout)
        if conn.status_code != requests.codes.ok:
            raise ValidationError(_("Cannot Establish a connection to server"))
        return conn

    def __repr__(self):
        return f"<Redner {self.api_key}>"


class Templates:
    def __init__(self, master):
        self.master = master

    def render(
        self,
        template_id,
        data,
        accept="text/html",
        body_format="base64",
        metadata=None,
    ):
        """Inject content and optionally merge fields into a template,
        returning the HTML that results.

        Args:
            template_id(str): Redner template ID.
            data(dict): Template variables.
            accept: format of a request or response body data.
            body_format (string): The body attribute format.
                Can be 'text' or 'base64'. Default 'base64',
            metadata (dict):

        Returns:
            Array of dictionaries: API response
        """

        if isinstance(data, dict):
            data = [data]

        params = {
            "accept": accept,
            "data": data,
            "template": {"account": self.master.account, "name": template_id},
            "body-format": body_format,
            "metadata": metadata or {},
        }
        return self.master.call("render", http_verb="post", **params)

    def account_template_list(self):
        """List templates from Redner made on the redner account

        Returns:
            list(templates): Redner template List.
        """
        return self.master.call(
            f"template/{self.master.account}",
            http_verb="get",
        )

    def account_template_read(self, redner_id):
        """Fetch a template from redner given it's id

        Args:
            redner_id(string): The redner template identifier.
        Returns:
            template: Redner template.
        """
        return self.master.call(
            f"template/{self.master.account}/{redner_id}",
            http_verb="get",
        )

    def account_template_preview(self, redner_id):
        """Fetch a template preview from redner given it's id

        Args:
            redner_id(string): The redner template identifier.
        Returns:
            preview: Redner template preview in png.
        """
        return self.master.call(
            f"template/{self.master.account}/{redner_id}/preview.png",
            http_verb="get",
            json=False,
        )

    def account_template_add(
        self,
        language,
        body,
        name,
        description="",
        produces="text/html",
        body_format="text",
        locale="fr_FR",
        version="N/A",
    ):
        """Store template in Redner

        Args:
            name(string): Name of your template. This is to help the user find
                its templates in a list.
            description(string): Description of your template.
            language(string): Language your template is written with.
                Can be mustache, handlebar or od+mustache.
            body(string): Content you want to create.

            produces(string): Can be text/html or

            body_format (string): The body attribute format. Can be 'text' or
                'base64'. Default 'base64'

            locale(string):

            version(string):

        Returns:
            template: Redner template.
        """

        params = {
            "name": name,
            "description": description,
            "language": language,
            "body": body,
            "produces": produces,
            "body-format": body_format,
            "locale": locale,
            "version": version,
        }
        res = self.master.call(
            f"template/{self.master.account}",
            http_verb="post",
            **params,
        )
        return res

    def account_template_update(
        self,
        template_id,
        language,
        body,
        name="",
        description="",
        produces="text/html",
        body_format="text",
        locale="fr_FR",
        version="N/A",
    ):
        """Store template in Redner

        Args:
            template_id(string): Name of your template.
            This is to help the user find its templates in a list.
            name(string): The new template name (optional)
            description(string): Description of your template.
            language(string): Language your template is written with.
                Can be mustache, handlebar or od+mustache

            body(string): Content you want to create.

            produces(string): Can be text/html or

            body_format (string): The body attribute format. Can be 'text' or
                'base64'. Default 'base64'

            locale(string):

            version(string):

        Returns:
            template: Redner template.
        """
        params = {
            "name": name,
            "description": description,
            "language": language,
            "body": body,
            "produces": produces,
            "body-format": body_format,
            "locale": locale,
            "version": version,
        }
        res = self.master.call(
            f"template/{self.master.account}/{template_id}",
            http_verb="put",
            **params,
        )
        return res

    def account_template_delete(self, name):
        """Delete a given template name

        Args:
            name(string): Redner template Name.

        Returns:
            dict: API response.
        """
        return self.master.call(
            f"template/{self.master.account}/{name}", http_verb="delete"
        )

    def account_template_varlist(self, name):
        """Extract the list of variables present in the template.
        The list is not quaranteed to be accurate depending on the
        template language.

        Args:
            name(string): Redner template name.

        Returns:
            dict: API response.
        """

        params = {"account": self.master.account, "name": name}

        return self.master.call("varlist", **params)
