twitt-back
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

Here's an example of ``twitt-back`` in action:

`http://dmerej.info/tweets <http://dmerej.info/tweets>`_

How to use it ?
---------------

* Install Python3 and then install twitt-back with ``pip``

* Edit ``~/.config/twitt-back.cfg`` to have something like::


    [twitt-back]
    user = <user>
    api_secret = <secret api>
    token_secret = <secret token>

* Then run::

    twitt-back get

This will generate ``some .json`` files with your recent tweets:

For instance, if your run it on 2016 October 10, you'll get two
files:

* ``tweets-<user>-2016-09.json`` (all the tweets from September)
* ``tweets-<user>-2016-10.json`` (all the tweets from October so far)

Of course, the last file will be overridden when you'll re-run the
script in November.

So keep these ``.json`` somewhere safe, you'll need them later,
and remember to re-run ``twitt-back get`` at least once a month.

* Then, when you are ready you can generate a completely static
  copy of your TL with::

    twitt-back gen

(By static, we mean that it's possible to upload those html files wherever
you want so it's extremely easy to publish your new TL on the web)

The best part is that since you have a copy of all your tweets as ``.json`` files,
it's easy to edit them :)

Permalinks
----------

If you want to generate permalinks, simply set ``site_url`` in the config
file::

    [twitt-back]
    site_url = http://example.com/tweets
