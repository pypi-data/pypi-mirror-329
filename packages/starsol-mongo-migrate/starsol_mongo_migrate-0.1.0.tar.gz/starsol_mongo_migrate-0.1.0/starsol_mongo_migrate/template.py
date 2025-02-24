from datetime import datetime

__all__ = ('generate_migration_template',)

TEMPLATE = """from typing import TYPE_CHECKING, ClassVar

from starsol_mongo_migrate import BaseMigration

if TYPE_CHECKING:
    from pymongo.client_session import ClientSession
    from pymongo.database import Database


class Migration(BaseMigration):
    \"\"\"{name_str}\"\"\"
    
    revision: ClassVar[str] = '{revision_str}'
    down_revision: ClassVar[str | None] = {down_revision}
    name = '{name_str}'

    def upgrade(self, session: 'ClientSession | None', db: 'Database') -> None:
        # Write your migration below using the session object

    def downgrade(self, session: 'ClientSession | None', db: 'Database') -> None:
        # Write your migration rollback below using the session object
"""


def generate_migration_template(
    name: str, down_revision: str | None = None
) -> tuple[str, str]:
    revision = datetime.now().strftime('%Y%m%d%H%M%S')
    return revision, TEMPLATE.format(
        revision_str=revision,
        name_str=name,
        down_revision=f"'{down_revision}'" if down_revision else 'None',
    )
