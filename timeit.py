import time
from weedemout import *

username = str(raw_input("Enter Soundcloud username: "))
st = time.time()
print returnBlacklist(username)
print 'That took %.2f seconds' % (time.time() - st)

