import pytest
from backend.config import Settings, get_libsql_client, get_minio_client
from libsql_client import Client
from minio import Minio

def test_settings():
    settings = Settings(
        libsql_url="http://test-libsql:8080",
        libsql_token="test-token",
        minio_endpoint="test-minio:9000",
        minio_access_key="test-access-key",
        minio_secret_key="test-secret-key"
    )
    assert settings.libsql_url == "http://test-libsql:8080"
    assert settings.libsql_token == "test-token"
    assert settings.minio_endpoint == "test-minio:9000"
    assert settings.minio_access_key == "test-access-key"
    assert settings.minio_secret_key == "test-secret-key"

def test_get_libsql_client(monkeypatch):
    monkeypatch.setattr("backend.config.settings", Settings(libsql_url="http://test-libsql:8080", libsql_token="test-token"))
    client = get_libsql_client()
    assert isinstance(client, Client)
    assert client.url == "http://test-libsql:8080"
    assert client.auth_token == "test-token"

def test_get_minio_client(monkeypatch):
    monkeypatch.setattr("backend.config.settings", Settings(minio_endpoint="test-minio:9000", minio_access_key="test-access-key", minio_secret_key="test-secret-key"))
    client = get_minio_client()
    assert isinstance(client, Minio)
    assert client._endpoint_url == "http://test-minio:9000"
    assert client._access_key == "test-access-key"
    assert client._secret_key == "test-secret-key"
