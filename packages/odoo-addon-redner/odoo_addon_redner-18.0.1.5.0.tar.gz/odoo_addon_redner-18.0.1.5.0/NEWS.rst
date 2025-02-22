=========
Changelog
=========

18.0.1.5.0
----------

Add typst language to redner odoo.

18.0.1.4.1
----------

Declare compatibility with changes in converter 18.0.5.0.0.

18.0.1.4.0
----------

Compatibility with changes in converter 18.0.4.0.0.

18.0.1.3.0
----------

Add neutralize script that remove configuration values.

18.0.1.2.2
----------

Improve _set_value_from_template for redner integration.

18.0.1.2.1
----------

eslint fixes.

18.0.1.2.0
----------

Improve dynamic placeholder implementation.

18.0.1.1.2
----------

Remove the hard requirement for python-magic by reusing odoo guess mimetype code and compatibility code between
different versions of python-magic.
Including the python-magic library is still recommended as Odoo uses it when available.

18.0.1.1.1
----------

Add missing python-magic requirement for package.

18.0.1.1.0
----------

Add dynamic expression button for substitution line and new converter features.

18.0.1.0.5
----------

Declare compatibility with odoo-addon-converter 18.0.3 series.

18.0.1.0.4
----------

Refactor redner.template model to improve template management.

18.0.1.0.3
----------

mail_template: add `find_or_create_partners` parameter to `_generate_template`.

18.0.1.0.2
----------

- Fix: ensure Redner instance reflects updated system parameters.
- Add python-magic as external dependency and fix print-paper-size metadata.
- Restriction Added: Disallow the deletion of a template if its source is Redner.
(Deletion is still allowed for templates created in Odoo but not for those originating from Redner.)
- Implement caching and optimization for Redner template handling.
- test: Fix timing discrepancy in Redner template version field during tests.

18.0.1.0.1
----------

Fix: Update test cases to match the API call structure.

18.0.1.0.0
----------

Initial version.
