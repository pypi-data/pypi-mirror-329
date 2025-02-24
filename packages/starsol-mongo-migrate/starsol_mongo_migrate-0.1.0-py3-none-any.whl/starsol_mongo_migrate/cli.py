# pylint: disable=import-outside-toplevel
import argparse
import os
import sys
from pathlib import Path


def list_migrations(args: argparse.Namespace) -> None:
    from starsol_mongo_migrate.migration_path import MigrationPath

    migrations = MigrationPath.load_from_dir(args.dir)
    for mig in reversed(migrations):
        print(f'{mig.revision}: {mig.name}')


def generate_migration(args: argparse.Namespace) -> None:
    from starsol_mongo_migrate.migration_path import (
        EmptyMigrationPathError,
        LoadMigrationError,
        MigrationPath,
    )
    from starsol_mongo_migrate.template import generate_migration_template

    try:
        migrations = MigrationPath.load_from_dir(args.dir)
        down_revision = migrations.head.revision
    except EmptyMigrationPathError:
        down_revision = None
    except LoadMigrationError as e:
        print(f'Error loading migrations: {e}')
        return
    revision, migration_code = generate_migration_template(
        args.name, down_revision=down_revision
    )
    with open(args.dir / f'{revision}_{args.name}.py', 'w', encoding='utf-8') as f:
        f.write(migration_code)


def init(args: argparse.Namespace) -> None:
    from starsol_mongo_migrate.db import get_client, set_db_version

    client = get_client(args.mongo_uri)
    set_db_version(client, None)
    os.makedirs(args.dir, exist_ok=True)


def upgrade(args: argparse.Namespace) -> None:
    from starsol_mongo_migrate.db import get_client
    from starsol_mongo_migrate.migration_path import (
        EmptyMigrationPathError,
        LoadMigrationError,
        MigrationPath,
        RevisionNotFoundError,
        RevisionOrderError,
    )

    try:
        migrations = MigrationPath.load_from_dir(args.dir)
    except EmptyMigrationPathError:
        print('No migrations found')
        return
    except LoadMigrationError as e:
        print(f'Error loading migrations: {e}')
        return

    client = get_client(args.mongo_uri)

    try:
        migrations.upgrade(
            client,
            args.target_revision or migrations.head.revision,
            use_session=not args.no_transactions,
        )
    except (RevisionNotFoundError, RevisionOrderError) as e:
        print(f'Error upgrading: {e}')


def downgrade(args: argparse.Namespace) -> None:
    from starsol_mongo_migrate.db import get_client
    from starsol_mongo_migrate.migration_path import (
        EmptyMigrationPathError,
        LoadMigrationError,
        MigrationPath,
        RevisionNotFoundError,
        RevisionOrderError,
    )

    try:
        migrations = MigrationPath.load_from_dir(args.dir)
    except EmptyMigrationPathError:
        print('No migrations found')
        return
    except LoadMigrationError as e:
        print(f'Error loading migrations: {e}')
        return

    client = get_client(args.mongo_uri)

    try:
        migrations.downgrade(
            client, args.target_revision, use_session=not args.no_transactions
        )
    except (RevisionNotFoundError, RevisionOrderError) as e:
        print(f'Error downgrading: {e}')


def show_current_revision(args: argparse.Namespace) -> None:
    from starsol_mongo_migrate.db import get_client, get_db_version

    client = get_client(args.mongo_uri)
    current_revision = get_db_version(client)
    print(f'Current revision: {current_revision}')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--dir',
        type=Path,
        default='versions',
        help='Directory with migration files',
    )
    subparsers = parser.add_subparsers(required=True)

    generate_subparser = subparsers.add_parser(
        'generate', help='Generate new migration'
    )
    generate_subparser.add_argument('name', type=str, help='Name of the migration')
    generate_subparser.set_defaults(func=generate_migration)

    list_subparser = subparsers.add_parser('list', help='List all migrations')
    list_subparser.set_defaults(func=list_migrations)

    upgrade_subparser = subparsers.add_parser(
        'upgrade', help='Upgrade database to the specified revision'
    )
    upgrade_subparser.add_argument(
        '--no-transactions',
        action='store_true',
        help='Do not use transactions (transactions are not supported if the MongoDB is not a replica set)',
    )
    upgrade_subparser.add_argument('mongo_uri', type=str, help='Mongo URI')
    upgrade_subparser.add_argument(
        'target_revision',
        nargs='?',
        default=None,
        help='Start revision, default is the head revision',
    )
    upgrade_subparser.set_defaults(func=upgrade)

    downgrade_subparser = subparsers.add_parser(
        'downgrade', help='Downgrade database to the specified revision'
    )
    downgrade_subparser.add_argument(
        '--no-transactions',
        action='store_true',
        help='Do not use transactions (transactions are not supported if the MongoDB is not a replica set)',
    )
    downgrade_subparser.add_argument('mongo_uri', type=str, help='Mongo URI')
    downgrade_subparser.add_argument(
        'target_revision',
        nargs='?',
        default=None,
        help='End revision, default is the root revision',
    )
    downgrade_subparser.set_defaults(func=downgrade)

    init_subparser = subparsers.add_parser(
        'init', help='Initialize migration directory and database version collection'
    )
    init_subparser.add_argument('mongo_uri', type=str, help='Mongo URI')
    init_subparser.set_defaults(func=init)

    show_current_revision_subparser = subparsers.add_parser(
        'current', help='Show current database revision'
    )
    show_current_revision_subparser.add_argument(
        'mongo_uri', type=str, help='Mongo URI'
    )
    show_current_revision_subparser.set_defaults(func=show_current_revision)

    args = parser.parse_args()

    args.func(args)
    return 0


if __name__ == '__main__':
    sys.exit(main())
