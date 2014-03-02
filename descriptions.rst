==========================
Markdown to Github Html
==========================

Motivation
===============

Basically, You may want to convert md files into Html looks exactly like github does.

Maybe you would try `pandoc`_, but html it generates looks **not** very well(~~Just my own opinion~~).

So, I start writing this small tool, inspired by `grip`_

Features
=================

mdtogh can **convert** your md files into html files like github does with features belows:

- toc support
- index.html for your book
- next/prev files link
- file regexp to select your md files
- custom template(still working)
- offline renderer(still working)

demo
=================

I've generate a book written by julycoding: `The-Art-Of-Programming-By-July`_.

Demo link: `taop.marchtea.com`_

You can check on that.


Installation
==============

From `pypi`_

.. code-block:: bash

    $ pip install mdtogh 

Also, you can clone repo & install with setup.py.

.. code-block:: bash

	$ git clone https://github.com/marchtea/md_to_github_html.git
	$ cd md_to_github_html
	$ python setup.py install

**Maybe you will need add `sudo`**

Usage
==================

Generate one or more files

.. code-block:: bash
    $ cd mdfiles
	$ mdtogh 01.md 02.md 03.md
	
Generate all md files in current directory

.. code-block:: bash

    $ cd mdfiles
    $ mdtogh
    
Generate md files in other directory

.. code-block:: bash

	$ mdtogh ../mdfiles

Generate files with file reg support

.. code-block:: bash

	$ cd mdfiles
	$ mdtogh --file_reg='^\d.+\.md'

Generate files with toc support

.. code-block:: bash

	$cd mdfiles
	$ mdtogh --toc --file_reg='^\d.+\.md'

Generate files with additional book info

.. code-block:: bash

	$cd mdfiles
	$ mdtogh --toc --book='book.json'
	
The format of `book.json` is given below.

**Recommanded** options to `generate book`

.. code-block:: bash

	$ mdtogh --css --toc --book='book.json' --file_reg='your reg exp'

**Recommanded** options to generate `several files`

.. code-block:: bash

	$ mdtogh 01.md 02.md

For more options

.. code-block:: bash

	mdtogh -h
	
Something You May Notice
=================================

As to generate files exactly like github does, the easiest way is to use
`api`_ if offers. But it has its own `limits`_.

-	60 for anonymous requests an hour
-	5000 for requests using `Basic Authentication`

So, you may using `--user` & `--pass` options

	$ mdtogh --user='your_github_username' --pass='your login password'
	
Your info are sended through `https` which is safe. `mdtogh` will not save any your info.


book.json
========================

.. code-block:: javascript 
    {
        "title": "Demo book",
        "description": "This is a book.",
        "coverimage": "demo.jpg"
    }

TODO
===================
`mdtogh` is still on developing.

Features is developing or will be add later.

-	max toc level
-	support recursive options.
-	custom html template
-	add toc in content.html
-	show ratelimit-remaining after generate complete
-	offline renderer

Contibuting
===============

Any help will be **appreciated**.

-	open issues if you find any questions
-	complete one in TODO list

Links
=====================

- `Github repo`_
- `grip`_
- `github markdown api`_

Thanks
==========

Special thanks to `grip`_. Without its excellent work, this tools can't be done.

.. _limits: http://developer.github.com/v3/#rate-limiting
.. _api: http://developer.github.com/v3/markdown/
.. _github markdown api: http://developer.github.com/v3/markdown/
.. _pypi: https://pypi.python.org/pypi
.. _grip: https://github.com/joeyespo/grip
.. _pandoc: http://johnmacfarlane.net/pandoc/index.html
.. _The-Art-Of-Programming-By-July: https://github.com/julycoding/The-Art-Of-Programming-By-July
.. _taop.marchtea.com: http://taop.marchtea.com

.. _Github repo: http://github.com/marchtea/mdtogh
