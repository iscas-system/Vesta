import httplib
import urllib
import urllib2

get_url = "http://192.168.81.16/cgi-bin/python_test/test.py?ServiceCode=aaaa"

conn = httplib.HTTPConnection("192.168.81.16")
conn.request(method="GET",url=get_url)

response = conn.getresponse()
get_res= response.read()
print get_res



test_data = {'ServiceCode':'aaaa',
             'b':'bbbbb'}
test_data_urlencode = urllib.urlencode(test_data)

post_requrl = "http://192.168.81.16/cgi-bin/python_test/test.py"

req = urllib2.Request(url = post_requrl,data =test_data_urlencode)
print req

res_data = urllib2.urlopen(req)
res = res_data.read()
print res