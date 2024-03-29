"""initial

Revision ID: 71750f3ce648
Revises: 
Create Date: 2024-02-23 18:35:51.133198

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "71750f3ce648"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "currency",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("code", sa.String(length=10), nullable=False),
        sa.Column("rate", sa.Numeric(precision=18, scale=6), nullable=False),
        sa.Column("type", sa.Enum("FIAT", "CRYPTO", name="currencytype"), nullable=False),
        sa.PrimaryKeyConstraint("code", name=op.f("pk_currency")),
    )
    op.create_table(
        "currency_update_task",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("rates", sa.JSON(), nullable=False),
        sa.Column("run_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_currency_update_task")),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("currency_update_task")
    op.drop_table("currency")
    # ### end Alembic commands ###
