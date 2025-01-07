# import json
# import logging

# from pyngrok import ngrok

# # from config_reader import config


# def start_ngrok(port: int = 8000) -> str | None:
#     try:
#         # ngrok.set_auth_token(auth_token)

#         http_tunnel = ngrok.connect(port)
#         ngrok_url = http_tunnel.public_url
            
#         return ngrok_url
#     except Exception as e:
#         logging.error(f"Error getting ngrok URL: {e}")
#         return None
        
        
# def stop_ngrok(public_url: str) -> None:
#     ngrok.disconnect(public_url)
#     ngrok.kill()


