from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS")
ENV = os.getenv("ENV")
DOMAIN = "localhost" if ENV == "dev" else "coronavirusmap.london-man.com"
PROTOCOL = "http" if ENV == "dev" else "https"
PORT = "5000" if ENV == "dev" else "443"
