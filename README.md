#Markdown to Github Html

##Motivation

Basically, You may want to convert md files into Html looks exactly like github does.

Maybe you would try [pandoc](http://johnmacfarlane.net/pandoc/index.html), but html it generates looks **not** very well(~~Just my own opinion~~).

So, I start writing this small tool, inspired by [grip](https://github.com/joeyespo/grip)

##Features

mdtogh can **convert** your md files into html files like github does with features belows:

* toc support
* index.html for your book
* next/prev files link
* file regexp to select your md files
* fix relative link(ie. `<a href="01.md"></a>` => `<a href="01.html"></a>`)
* custom template
* offline renderer(still working)

##demo


I've generate a book written by julycoding: [The-Art-Of-Programming-By-July](https://github.com/julycoding/The-Art-Of-Programming-By-July).

Demo link: [taop.marchtea.com](http://taop.marchtea.com)

You can check on that.


##Installation

From [pypi](https://pypi.python.org/pypi)

    $ pip install mdtogh 

Also, you can clone repo & install with setup.py.

	$ git clone https://github.com/marchtea/md_to_github_html.git
	$ cd md_to_github_html
	$ python setup.py install

**Maybe you will need add `sudo`**

##Usage

Generate one or more files:

	$ cd mdfiles
	$ mdtogh 01.md 02.md 03.md
	
Generate all md files in current directory:

    $ cd mdfiles
    $ mdtogh
    
Generate md files in other directory:

	$ mdtogh ../mdfiles

Generate files with file reg support:

	$ cd mdfiles
	$ mdtogh --file_reg='^\d.+\.md'

Generate files with toc & toc_depth support:

	$ cd mdfiles
	$ mdtogh --toc --toc_depth=2 --file_reg='^\d.+\.md'

Generate files with additional book info.

	$ cd mdfiles
	$ mdtogh --toc --book='book.json'
	
The format of `book.json` is given below.

Generate files with custom template:

	$ cd mdfiles
	$ mdtogh --templates=path_to_templates 01.md
	
The rules for `templates` is given below.

**Recommanded** options to `generate book`:

	$ mdtogh --css --toc --book='book.json' --file_reg='your reg exp'

**Recommanded** options to generate `several files`:

	$ mdtogh 01.md 02.md

For more options:

	mdtogh -h
	
##Something You May Notice

As to generate files exactly like github does, the easiest way is to use [api](http://developer.github.com/v3/markdown/) if offers. But it has its own [limits](http://developer.github.com/v3/#rate-limiting).

*	60 for anonymous requests an hour
*	5000 for requests using `Basic Authentication` an hour

So, you may using `--user` & `--pass` options

	$ mdtogh --user='your_github_username' --pass='your login password'
	
Your info is sent through `https` which is safe. `mdtogh` will not save any of it.


##book.json

```
{
	"title": "Demo book",
	"description": "This is a book.",
	"coverimage": "demo.jpg"
}
```
##Custom Templates Support

mdtogh now support custom templates. You can use --templates to specific where to locate templates. You should give at least three files belows:

*	content.html
*	toc.html
*	index.html

mdtogh use [jinja2](https://github.com/mitsuhiko/jinja2) as template engine.

For tutorial of template writing, please check [this](http://jinja.pocoo.org/docs/)

###content.html

`content.html` is used for generate standalone html file with things like `head`, `body` **after** content of md file is rendered by `github` or `offline renderer`.

mdtogh will pass several  parameters to `content.html` which you can use:

*	filetitle    #booktitle in book.json
*	content      #contents after render by `github` or `offline renderer`
*	toc          #not support yet
*	needtoc		 #whether toc is needed
*	prevfile     #link to prevfile. only used when `--toc` is set
*	nextfile     #link to nextfile. only used when `--toc`is set

###toc.html

mdtogh will pass parameters to `toc.html`.

###index.html



##TODO
`mdtogh` is still on developing.

Features are developing or will be add later.

*	support recursive options.
*	add toc in content.html
*	offline renderer

##Contibuting
Any **help** will be **appreciated**.

*	open issue if you find any questions
*	complete tasks in TODO list
*	add features you like
*	feel free to open pull request

##Links

* [grip](https://github.com/joeyespo/grip)
* [github markdown api](http://developer.github.com/v3/markdown/)

##Change Log

*	2014/3/6 0.0.6 add option: --encoding for offline renderer, fix relative link, add support for custom template
*	2014/3/5 0.0.5 add MANIFEST.in, fix pacakge wrapped by `setup.py`. Fix css link not include while rendering after first downloading css files
*   2014/3/4 0.0.3 fix error leads by unicode filename
*	2014/3/3 0.0.2 add --toc_depth support, fix get_html_name bug
*	2014/3/1 0.0.1 first release

##Thanks
Special thanks to [grip](https://github.com/joeyespo/grip). Without its excellent work, this tool can't be done.

