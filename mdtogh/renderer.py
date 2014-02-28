from .github_renderer import github_render_content
from .toc import get_toc
from .toc import get_github_toc
from jinja2 import Environment, PackageLoader
import os.path

##for jinjia2
##Get template to render
env = Environment(loader=PackageLoader('mdtogh', 'templates'),
		extensions=['jinja2.ext.do', 'jinja2.ext.loopcontrols'])
content_template = env.get_template('content.html')
toc_template = env.get_template('toc.html')
index_template = env.get_template('index.html')

def render_content(filename, gfm, username, password, toc, offline):
	'''render one file
		return: content, toc	
	'''
	print 'Rendering: ', filename,
	if offline:
		#offline_renderer, using get_toc to get toc
		content = ''
		gentoc = get_toc(filename)
		pass
	else:
		##using github renderer
		with open(filename) as f:
			content, message = github_render_content(f.read(), gfm, None, username, password)
			if message != None:
				raise RuntimeError('render file error: ' + message)

		gentoc = None
		if toc:
			gentoc = get_github_toc(content)

	return content, gentoc


def render_with_template(title, content, toc, prevfile, nextfile, css, abscss, needtoc, styles, style_paths):
	'''
		render file using template
	'''
	#if using css, then clear styles
	#otherwise, clear style_paths
	if css:
		styles[:] = []
		if not abscss:
			style_paths = [os.path.relpath(path) for path in style_paths]
	else:
		style_paths[:] = []

	return content_template.render(content=content, filetitle=title,
			style_paths=style_paths, styles=styles, toc = toc, needtoc = needtoc, 
			prevfile = prevfile, nextfile = nextfile)


def render_toc(tocs):
	return toc_template.render(tocs = tocs)


def render_index(title, cover, description, toc):
	return index_template.render(booktitle = title, coverimage = cover,
			description = description, toc = toc)

