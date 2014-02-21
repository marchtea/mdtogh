import os
from .renderer import render_file
from .util import getDefaultPath
import settings 
import requests
import re

def transform(path = None, cache_path = None, inline = None, abscss = None, gfm = False, username = None, password = None, toc = True, offline = False):
    if path == None:
        path = '.'
    if not os.path.exists(path):
        raise ValueError('File not found: ' + path)

    style, style_paths = get_style(cache_path)

    if os.path.isdir(path):
        pass
    elif os.path.isfile(path):
        try:
            content, toc = render_file(path, gfm, username, password, toc, offline)
            f = open('tmp.html', 'w')
            f.write(content)
            f.close()
            print "done."
        except RuntimeError as ex:
            print "Error: ", ex
    else:
        raise ValueError('Not supported file: ' + path)



def _get_cached_style_files(cache_path):
    """Gets the URLs of the cached styles."""
    cached_styles = os.listdir(cache_path)
    return [os.path.join(cache_path, style) for style in cached_styles]

def _cache_style(urls, cache_path):
    """Fetches the given URLs and caches their contents in the given directory."""
    for url in urls:
        basename = url.rsplit('/', 1)[-1]
        print 'Download css file: ', basename, '...',
        filename = os.path.join(cache_path, basename)
        contents = requests.get(url).text
        with open(filename, 'w') as f:
            f.write(contents.encode('utf-8'))
        print 'done'

def _get_style_urls(cache_path):
    '''Get css urls from settings.STYLE_URLS_SOURCE
        if css files are already cached, return []
    '''
    try:
        cached = _get_cached_style_files(cache_path)
        if not cached:
            # Find css url
            print "Fetching css url from ", settings.STYLE_URLS_SOURCE,
            r = requests.get(settings.STYLE_URLS_SOURCE)
            if not 200 <= r.status_code < 300:
                print ' * Warning: retrieving styles gave status code', r.status_code
            urls = re.findall(settings.STYLE_URLS_RE, r.text)
            print "......done"
            return urls

            ##cache style files 
            #_cache_style(urls, cache_path)
            #cached = _get_cached_style_files(cache_path)
    except Exception as ex:
        print '* Error: Retrive style error:', str(ex)
    return []

def _get_style_contents(urls, cache_path):
    '''fetching css file content, cache if not exists
       return contents, file_paths
    '''
    styles = []
    file_paths = []
    cached_styles = os.listdir(cache_path)
    for url in urls:
        basename = url.rsplit('/', 1)[-1]
        if basename not in cached_styles:
            _cache_style([url], cache_path)
        css_path = os.join(cache_path, basename)
        with open(css_path, 'r') as f:
            styles.extend(f.read())
        file_paths.extend(css_path)
    return styles, file_paths

def get_style(cache_path):
    '''Get github's css, render to html file later
        return style content
    '''
    if cache_path is None:
        cache_path = getDefaultPath()
    
    print "cache_path", cache_path

    cache_path = os.path.join(cache_path, 'style_cache')
    if not os.path.exists(cache_path):
        os.makedirs(cache_path, 0755)
    style_urls = settings.STYLE_URLS[:]

    style_urls.extend(_get_style_urls(cache_path))
    styles, style_paths = _get_style_contents(style_urls, cache_path)
    return styles, style_paths

