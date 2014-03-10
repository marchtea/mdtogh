from urllib import quote_plus
import markdown
import codecs
from bs4 import BeautifulSoup

def get_toc(filename, encoding):
	#get toc
	input_file = codecs.open(filename, mode='r', encoding=encoding)
	text = input_file.read()
	input_file.close()
	md = markdown.Markdown(extensions=['toc', 'fenced_code'], extension_configs={'toc': [('slugify', github_link_renderer)]})
	md.convert(text)

	#convert to toc list
	soup = BeautifulSoup(md.toc)
	tocs = _toc(soup.select('div > ul > li'))

	return tocs 


def _toc(toc_list, level = 1):
	menus = []
	for li in toc_list:
		menu = [ ['h%d' % level, li.a.get_text(), li.a.attrs['href']] ]
		#menu = [ [li.a.get_text(), li.a.attrs['href']] ]
		if li.ul is not None:
			menu.extend(_toc(li.ul.find_all('li', recursive=False), level+1))
		menus.extend(menu)
	return menus


def github_link_renderer(link, md):
	'''
		get github-like heading href.
	'''
	link = link.lower().replace(' ', '-').replace('+', '')
	return quote_plus(link.encode('utf-8'))


def get_github_toc(content):
	soup = BeautifulSoup(content)
	toclinks = soup.select('a.anchor span.octicon.octicon-link')
	tocs = []
	for link in toclinks:
		a = link.parent
		h = a.parent
		tocs.append([h.name, h.get_text(strip=True), a.attrs['href']])

	return tocs


