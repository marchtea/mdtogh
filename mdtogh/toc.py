from urllib import quote_plus
import markdown
import codecs

def get_toc(filename):
	input_file = codecs.open(filename, mode='r', encoding='utf-8')
	text = input_file.read()
	md = markdown.Markdown(extensions=['toc'], extension_configs={'toc': [('slugify', github_link_renderer)]})
	md.convert(text)
	return md.toc


def github_link_renderer(link, md):
	'''
		get github-like heading href.
	'''
	link = link.lower().replace(' ', '-').replace('+', '')
	return quote_plus(link.encode('utf-8'))
