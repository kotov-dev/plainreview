#!/usr/bin/python
import os
import urllib2
import urllib

diff = os.popen("git diff origin master")
diff_text = diff.read()
print diff_text


description = raw_input("Description: ")
reviewers = raw_input("Reviewers: ")


url = 'http://127.0.0.1:8000/upload-review/'
values = {
    'diff': diff_text,
    'description': description,
    'reviewers': reviewers,
    'project_id': 1
}

data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
result = response.read()
print result
