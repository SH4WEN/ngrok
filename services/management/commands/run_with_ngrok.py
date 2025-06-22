from pyngrok import ngrok
from django.core.management.commands.runserver import Command as Runserver
from django.conf import settings

class Command(Runserver):
    def handle(self, *args, **options):
        # Start ngrok when the server starts
        http_tunnel = ngrok.connect(addr='8000', bind_tls=True)
        print(f'Public URL: {http_tunnel.public_url}')
        
        # Update ALLOWED_HOSTS with the ngrok URL
        ngrok_host = http_tunnel.public_url.replace('https://', '').replace('http://', '')
        settings.ALLOWED_HOSTS.append(ngrok_host)
        
        super().handle(*args, **options)