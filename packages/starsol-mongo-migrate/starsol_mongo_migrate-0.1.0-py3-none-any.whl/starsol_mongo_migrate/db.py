from collections.abc import Callable
from typing import TYPE_CHECKING, Concatenate, ParamSpec

from pymongo import MongoClient

if TYPE_CHECKING:
    from pymongo.client_session import ClientSession

__all__ = (
    'get_client',
    'get_db_version',
    'set_db_version',
    'run_with_session',
)

VERSION_COLLECTION = '__db_version__'

P = ParamSpec('P')


def get_client(mongo_uri: str) -> MongoClient:
    return MongoClient(mongo_uri)


def get_db_version(client: MongoClient) -> str | None:
    version = client.get_database().get_collection(VERSION_COLLECTION).find_one()
    return version['version'] if version else None


def set_db_version(client: MongoClient, version: str | None) -> None:
    client.get_database().get_collection(VERSION_COLLECTION).replace_one(
        {}, {'version': version}, upsert=True
    )


def run_with_session(
    client: MongoClient,
    func: Callable[Concatenate['ClientSession', P], None],
    *args: P.args,
    **kwargs: P.kwargs,
) -> None:
    with client.start_session() as session:
        session.with_transaction(lambda s: func(s, *args, **kwargs))
        session.commit_transaction()
