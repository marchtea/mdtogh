from .github_renderer import github_render_content
from .toc import get_toc
from .toc import get_github_toc
from .offline_renderer import offline_renderer
from jinja2 import Environment, PackageLoader, FileSystemLoader
from bs4 import BeautifulSoup
from urllib import url2pathname
import os.path
import sys
import re

##for jinjia2
##Get template to render
env = None
content_template = None
toc_template = None
index_template = None

def init_env(template_path):
    global env, content_template, toc_template, index_template
    #global content_template
    #global toc_template
    #global index_template
    if template_path:
        env = Environment(loader=FileSystemLoader(template_path), 
                extensions=['jinja2.ext.do', 'jinja2.ext.loopcontrols'])
    else:
        env = Environment(loader=PackageLoader('mdtogh', 'templates'),
                extensions=['jinja2.ext.do', 'jinja2.ext.loopcontrols'])
    content_template = env.get_template('content.html')
    toc_template = env.get_template('toc.html')
    index_template = env.get_template('index.html')


def render_content(filename, gfm, username, password, toc, offline, encoding, timeout):
    '''render one file
        return: content, toc	
    '''
    print 'Rendering: ', filename,
    file.flush(sys.stdout)

    if offline:
        #offline_renderer, using get_toc to get toc
        if encoding is None:
            encoding = 'utf-8'
        content = offline_renderer(filename, encoding)
        gentoc = get_toc(filename, encoding)
        extradata = None
        pass
    else:
        ##using github renderer
        with open(filename) as f:
            content, message, extradata = github_render_content(f.read(), gfm, None, username, password, timeout)
            if message != None:
                raise RuntimeError('render file error: ' + message)

        gentoc = None
        if toc:
            gentoc = get_github_toc(content)

    return content, gentoc, extradata


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


def render_toc(tocs, toc_depth):
    if toc_depth is None:
        toc_depth = '2'

    if not toc_depth.isdigit():
        raise ValueError('--toc-depth must be digit')

    return toc_template.render(tocs = tocs, toc_depth = toc_depth)


def render_index(title, cover, description, toc, custom_toc):
    return index_template.render(booktitle = title, coverimage = cover,
            description = description, toc = toc, custom_toc = custom_toc)


def fix_file_link(fcontent, f, contents, file_reg):
    #fix link in file
    #fcontent: content of file to be fixed
    #f: name of file to be fixed
    #contents: files after render
    hrefreg = re.compile('^(http://|https://)')

    soup = BeautifulSoup(fcontent)
    hrefs = soup.find_all('a', href=file_reg)
    for href in hrefs:
        #fix only relative path
        if hrefreg.search(href['href']) is None:
            newpath = os.path.normpath(os.path.join(os.path.dirname(f), url2pathname(href['href'])))
            if not os.path.exists(newpath):
                print 'warning: link in ', os.path.basename(f), ': ', href['href'], ' not exists..'
            else:
                htmlname = [info[0] for info in contents if info[2] == newpath]
                if htmlname:
                    href['href'] = htmlname[0]
                else:
                    print 'warning: link in ', os.path.basename(info[2]), ': ', href['href'], ' not in render list'

    return soup.prettify() 

