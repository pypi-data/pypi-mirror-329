Changelog
=========

18.0.4.0.0
----------

In Model converter, also validate messages in ``message_to_odoo``.

Model converter argument changed, `__type__` is now the last argument and is optional. It is expected not to be used
anymore.
Added possible_datatypes property and odoo_datatype on Converter. Defaults to empty set and None.
On Model, it can be set.

Replace generic exception.

18.0.3.1.0
----------

Added Writeonly converter.

Add some typing information, or make it consistent.

Add more docstrings.

Fix using Skip in switch converter.

18.0.3.0.0
----------

Breaking change: validator package does not assume a odoo.addons package name, provide full package name instead.

18.0.2.2.0
----------

Remove mail dependency, to avoid forcing its installation, only needed when using some specific converters.

18.0.2.1.0
----------

Expose Context, NewinstanceType and build_context at the top level package.

18.0.2.0.2
----------

Evolve: Allow to skip update process.

18.0.2.0.1
----------

Fix RelationToMany calling undefined fonction.

18.0.2.0.0
----------

Fixes and changes after making the module typing compliant.

18.0.1.0.0
----------

Migration to Odoo 18.
