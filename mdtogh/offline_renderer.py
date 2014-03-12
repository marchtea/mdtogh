import markdown
import codecs

def offline_renderer(filename, encoding):
	#get toc
    with codecs.open(filename, mode='r', encoding=encoding) as f:
        text = f.read()
    return markdown.markdown(text, 
        extensions=['fenced_code',
        'codehilite(css_class=highlight)',
    ])

