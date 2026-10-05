"""Normalized endpoint reporting results."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision="0002"
down_revision="0001"
branch_labels=None
depends_on=None

def upgrade():
    op.create_table("endpoint_results",
        sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),
        sa.Column("campaign_id",postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column("provider_action_id",postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column("endpoint_id",sa.String(255),nullable=False),
        sa.Column("endpoint_name",sa.String(255),nullable=False),
        sa.Column("server_role",sa.String(64)),
        sa.Column("os",sa.String(120)),
        sa.Column("state",sa.String(32),nullable=False),
        sa.Column("exit_code",sa.Integer()),
        sa.Column("reboot_required",sa.Boolean()),
        sa.Column("failure_reason",sa.Text()),
        sa.Column("details",postgresql.JSONB(),nullable=False,server_default=sa.text("'{}'::jsonb")),
        sa.Column("observed_at",sa.DateTime(timezone=True),server_default=sa.func.now()))
    for column in ("campaign_id","provider_action_id","endpoint_id","endpoint_name","server_role","state","observed_at"):
        op.create_index(f"ix_endpoint_results_{column}","endpoint_results",[column])

def downgrade():
    op.drop_table("endpoint_results")
