from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from pymongo.client_session import ClientSession
    from pymongo.database import Database

__all__ = ('BaseMigration',)


class BaseMigration(ABC):
    revision: ClassVar[str]
    down_revision: ClassVar[str | None] = None
    name: ClassVar[str] = ''

    @property
    def description(self) -> str:
        return self.__doc__ or ''

    @abstractmethod
    def upgrade(self, session: 'ClientSession | None', db: 'Database') -> None:
        pass

    @abstractmethod
    def downgrade(self, session: 'ClientSession | None', db: 'Database') -> None:
        pass
