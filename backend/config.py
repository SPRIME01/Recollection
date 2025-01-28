import os
from libsql_client import Client
from minio import Minio

def get_libsql_client() -> Client:
    return Client(
        url=os.getenv("LIBSQL_URL", "http://localhost:8080"),
        auth_token=os.getenv("LIBSQL_TOKEN", "")
    )

def get_minio_client() -> Minio:
    return Minio(
        os.getenv("MINIO_ENDPOINT", "localhost:9000"),
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=False
    )
