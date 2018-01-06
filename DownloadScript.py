"""import urllib3"""

url = "https://github.com/git-for-windows/git/releases/download/v2.15.1.windows.2/PortableGit-2.15.1.2-32-bit.7z.exe"

"""file_name = url.split('/')[-1]
u = urllib3.urlopen(url)
f = open(file_name, 'wb')
meta = u.info()
file_size = int(meta.getheaders("Content-Length")[0])
print ("Downloading: %s Bytes: %s" % (file_name, file_size))

file_size_dl = 0
block_sz = 8192
while True:
    buffer = u.read(block_sz)
    if not buffer:
        break

    file_size_dl += len(buffer)
    f.write(buffer)
    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    status = status + chr(8)*(len(status)+1)
    print (status)

f.close()"""
"""import urllib
urllib.request.urlretrieve ("https://github.com/git-for-windows/git/releases/download/v2.15.1.windows.2/PortableGit-2.15.1.2-32-bit.7z.exe", "git.exe")
"""
print("Start")
import urllib3
http = urllib3.PoolManager()
r = http.request('GET', url, preload_content=False)

with open(path, 'wb') as out:
    while True:
        data = r.read(chunk_size)
        if not data:
            break
        out.write(data)

r.release_conn()
print(data)
