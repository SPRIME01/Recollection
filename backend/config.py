import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    libsql_url: str = "http://localhost:8080"
    libsql_token: str = ""
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = ""
    minio_secret_key: str = ""

    class Config:
        env_file = ".env"

settings = Settings()

from libsql_client import Client
from minio import Minio

def get_libsql_client() -> Client:
    return Client(
        url=settings.libsql_url,
        auth_token=settings.libsql_token
    )

def get_minio_client() -> Minio:
    return Minio(
        settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=False
    )
