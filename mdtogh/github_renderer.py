import requests
import json


def github_render_content(text, gfm=False, context=None, username=None, password=None, timeout=20):
    """Renders the specified markup using the GitHub API."""
    if gfm:
        url = 'https://api.github.com/markdown'
        data = {'text': text, 'mode': 'gfm', 'context': context}
        if context:
            data['context'] = context
        data = json.dumps(data)
    else:
        url = 'https://api.github.com/markdown/raw'
        data = text
    headers = {'content-type': 'text/plain'}
    auth = (username, password) if username else None

    r = requests.post(url, headers=headers, data=data, auth=auth, timeout = timeout)

    extradata = None
    message = None
    # Relay HTTP errors
    if r.status_code != 200:
        try:
            message = r.json()['message']
        except:
            message = r.text
    extradata = {'x-ratelimit-remaining': r.headers['x-ratelimit-remaining'],
                 'x-ratelimit-limit': r.headers['x-ratelimit-limit'],
                 'x-ratelimit-reset': r.headers['x-ratelimit-reset']
            }

    return r.text, message, extradata
