=========
Changelog
=========

18.0.1.8.0
----------

Compatibility with changes in converter 17.0.2.0.0.

17.0.1.7.0
----------

Add typst language to redner odoo.

17.0.1.6.0
----------

Add neutralize script that remove configuration values.

17.0.1.5.2
----------

Improve _set_value_from_template for redner integration.

17.0.1.5.1
----------

Dynamic placeholder,mimetype: code cleanup and documentation fixes.

17.0.1.5.0
----------

Fix prop validation and refactor placeholder logic.

17.0.1.4.1
----------

Fix _generate_template signature.

17.0.1.4.0
----------

Remove pypdf compatibility code to use Odoo pypdf compatibility instead.
Requires a Odoo with `[ADD] *: pypdf 3.x compatibility <https://github.com/odoo/odoo/commit/fddf53c9b6bcaea1a9ff7e041c0ccbb65a4647c8>`_.

17.0.1.3.2
----------

Also remove python-magic from odoo manifest requirements.

17.0.1.3.1
----------

Remove the hard requirement for python-magic by reusing odoo guess mimetype code and compatibility code between
different versions of python-magic.
Including the python-magic library is still recommended as Odoo uses it when available.

17.0.1.3.0
----------

- Add missing python-magic requirement for package.
- Add dynamic expression button for substitution line and new converter features.
- Refactor redner.template model to improve template management.

17.0.1.2.0
----------

- Implement caching and optimization for Redner template handling.
- Fix unlink func: log errors and refine template deletion condition.
- test: Fix timing discrepancy in Redner template version field during tests.
- Fix redner property caching and param detection.

17.0.1.1.1
----------

- Add python-magic as external dependency and fix print-paper-size metadata.

17.0.1.1.0
----------

- template-computation is now more robust and does not fail with .odt and other
  files template

17.0.1.0.0
----------

Migration to Odoo 17.
