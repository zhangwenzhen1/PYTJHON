from urllib.request import urlopen
import re
webpage = urlopen('http://www.python.org')

text = webpage.read()
m = re.search(b'<a href="([^"]+)" .*?>about</a>', text, re.IGNORECASE)
print(m.group(1))