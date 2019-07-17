# chatroom
Проект на основе django channels

Все достаточно просто
Настраиваем CHANNEL_LAYER.
используем Redis в качестве канала
"BACKEND": "asgi_redis.RedisChannelLayer"
"CONFIG": {'hosts': [('localhost', 6379)]}, 

Указываем файл роуты нашего приложения
"ROUTING": "chatroom.routing.channel_routing",


Обрабатываем события
