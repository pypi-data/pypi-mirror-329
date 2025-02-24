from collections.abc import Generator
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import TYPE_CHECKING, Self

from .base import BaseMigration
from .db import get_db_version, run_with_session, set_db_version

if TYPE_CHECKING:
    from pymongo import MongoClient


__all__ = (
    'MigrationPath',
    'ValidateMigrationPathError',
    'EmptyMigrationPathError',
    'LoadMigrationError',
    'RevisionNotFoundError',
    'RevisionOrderError',
)


class ValidateMigrationPathError(Exception):
    pass


class EmptyMigrationPathError(Exception):
    pass


class LoadMigrationError(Exception):
    pass


class RevisionNotFoundError(Exception):
    pass


class RevisionOrderError(Exception):
    pass


class MigrationPath:
    __migrations: dict[str, BaseMigration]
    __up_migrations: dict[str | None, str | None]
    __head: str
    __root: str

    @property
    def head(self) -> BaseMigration:
        return self.__migrations[self.__head]

    @property
    def root(self) -> BaseMigration:
        return self.__migrations[self.__root]

    def __init__(self, migrations: dict[str, BaseMigration]):
        if not migrations:
            raise EmptyMigrationPathError('No migrations provided')
        self.__migrations = migrations.copy()
        down_revisions = {
            mig.down_revision for mig in self.__migrations.values() if mig.down_revision
        }
        if len(down_revisions) != len(self.__migrations) - 1:
            raise ValidateMigrationPathError(
                'Multiple migrations with the same down_revision found'
            )
        self.__up_migrations = {
            mig.down_revision: rev for rev, mig in self.__migrations.items()
        }
        root_ = None
        head_ = None
        for rev, mig in self.__migrations.items():
            if mig.down_revision is None:
                if root_ is not None:
                    raise ValidateMigrationPathError(
                        f'Multiple roots found: "{root_}" and "{rev}"'
                    )
                self.__root = root_ = rev
            if rev not in down_revisions:
                if head_ is not None:
                    raise ValidateMigrationPathError(
                        f'Multiple heads found: "{head_}" and "{rev}"'
                    )
                self.__head = head_ = rev
        if not self.__root:
            raise ValidateMigrationPathError('No root found')
        if not self.__head:
            raise ValidateMigrationPathError('No head found')
        self.__up_migrations[self.__head] = None

    @classmethod
    def load_from_dir(cls, versions_dir: Path) -> Self:
        try:
            return cls(load_dir(versions_dir))
        except (FileNotFoundError, NotADirectoryError, RuntimeError) as e:
            raise LoadMigrationError(
                f'Failed to load migrations from directory: {e}'
            ) from e

    def _get_up(self, current: BaseMigration | None) -> BaseMigration | None:
        revision = self.__up_migrations.get(current.revision if current else None)
        if not revision:
            return None
        return self.__migrations.get(revision)

    def _get_down(self, current: BaseMigration) -> BaseMigration | None:
        if not current.down_revision:
            return None
        return self.__migrations.get(current.down_revision)

    def _validate_order(self, src: str | None, dst: str | None) -> None:
        if src and src not in self.__migrations:
            raise RevisionNotFoundError(f'Migration {src} not found')
        if dst and dst not in self.__migrations:
            raise RevisionNotFoundError(f'Migration {dst} not found')
        current = self.__migrations.get(src) if src else None
        while not current or current.revision != dst:
            current = self._get_up(current)
            if not current:
                raise RevisionOrderError(
                    f'Migration {dst} is not an ancestor of migration {src}'
                )

    def __iter__(self) -> Generator[BaseMigration]:
        current: BaseMigration | None = self.head
        while current:
            yield current
            current = self._get_down(current)

    def __len__(self) -> int:
        return len(self.__migrations)

    def __reversed__(self) -> Generator[BaseMigration]:
        current: BaseMigration | None = self.root
        while current:
            yield current
            current = self._get_up(current)

    def upgrade(
        self,
        client: 'MongoClient',
        target_revision: str | None = None,
        use_session: bool = True,
    ) -> None:
        current_revision = get_db_version(client)
        self._validate_order(current_revision, target_revision)
        current = self._get_up(
            self.__migrations.get(current_revision) if current_revision else None
        )
        db = client.get_database()
        while current and current.down_revision != target_revision:
            if use_session:
                run_with_session(client, current.upgrade, db)
            else:
                current.upgrade(None, db)
            set_db_version(client, current.revision)
            print(
                f'Upgraded {current.down_revision} -> {current.revision} ({current.name})'
            )
            current = self._get_up(current)

    def downgrade(
        self,
        client: 'MongoClient',
        target_revision: str | None = None,
        use_session: bool = True,
    ) -> None:
        current_revision = get_db_version(client)
        self._validate_order(target_revision, current_revision)
        current = self.__migrations.get(current_revision) if current_revision else None
        while current and current.revision != target_revision:
            if use_session:
                run_with_session(client, current.downgrade, client.get_database())
            else:
                current.downgrade(None, client.get_database())
            set_db_version(client, current.down_revision)
            print(
                f'Downgraded {current.revision} -> {current.down_revision} ({current.name})'
            )
            current = self._get_down(current)


def load_file(version_file: Path) -> BaseMigration:
    if not version_file.exists():
        raise FileNotFoundError(f'Version file {version_file} does not exist')
    if not version_file.is_file():
        raise NotADirectoryError(f'Version file {version_file} is not a file')

    spec = spec_from_file_location(version_file.stem, version_file)
    if not spec:
        raise RuntimeError(f'Failed to load migration from {version_file}')
    module = module_from_spec(spec)
    if not spec.loader:
        raise RuntimeError(f'Failed to load migration from {version_file}')
    spec.loader.exec_module(module)
    if not hasattr(module, 'Migration'):
        raise AttributeError(
            f'File {version_file.name} does not have a Migration class'
        )
    if not issubclass(module.Migration, BaseMigration):
        raise TypeError(
            f'Migration class in file {version_file.name} is not a subclass of BaseMigration'
        )
    return module.Migration()  # type: ignore


def load_dir(versions_dir: Path) -> dict[str, BaseMigration]:
    if not versions_dir.exists():
        raise FileNotFoundError(f'Versions directory {versions_dir} does not exist')
    if not versions_dir.is_dir():
        raise NotADirectoryError(
            f'Versions directory {versions_dir} is not a directory'
        )

    migrations = {}
    for version_path in versions_dir.iterdir():
        if version_path.is_dir():
            continue
        try:
            migration = load_file(version_path)
        except Exception as e:
            raise RuntimeError(f'Failed to load migration from {version_path}') from e
        migrations[migration.revision] = migration
    return migrations
