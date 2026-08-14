from dependency_injector import containers, providers
from pymongo import MongoClient

from repositories.mongo.plugin_token_repository import MongoPluginTokenRepository
from repositories.mongo.silent_request_repository import MongoSilentRequestRepository


class MongoDBContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    mongo_client = providers.Singleton(
        MongoClient,
        config.mongo.uri,
    )

    mongo_database = providers.Singleton(
        lambda client, name: client[name],
        mongo_client,
        name=config.mongo.database,
    )

    # Plugin Token

    plugin_token_collection = providers.Singleton(
        lambda db: db["plugin-token"],
        mongo_database,
    )

    plugin_token_repository = providers.Singleton(
        MongoPluginTokenRepository, collection=plugin_token_collection
    )

    # Silent Request

    silent_request_collection = providers.Singleton(
        lambda db: db["silent-requests"],
        mongo_database,
    )

    silent_request_repository = providers.Singleton(
        MongoSilentRequestRepository, collection=silent_request_collection
    )
