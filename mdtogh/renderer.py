from .github_renderer import github_render_content
from .toc import get_toc
from jinja2 import Environment, PackageLoader
import os.path

##for jinjia2
##Get template to render
##TODO: add custom template support
env = Environment(loader=PackageLoader('mdtogh', 'templates'))
template = env.get_template('index.html')

def render_content(filename, gfm, username, password, toc, offline):
	'''render one file
		return: content, toc	
	'''
	print 'Rendering: ', filename
	if offline:
		#offline_renderer	
		pass
	with open(filename) as f:
		content, message = github_render_content(f.read(), gfm, None, username, password)
		if message != None:
			raise RuntimeError('render file error: ' + message)

	gentoc = None
	if toc:
		gentoc = get_toc(filename)
	return content, gentoc


def render_file(filename, css, rlcss, gfm, username, password, toc, offline, styles, style_paths):
	'''
		render file using template
		return:
			content, toc
	'''
	content, toc = render_content(filename, gfm, username, password, toc, offline)

	#if using css, then clear styles
	#otherwise, clear style_paths
	if css:
		styles[:] = []
		if rlcss:
			style_paths = [os.path.relpath(path) for path in style_paths]
	else:
		style_paths[:] = []

	print "start render..."	

	return template.render(content=content, filename=filename,
			style_paths=style_paths, styles=styles), toc
