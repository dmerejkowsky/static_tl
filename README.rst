static_tl
==========

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

* Install Python3 and then install static_tl with ``pip``

* Create an app on ``http://apps.twitter.com``

* Edit ``~/.config/static_tl.cfg`` to have something like::


    [static_tl]
    user = <user>
    api_key = <Consumer Key>
    api_secret = <Consumer Secret>
    token = <Access Token>
    token_secret = <Access Token Secret>

* Then run::

    static-tl get

This will generate some ``tweets-<year>-<month>.json`` files with your recent tweets.

For instance, if your run it on 2016 October 10, you'll get two
files:

* ``tweets-2016-09.json`` (all the tweets from September)
* ``tweets-2016-10.json`` (all the tweets from October so far)

Of course, the last file will be overridden when you'll re-run the
script in November.

So keep these ``.json`` somewhere safe, you'll need them later,
and remember to re-run ``static-tl get`` at least once a month.

* Then, when you are ready you can generate a completely static
  copy of your TL with::

    static-tl gen

(By static, we mean that it's possible to upload those html files wherever
you want so it's extremely easy to publish your new TL on the web)

The best part is that since you have a copy of all your tweets as ``.json`` files,
it's easy to edit them :)

Permalinks
----------

If you want to generate permalinks, simply set ``site_url`` in the config
file::

    [static_tl]
    site_url = http://example.com/tweets
