import httpx
r = httpx.get('')
print(r.content)