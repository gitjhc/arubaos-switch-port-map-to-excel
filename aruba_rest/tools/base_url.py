from dotenv import load_dotenv
import os

load_dotenv()

def base_url(ip:str):
    if os.getenv('HTTP_SECURE', False).lower() in ['true', '1']:
        return f'https://{ip}/rest/{os.getenv("REST_VERSION", "v4")}/'
    return f'http://{ip}/rest/{os.getenv("REST_VERSION", "v4")}/'