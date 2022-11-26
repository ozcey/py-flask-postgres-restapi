'''
>>> import time
>>> import datetime
>>> s = "01/12/2011"
>>> time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple())
1322697600.0
datetime.datetime.strptime(s, "%d/%m/%Y").timestamp()
'''
import datetime

date = '01-12/2011'
unix = 0
try:
    unix = datetime.datetime.strptime(date, '%d/%m/%Y').timestamp()
except ValueError:
    print('Date format does not match')
print(unix)