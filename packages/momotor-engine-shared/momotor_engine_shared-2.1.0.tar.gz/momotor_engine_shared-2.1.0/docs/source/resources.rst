.. py:module:: momotor.shared.resources

============================
``momotor.shared.resources``
============================

Resources are used to match jobs with workers. A job can request resources, workers provide certain resources.
Either job and workers can also explicitly reject certain resources.

The :py:mod:`momotor.shared.resources` module contains the code to match requested resources with provided resources.

Currently, resources are boolean tags (ie. a worker can indicate it provides the resource "Python 3").
A future update could make it possible to use resources with numeric values
(eg. a worker can indicate it can provide up to 4 GiB of memory for the job)

Resource definition syntax
==========================

A worker defines the resources it can provide, whereas a job defines the resources it requires. The syntax for
both these definitions is the same:

.. code:: text

   group[":"]item[","item]*

The ``group`` is the name of a group, consisting of a series of alphanumeric ASCII characters, dashes (``-``),
underscores (``_``), dots (``.``) and/or whitespace. Any other character can be escaped with a backslash
character (``\``). It is also possible to use a quotes, where both single (``'``) and double quotes (``"``)
can be used. Within quotes, any character is valid. Quotes can start and end anywhere in
the string, but need to be matched in pairs. Whitespace is normally stripped from the beginning
and end of group names, but using quotes it will be retained.

The following are all valid group names:

* ``name`` - Nothing special here
* ``dotted.name`` - The dot is valid
* ``spaced name`` - Whitespace is also valid as part of the group name
* ``"email@example.com"`` - The ``@`` is not an allowed character, so the string needs to be quoted
* ``email"@"example.com`` - Only quoting the ``@``
* ``email\@example.com`` - Escaping the ``@``
* ``backslashed\\name`` - The backslash itself also needs to be escaped
* ``"trailing whitespace "`` - The whitespace at the end is retained

The first character that is not a valid character for a group name ends the group name field, so for example
a colon (``:``), a tilde (``~``) or a less-than (``<``) character all end the group name field.

A group name field is followed by an optional colon (``:``) and a list of items. The colon is only needed
if otherwise the transition from the group name field to the item list is indeterminate.

Items are separated by comma's (``,``). At least one item is required. A semi-colon (``;``), newline character
or end of string ends the list of items.

The ``item`` is the definition for an item. Items can contain any character except comma's (``,``),
colons (``:``), semi-colons (``;``), single (``'``) and double quotes (``"``), and backslashes (``\``).
Any of these characters can be escaped using the backslash (``\``), or included in quotes.
Just like with group names, whitespace is stripped, but will be retained within quotes.

The following are all valid items:

* ``string`` - Nothing special here
* ``< 1000`` - The ``<`` and space are both valid characters within an item
* ``five<6`` - So this is valid too
* ``list",of,strings"`` - We need to quote the string to use comma's in an item, item value will be ``list,of,strings``
* ``list\,of\,strings`` - The comma's can also be escaped, item value will also be ``list,of,strings``

Multiple groups can be separated by a newline character or a semi-colon (``;``)

These are all valid full resource definitions:

* ``lang: python, java`` - A group named ``lang``, containing two items ``python`` and ``java``
  The colon is needed to separate the group name from the items here
* ``memory < 1 GiB`` - A group named ``memory``, containing one item ``< 1 GiB``
  A colon separating the group name from the item is not needed here, but would be allowed
* ``version <3, >=5`` - A group named ``version``, containing two items ``<3`` and ``>=5``
* ``test case: "one; two, or more"`` - A group named ``test case``, containing one item ``one; two, or more``
* ``one: 1; two: 2`` - Two groups, one named ``one`` containing the item ``1``,
  and one named ``two`` containing the item ``2``
* .. code:: text

    one: 1
    two: 2

  Identical to ``one: 1; two: 2``


Tag type resources
------------------

There are three types of tags:

* *required tags*: defined as a name without prefix: ``tag``
* *optional tags*: prefixed with a question mark: ``?tag``
* *excluded tags*: prefixed with a tilde: ``~tag``

Workers provide tag resource. The worker can indicate tags it *requires* from the jobs, tags that
are *optional*, and *excluded* tags that it will not accept.

Jobs require tag resources. The job can indicate tags it *requires* from the worker, tags that are *optional*,
and *excluded* tags that it does not want from workers.

Matches have a strength, indicated as a floating point number ranging from negative infinity to positive infinity,
making it possible to compare them. The strongest possible match is represented as negative infinity,
and the weakest match is positive infinity.

If both the worker and job define the same *required* tag, this is considered the strongest possible match.
If both worker and job define the tag as *optional* the match is the weakest possible match.

If a tag is *excluded* by either of the parties, while the other *requires* or *optionally* defines the tag,
the match is rejected. If both *exclude* the tag, the tag is ignored.

The following table describes all possible matches:

+---------------+-----------------------------------------------+------------------------------------------------------+----------------------------------------------------+-----------------------------------------------+
| task \\ worker|  `-`                                          |  ``tag``                                             | ``?tag``                                           | ``~tag``                                      |
+---------------+-----------------------------------------------+------------------------------------------------------+----------------------------------------------------+-----------------------------------------------+
| `-`           |                                               | :py:class:`~momotor.shared.resources.NoMatch`        |                                                    |                                               |
+---------------+-----------------------------------------------+------------------------------------------------------+----------------------------------------------------+-----------------------------------------------+
| ``tag``       | :py:class:`~momotor.shared.resources.NoMatch` | :py:data:`~momotor.shared.resources.const.STRONGEST` | :py:data:`~momotor.shared.resources.const.STRONG`  | :py:class:`~momotor.shared.resources.NoMatch` |
+---------------+-----------------------------------------------+------------------------------------------------------+----------------------------------------------------+-----------------------------------------------+
| ``?tag``      |                                               | :py:data:`~momotor.shared.resources.const.WEAK`      | :py:data:`~momotor.shared.resources.const.WEAKEST` | :py:class:`~momotor.shared.resources.NoMatch` |
+---------------+-----------------------------------------------+------------------------------------------------------+----------------------------------------------------+-----------------------------------------------+
| ``~tag``      |                                               | :py:class:`~momotor.shared.resources.NoMatch`        | :py:class:`~momotor.shared.resources.NoMatch`      |                                               |
+---------------+-----------------------------------------------+------------------------------------------------------+----------------------------------------------------+-----------------------------------------------+

* `-`: worker or task does not have this tag defined
* blank cell: ignore, no change in match value
* ``NoMatch``: indicates the :py:class:`~momotor.shared.resources.NoMatch` exception will be raised
* any other value: corresponding value for the match.

If every resource tag match is a blank cell in the above table, the final match will be
:py:data:`~momotor.shared.resources.const.NEUTRAL` which is weaker than a strong match, but stronger than a weak match.

If multiple tags within the same resource group match, the *strongest* match is returned.

If multiple resource groups match, the *weakest* group determines the final value.

Note that the constants are defined the other way around:
:py:data:`~momotor.shared.resources.const.WEAKEST` > :py:data:`~momotor.shared.resources.const.STRONGEST`.
The reason for these counter intuitive values is the planned handling of value type resources, where a lower valued
match will indicate a better match.

Example: Matching programming languages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The worker defines the following tags

.. code:: text

   language: ?java, ?python
   java: ?8, ?11, ?12, ?13
   python: ?3.6, ?3.7

This worker indicates it can process Java and Python, and which versions for each

The jobs:

* .. code:: text

     language: java
     java: 12

  This job indicates it wants Java 12. The ``language`` group matches :py:data:`~momotor.shared.resources.const.STRONG`,
  the ``java`` group matches :py:data:`~momotor.shared.resources.const.NEUTRAL`, so the total match is
  :py:data:`~momotor.shared.resources.const.NEUTRAL`, because the weakest group defines the total match.
  Since the job does not have a ``python`` requirement, and the worker defines all ``python`` group tags as optional,
  this is not considered at all for the match.

* .. code:: text

     language: java
     java: 14

  This job indicates it wants Java 14. The ``language`` group matches
  :py:data:`~momotor.shared.resources.const.STRONG`, however, the ``java`` group
  produces a :py:class:`~momotor.shared.resources.NoMatch`

* .. code:: text

     language: java
     java: ?14

  This job indicates it would like Java 14. The ``language`` group match matches
  :py:data:`~momotor.shared.resources.const.STRONG` again, the ``java`` group matches
  :py:data:`~momotor.shared.resources.const.NEUTRAL`, so the total match is
  :py:data:`~momotor.shared.resources.const.NEUTRAL` again

* .. code:: text

     arch: x86

  This job does not mention any programming language, it just asks for an ``arch`` tag of ``x86``. The worker does not
  define a ``arch`` resource at all, so this will be a :py:class:`~momotor.shared.resources.NoMatch`.

* .. code:: text

     arch: ?x86

  This job also does not mention any programming language, it just asks for an *optional* ``arch`` tag of ``x86``.
  The worker does not define a ``arch`` resource group at all, it does not exclude it either.
  The final match will be :py:data:`~momotor.shared.resources.const.NEUTRAL`

* .. code:: text

     arch: ~x86

  This job explicitly rejects ``arch`` of ``x86``. However, since our worker does not define an ``arch`` resource,
  this will also result in a :py:data:`~momotor.shared.resources.const.NEUTRAL` match

Value type resources
--------------------

Not implemented yet.

This could be used to match dynamic resources like memory or disk space.

An example of a required values definition would be:

* ``ram >= 1 GiB`` - request a worker with at least 1 GiB of free RAM

An example of a provided values definition would be:

* ``ram = 2147483648`` - the worker has this amount of available RAM

Class documentation
===================

.. autoclass:: momotor.shared.resources.Resources
   :members:
   :undoc-members:
   :inherited-members:

.. autoclass:: momotor.shared.resources.group.ResourceGroup
   :members:
   :undoc-members:
   :inherited-members:

.. autoclass:: momotor.shared.resources.item.ResourceItem
   :members:
   :undoc-members:
   :inherited-members:

.. autoclass:: momotor.shared.resources.tag.Tag
   :members:
   :undoc-members:
   :inherited-members:

.. autoclass:: momotor.shared.resources.NoMatch

.. automodule:: momotor.shared.resources.const
   :members:
