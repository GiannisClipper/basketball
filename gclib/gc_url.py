### gc_url.py ################################################################
'''Γενική βιβλιοθήκη για τη διεκπαιρέωση url αιτημάτων'''

import urllib.request
import urllib.error
import socket

class Request(object):
  '''Manage url requests'''
  def __init__(self, **kw):
    self.ua=''
    self.charset=''
    self.timeout=10 #χρόνος αναμονής (σε δευτερόλεπτα)
    for k, v in kw.items(): setattr(self, k, v)
    socket.setdefaulttimeout(self.timeout)

  def open(self, url):
    try:
      headers={'User-Agent':self.ua}
      req=urllib.request.Request(url, headers=headers)
      with urllib.request.urlopen(req) as response:
        return True, response.read().decode(self.charset if self.charset!='' else response.headers.get_content_charset())
    except urllib.error.HTTPError as e:
      return False, ('HTTP error: ', e.code)
    except urllib.error.URLError as e:
      return False, ('Server connection failed: ', e.reason)

##############################################################################
