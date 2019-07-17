# chatroom
Проект на основе django channels

Настраиваем CHANNEL_LAYER.

Используем Redis в качестве канала

"BACKEND": "asgi_redis.RedisChannelLayer"

"CONFIG": {'hosts': [('localhost', 6379)]}, 

Указываем файл роутов нашего приложения

"ROUTING": "chatroom.routing.channel_routing",

Обрабатываем события
