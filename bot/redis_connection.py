import json

from redis import Redis

redis_connection=Redis()
# #
# redis_connection.mset({'1140762398': json.dumps({
#     'phone_number': '904111879'
# })})

#
# redis_connection.delete('1140762398')