Changelog
=========

17.0.2.0.0
----------

Fixes and changes after making the module typing compliant.

Evolve: Allow to skip update process.

Expose Context, NewinstanceType and build_context at the top level package.

Remove mail dependency, to avoid forcing its installation, only needed when using some specific converters.

Breaking change: validator package does not assume a odoo.addons package name, provide full package name instead.

Added Writeonly converter.

Add some typing information, or make it consistent.

Add more docstrings.

Fix using Skip in switch converter.

In Model converter, also validate messages in ``message_to_odoo``.

Model converter argument changed, `__type__` is now the last argument and is optional. It is expected not to be used
anymore.
Added possible_datatypes property and odoo_datatype on Converter. Defaults to empty set and None.
On Model, it can be set.

Replace generic exception.

Fix Switch converter to call post_hook.

Xref converter:

- Allow prefix on Xref converter
- Add option to include module name in messages. Incoming and outgoing message value have the same comportment.
  For example, if __converter__ is used as the module, both generated messages and received message will contain __converter__.<name>.
  Previously, generated messages would use the module name while received one would not.

17.0.1.0.1
----------

Fix RelationToMany calling undefined fonction.

17.0.1.0.0
----------

Migration to Odoo 17.
