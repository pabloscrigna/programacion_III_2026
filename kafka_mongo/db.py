from pymongo import AsyncMongoClient

from config import get_settings

_client: AsyncMongoClient | None = None


async def connect_mongo():
    global _client

    settings = get_settings()
    _client = AsyncMongoClient(
        settings.mongodb_uri
    )

    await _client.admin.command("ping")
    _client[settings.mongodb_db]

def get_db() -> AsyncMongoClient:

    if _client is None:
        raise RuntimeError("MongoDB no inicializada")

    return _client[get_settings().mongodb_db]
