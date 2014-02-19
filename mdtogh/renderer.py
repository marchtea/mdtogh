from .github_renderer import render_content
from .toc import get_toc

def render_file(filename, gfm, username, password, toc, offline):
	'''render one file
		return: content, toc	
	'''
	print 'Rendering: ', filename
	if offline:
		#offline_renderer	
		pass
	with open(filename) as f:
		content, message = render_content(f.read(), gfm, None, username, password)
		if message != None:
			raise RuntimeError('render file error: ' + message)

	toc = None
	if toc:
		toc = get_toc(filename)
	return content, toc

