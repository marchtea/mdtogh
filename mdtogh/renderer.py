from .github_renderer import github_render_content
from .toc import get_toc
from .toc import get_github_toc
from jinja2 import Environment, PackageLoader
import os.path

##for jinjia2
##Get template to render
##TODO: add custom template support
env = Environment(loader=PackageLoader('mdtogh', 'templates'),
		extensions=['jinja2.ext.do', 'jinja2.ext.loopcontrols'])
template = env.get_template('index.html')
toc_template = env.get_template('toc.html')

def render_content(filename, gfm, username, password, toc, offline):
	'''render one file
		return: content, toc	
	'''
	print 'Rendering: ', filename
	if offline:
		#offline_renderer, using get_toc to get toc
		gentoc = get_toc(filename)
		pass

	##using github renderer
	with open(filename) as f:
		content, message = github_render_content(f.read(), gfm, None, username, password)
		if message != None:
			raise RuntimeError('render file error: ' + message)

	gentoc = None
	if toc:
		gentoc = get_github_toc(content)
	return content, gentoc


def render_with_template(title, content, toc, prevfile, nextfile, css, rlcss, styles, style_paths):
	'''
		render file using template
	'''
	#if using css, then clear styles
	#otherwise, clear style_paths
	if css:
		styles[:] = []
		if rlcss:
			style_paths = [os.path.relpath(path) for path in style_paths]
	else:
		style_paths[:] = []

	return template.render(content=content, filetitle=title,
			style_paths=style_paths, styles=styles)

def render_toc(tocs):
	return toc_template.render(tocs = tocs)

#def render_file(filename, css, rlcss, gfm, username, password, toc, offline, styles, style_paths):
	#content, toc = render_content(filename, gfm, username, password, toc, offline)

	##if using css, then clear styles
	##otherwise, clear style_paths
	#if css:
		#styles[:] = []
		#if rlcss:
			#style_paths = [os.path.relpath(path) for path in style_paths]
	#else:
		#style_paths[:] = []

	#print "start render..."	

	#return template.render(content=content, filename=filename,
			#style_paths=style_paths, styles=styles), toc
