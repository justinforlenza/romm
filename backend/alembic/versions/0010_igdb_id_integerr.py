"""empty message

Revision ID: 0010_igdb_id_integerr
Revises: 0009_models_refactor
Create Date: 2023-09-14 09:57:13.487331

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0010_igdb_id_integerr"
down_revision = "0009_models_refactor"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("platforms", schema=None) as batch_op:
        batch_op.execute("UPDATE platforms SET igdb_id = NULL WHERE igdb_id = ''")
        batch_op.execute("UPDATE platforms SET sgdb_id = NULL WHERE sgdb_id = ''")

        batch_op.alter_column(
            "igdb_id",
            existing_type=sa.VARCHAR(length=10),
            type_=sa.Integer(),
            existing_nullable=True,
            postgresql_using="igdb_id::integer",
        )
        batch_op.alter_column(
            "sgdb_id",
            existing_type=sa.VARCHAR(length=10),
            type_=sa.Integer(),
            existing_nullable=True,
            postgresql_using="sgdb_id::integer",
        )

    with op.batch_alter_table("roms", schema=None) as batch_op:
        batch_op.execute("UPDATE roms SET igdb_id = NULL WHERE igdb_id = ''")
        batch_op.execute("UPDATE roms SET sgdb_id = NULL WHERE sgdb_id = ''")

        batch_op.alter_column(
            "igdb_id",
            existing_type=sa.VARCHAR(length=10),
            type_=sa.Integer(),
            existing_nullable=True,
            postgresql_using="igdb_id::integer",
        )
        batch_op.alter_column(
            "sgdb_id",
            existing_type=sa.VARCHAR(length=10),
            type_=sa.Integer(),
            existing_nullable=True,
            postgresql_using="sgdb_id::integer",
        )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("roms", schema=None) as batch_op:
        batch_op.alter_column(
            "sgdb_id",
            existing_type=sa.Integer(),
            type_=sa.VARCHAR(length=10),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "igdb_id",
            existing_type=sa.Integer(),
            type_=sa.VARCHAR(length=10),
            existing_nullable=True,
        )

    with op.batch_alter_table("platforms", schema=None) as batch_op:
        batch_op.alter_column(
            "sgdb_id",
            existing_type=sa.Integer(),
            type_=sa.VARCHAR(length=10),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "igdb_id",
            existing_type=sa.Integer(),
            type_=sa.VARCHAR(length=10),
            existing_nullable=True,
        )

    # ### end Alembic commands ###
