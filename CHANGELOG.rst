v0.5.2 - 2016-10-07
-------------------

* Nicer search:

  * Limit number of search results
  * Display pattern in results page
  * Display an error when nothing is found

v0.5.1 - 2016-10-07
-------------------

* Packaging changes for Pypi

v0.5 - 2016-10-07
------------------

* Include user data (such as full name, description and location) in the
  generated pages

v0.4.1 - 2016-09-17
-------------------

* search: return 404 early if the user does not exist
  (this fixes a potential SQL injection)

v0.4 - 2016-08-27
-----------------

* Implement search via a simple `flask <http://flask.pocoo.org/>`_ application,
  using a ``.sqlite`` database

* Include a link to the original tweet in the HTML output

* Include tweet contents in feed summary

* Allow to retrieve tweet but not publish them. To do this, patch the
  configuration file to have:

.. code-block:: ini

  [[users]]

  [users.<name>]
  publish = false

v0.3 - 2016-05-05
-----------------

* Work incrementally: only fetches new tweets since last dump. This means you
  can edit or remove old tweets :)

* Multi-user support

* Generate one atom feed per user. This allows to follow some user's tweets,
  by using `RSS`, without having to create an account on Twitter first.

v0.2 - 2016-04-09
-----------------

* First public release

v0.1 - 2016-04-08 - 2016-04-09
------------------------------

* Glorious sleepless hacking night
