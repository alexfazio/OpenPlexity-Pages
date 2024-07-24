import urllib.parse
import urllib.request
from http.cookies import SimpleCookie
import json
import os
import ssl
from dotenv import load_dotenv
import certifi
import re

load_dotenv()


# Custom HTTP client for making requests
class UrllibClient:
    def __init__(self):
        self.cookie_jar = urllib.request.HTTPCookieProcessor()
        context = ssl.create_default_context(cafile=certifi.where())
        self.opener = urllib.request.build_opener(self.cookie_jar, urllib.request.HTTPSHandler(context=context))
        urllib.request.install_opener(self.opener)

    # Perform GET request
    def get(self, url, headers={}):
        request = urllib.request.Request(url, headers=headers)
        return self._request(request)

    # Perform POST request
    def post(self, url, data=None, headers={}):
        postdata = urllib.parse.urlencode(data).encode()
        request = urllib.request.Request(url, postdata, headers)
        return self._request(request)

    # Execute the request and process the response
    def _request(self, request):
        response = self.opener.open(request)
        response.status_code = response.getcode()
        response.data = response.read().decode('utf-8')
        return response


# Create a new Rentry post
def new_rentry(url, edit_code, text):
    client, cookie = UrllibClient(), SimpleCookie()
    base_url = os.getenv('BASE_URL', 'https://rentry.co')
    headers = {"Referer": base_url}

    cookie.load(vars(client.get(base_url))['headers']['Set-Cookie'])
    csrftoken = cookie['csrftoken'].value

    payload = {
        'csrfmiddlewaretoken': csrftoken,
        'url': url,
        'edit_code': edit_code,
        'text': text
    }

    return json.loads(client.post(f"{base_url}/api/new", payload, headers=headers).data)


def strip_html_tags(text):
    return re.sub('<[^<]+?>', '', text)

# Export content to Rentry and return the URL and edit code
def export_to_rentry(content):
    cleaned_content = strip_html_tags(content)
    url = ''  # Leave empty for random URL
    edit_code = ''  # Leave empty for random edit code
    response = new_rentry(url, edit_code, cleaned_content)
    if response['status'] == '200':
        return response['url'], response['edit_code']
    else:
        return None, None