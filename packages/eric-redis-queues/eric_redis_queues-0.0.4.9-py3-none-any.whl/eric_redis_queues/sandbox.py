import redis

r = redis.Redis(host='localhost', port=6379, db=0)
#r.set('key', 'yaaa')
print(r.get('key').decode())

print(r.client_info())
r.close()