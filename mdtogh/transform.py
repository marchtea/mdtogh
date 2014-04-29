import os
from .renderer import render_content
from .renderer import render_with_template
from .renderer import render_toc
from .renderer import render_index
from .renderer import fix_file_link
from .renderer import init_env
from .util import getDefaultPath
from datetime import datetime
import settings 
import requests
import re
import sys
import shutil
import codecs
import json

def transform(paths = None, cache_path = None, system_css = False, css = False, abscss = False, gfm = False, username = None, password = None, needtoc = True, toc_depth = None, toc_file = None, book = '', offline = False, encoding = 'utf-8', refresh = False, file_reg = None, template_path = None, timeout = 20):

    #first, initial enviroment for jinjia2
    init_env(template_path)

    if len(paths) == 0:
        paths = ['.']

    #Get style file
    styles, style_paths = get_style(cache_path, system_css, refresh)
    #compile file reg exp
    file_reg = '\.(md|markdown)$' if file_reg is None else file_reg
    file_reg = re.compile(file_reg, re.I|re.U)

    render_flist = []

    for path in paths:
	if not os.path.exists(path):
	    print "File not found: " + path
	    continue
	#TODO:
	#    add recursive support
	if os.path.isdir(path):
	    path_files = os.listdir(path)
            path_files = [os.path.join(path, f) for f in path_files if file_reg.search(f)]
            render_flist.extend([os.path.abspath(f) for f in path_files if os.path.isfile(f)])
        elif os.path.isfile(path):
                render_flist.append(os.path.abspath(path))
        else:
                raise ValueError('Not supported file: ' + path)
    
    #print "in render_flist"
    #for f in render_flist:
      #print f

    print len(render_flist), " files in render list..." 

    timeout = float(timeout)

    contents = []
    tocs = []
    exception_occur = False
    extradata = None

    #load pickled data
    ##loadxxxx
    if not refresh:
        contents, tocs = __load_content_toc(offline)

    #get all file rendered using github api or offline renderer
    #Also, get toc
    try:
        for i, f in enumerate(render_flist):
            print i+1, "/", len(render_flist), ": ",
            rf_stat = os.stat(f)
            if len([content[2] for content in contents if content[2] == f and content[3] == rf_stat.st_mtime]):
               print "File not changed, skip..."
               continue
                
            content, toc, extradata = render_content(f, gfm, username, password, needtoc, offline, encoding, timeout)
            htmlname = __get_htmlfilename(f)
            contents.append([htmlname, content, f, rf_stat.st_mtime])
            if needtoc:
                tocs.extend(__process_toc(toc, htmlname))

            print "done."
    except requests.RequestException as e:
        print "\nError occur when request for github: ", e
        exception_occur = True

    #save renderer data 
    __save_content_toc(contents, tocs, offline)

    #if exception occured, exit
    if exception_occur:
        print "Network error, please try again later"
        return
    

    #fix relative links: 01.md => 01.html
    for i, info in enumerate(contents): 
        contents[i][1] = fix_file_link(info[1], info[2], contents, file_reg)

    if needtoc:
        if toc_file:
            print 'toc_file:', toc_file
            toc_file = os.path.abspath(toc_file)
            print 'Generating custom toc'
            try:
                rtoc, toc, extradata = render_content(toc_file, gfm, username, password, False, offline, encoding, timeout)
            except requests.RequestException as e:
                print "\nError occur when request for github: ", e
                return

            print 'done.'
            rtoc = fix_file_link(rtoc, toc_file, contents, file_reg)
        else:
            rtoc = render_toc(tocs, toc_depth)

        ##after render toc, we render index
        bookinfo = __get_book_conf(book)
        print 'Generating index.html'
        if bookinfo:
            book_index = render_index(bookinfo['title'], bookinfo['coverimage'], bookinfo['description'], rtoc, True if toc_file else False)
        else:
            book_index = render_index('', '', '', rtoc, True if toc_file else False)
        with open('index.html', 'w') as f:
            f.write(book_index.encode('utf-8'))
    else:
        rtoc = None

    #After get all file rendered, render them with template & save into files
    for i in range(len(contents)):
        p = contents[i - 1][0] if i > 0 else None 
        n = contents[i + 1][0] if i + 1 != len(contents) else None

        rendered = render_with_template('', contents[i][1], rtoc, p, n, css, abscss, needtoc, styles, style_paths)
        with open(contents[i][0], 'w') as f:
            f.write(rendered.encode('utf-8'))

    print 'All finished'
    if extradata:
        print "Github API rate remains: ", extradata['x-ratelimit-remaining'], "/", extradata['x-ratelimit-limit'], "."
        print "Reset at: ", datetime.fromtimestamp(float(extradata['x-ratelimit-reset']))



def __get_book_conf(book):
    if book:
        book = os.path.expanduser(book)
        if not os.path.exists(book):
            raise RuntimeError(book+' not exists')
        with open(book, 'r') as f:
            bookinfo = json.load(f)
        return bookinfo
    return None 


def __get_htmlfilename(path):
    basename = os.path.basename(path)
    filename = re.split('\.(markdown|md)', basename, re.U)[0]
    return unicode(filename + '.html', 'utf-8')


def __process_toc(toc, htmlname):
    ##process toc, add htmlname into link
    for header in toc:
        header[2] = htmlname + header[2]
    return toc



def _get_cached_style_files(cache_path):
    """Gets the URLs of the cached styles."""
    cached_styles = os.listdir(cache_path)
    return [os.path.join(cache_path, style) for style in cached_styles]


def _cache_style(urls, cache_path):
    """Fetches the given URLs and caches their contents in the given directory."""
    for url in urls:
        basename = url.rsplit('/', 1)[-1]
        print '\tDownload css file: ', basename, '...',
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
            print "Github css files are not cached. Download First"
            print "Fetching css url from ", settings.STYLE_URLS_SOURCE,
            file.flush(sys.stdout)
            r = requests.get(settings.STYLE_URLS_SOURCE)
            if not 200 <= r.status_code < 300:
                print ' * Warning: retrieving styles gave status code', r.status_code
                raise RuntimeError('Get css file failed')
            urls = re.findall(settings.STYLE_URLS_RE, r.text)
            print "......done"
            return urls

    except Exception as ex:
        print ''
        raise RuntimeError('Retrieve style error:' + str(ex))
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

    cached_styles = os.listdir(cache_path)

    for style in cached_styles:
        basename = style.rsplit('/', 1)[-1]
        css_path = os.path.join(cache_path, basename)
        with codecs.open(css_path, mode='r', encoding='utf-8') as f:
            styles.append(f.read())
        file_paths.append(css_path)
    return styles, file_paths


def get_style(cache_path, system_css, refresh):
    '''Get github's css, render to html file later
        return style content
    '''
    if cache_path is None:
        cache_path = os.path.curdir
    if system_css:
        cache_path = getDefaultPath()

    cache_path = os.path.expanduser(cache_path)

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


def __save_content_toc(contents, toc, offline):
    with open(".md_cache", "wb") as f:
        import pickle
        pickle.dump([offline, contents, toc], f)


def __load_content_toc(offline):
    contents = []
    tocs = []

    try:
        with open(".md_cache", "rb") as f:
            import pickle
            ofl, contents, tocs = pickle.load(f)
            if ofl != offline:
                contents = []
                tocs = []
    except:
        pass


    return contents, tocs

