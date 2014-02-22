import os
from .renderer import render_file
from .util import getDefaultPath
import settings 
import requests
import re
import sys
import shutil
import codecs

def transform(paths = None, cache_path = None, css = False, rlcss = False, gfm = False, username = None, password = None, toc = True, offline = False, refresh = False, file_reg = None):
    if len(paths) == 0:
        paths = ['.']

    #Get style file
    style, style_paths = get_style(cache_path, refresh)
    #compile file reg exp
    file_reg = '\.(md|markdown)$' if file_reg is None else file_reg
    file_reg = re.compile(file_reg, re.I)

    render_flist = []

    for path in paths:
        if not os.path.exists(path):
            print "File not found: " + path
            continue
        #TODO:
        #    add recursive support
        if os.path.isdir(path):
            path_files = os.listdir(path)
            path_files = [os.path.join(path, f) for f in path_files]
            render_flist.extend([f for f in path_files if os.path.isfile(f) and file_reg.search(f)])
        elif os.path.isfile(path):
            render_flist.append(path)
        else:
            raise ValueError('Not supported file: ' + path)
    
    print "in render_flist"
    for f in render_flist:
       print f

    tocs = []

    for f in render_flist:
        try:
            content, toc = render_file(f, css, rlcss, gfm, username, password, toc, offline, style, style_paths)
            htmlname = _get_htmlfilename(f)
            with open(htmlname, 'w') as f:
                f.write(content.encode('utf-8'))

            tocs.append([htmlname, toc])

            print "done."
        except RuntimeError as ex:
           print "Error: ", ex
        #_transform_file(path, css, rlcss, gfm, username, password, toc, offline, style, style_paths)

    for toc in tocs:
        print toc[0], ":  ", toc[1]


def _get_htmlfilename(path):
    basename = os.path.basename(path)
    filename = re.split('\.(markdown|md|)', basename)[0]
    return filename + '.html'


def _get_cached_style_files(cache_path):
    """Gets the URLs of the cached styles."""
    cached_styles = os.listdir(cache_path)
    return [os.path.join(cache_path, style) for style in cached_styles]


def _cache_style(urls, cache_path):
    """Fetches the given URLs and caches their contents in the given directory."""
    for url in urls:
        basename = url.rsplit('/', 1)[-1]
        print 'Download css file: ', basename, '...',
        file.flush(sys.stdout)
        filename = os.path.join(cache_path, basename)
        contents = requests.get(url).text
        with open(filename, 'w') as f:
            f.write(contents.encode('utf-8'))
        print 'done'
        file.flush(sys.stdout)


def _get_style_urls(cache_path):
    '''Get css urls from settings.STYLE_URLS_SOURCE
        if css files are already cached, return []
    '''
    try:
        cached = _get_cached_style_files(cache_path)
        if not cached:
            # Find css url
            print "Fetching css url from ", settings.STYLE_URLS_SOURCE,
            file.flush(sys.stdout)
            r = requests.get(settings.STYLE_URLS_SOURCE)
            if not 200 <= r.status_code < 300:
                print ' * Warning: retrieving styles gave status code', r.status_code
            urls = re.findall(settings.STYLE_URLS_RE, r.text)
            print "......done"
            print urls
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

    for style in cached_styles:
        basename = style.rsplit('/', 1)[-1]
        css_path = os.path.join(cache_path, basename)
        with codecs.open(css_path, mode='r', encoding='utf-8') as f:
            styles.append(f.read())
        file_paths.append(css_path)
    return styles, file_paths


def get_style(cache_path, refresh):
    '''Get github's css, render to html file later
        return style content
    '''
    if cache_path is None:
        cache_path = getDefaultPath()
    

    cache_path = os.path.join(cache_path, 'style_cache')
    
    #make a clean cache_path
    if refresh:
        shutil.rmtree(cache_path)

    if not os.path.exists(cache_path):
        os.makedirs(cache_path, 0755)

    style_urls = settings.STYLE_URLS[:]
    style_urls.extend(_get_style_urls(cache_path))
    styles, style_paths = _get_style_contents(style_urls, cache_path)
    return styles, style_paths

