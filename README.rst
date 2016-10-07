static_tl
==========

.. image:: http://img.shields.io/pypi/v/static_tl.svg
  :target: https://pypi.python.org/pypi/static_tl

What is it?
-----------

It' a tool that makes sure your TL won't be gone for ever if for some
reason twitter decides to no longer play nice.

In a way, it also makes it possible to:

* edit your tweets
* have them longer than 140 characters

Show me!
--------

Here's an example of ``static_tl`` in action:

`http://dmerej.info/tweets <http://dmerej.info/tweets>`_

How to use it ?
---------------

* Install Python3 and then install ``static_tl`` with ``pip``

* Create an app on ``http://apps.twitter.com``

* Edit ``~/.config/static_tl.toml`` to have something like:

  .. code-block:: ini

    [auth]
    api_key = "<Consumer Key>"
    api_secret = "<Consumer Secret>"

    token = "<Acces Token>"
    token_secret = "<Acess Token Secret>"

    [[users]]

    [users.user_one]
    with_replies = false

    [users.user_two]
    with_replies = true

* Then run::

    static-tl get

This will generate some files with your recent tweets in a ``json``
folder.

For instance, if your run it on 2016 October 10, you'll get two
files:

* ``json/<user>/2016-09.json`` (all the tweets from September)
* ``json/<user>/2016-10.json`` (all the tweets from October so far)

* Next time you'll run ``static-tl get``, we will look at the most recent
  status ID in the most recent ``.json`` file and only fetch new tweets.
  This means you can edit or even delete the tweets that are older than
  that :)

* Then, when you are ready you can generate a completely static
  copy of your TL with::

    static-tl gen

(By static, we mean that it's possible to upload those html files wherever
you want so it's extremely easy to publish your new TL on the web)


Permalinks and feeds
---------------------

If you want to generate permalinks, simply add ``site_url`` at the
top of the ``.toml`` file::

    site_url = http://example.com/tweets


By doing so, ``static-tl gen`` will also generate a ``<user>/feed.atom`` feed
so that people can be notified about your new tweets via RSS instead of having
to create an account on twitter :)

Tweaking the output
--------------------

Customization can be done by simply editing the ``Jinja`` templates in ``static_tl/templates``.

From the template you have access to all the fields returned by the official
twitter API.

Also, any file not ending with ``.html`` in the ``templates`` folder will be
copied directly to the ``html`` folder: useful for images, ``css`` files and
the like.

Perform backup only
---------------------

If you do not want to generate HTML files for a given user, use:

.. code-block:: ini

  [[users]]

  [users.<name>]
  publish = false


Searching
----------

Since version 0.4, ``static_tl gen`` also generates a ``tweets.sqlite`` file
containing one table per user.

We use the ``FTS4`` extension.

A search application is available in the sources : ``static_tl/search.py``,
using the `flask <http://flask.pocoo.org/>`_ framework.

This will only work if ``site_url`` is set, and
if the ``flask`` server can be reached at  ``<site_url>/search``
