from .base import Base, HumanIDMixin
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TEXT, INTEGER, TIMESTAMP
from sqlalchemy.sql import text
import datetime as dt


class Token(Base, HumanIDMixin):
    __tablename__ = "tokens"
    __table_args__ = {"schema": "token_vault"}
    __prefix__ = "tkn"
    __id_length__ = 16

    id = Column(TEXT, primary_key=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()"),
        nullable=False,
    )
    access_token = Column(TEXT, nullable=False)
    refresh_token = Column(TEXT, nullable=False)
    expires_in = Column(INTEGER, nullable=False)
    token_type = Column(TEXT, nullable=False)
    scope = Column(TEXT, nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False)

    # Foreign Keys
    integration_id = Column(
        TEXT, ForeignKey("integrations.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    # Relationships
    integration = relationship("Integration", back_populates="tokens")
    inverters = relationship("Inverter", back_populates="token")

    def is_expired(self):
        return self.updated_at + dt.timedelta(
            seconds=self.expires_in
        ) < dt.datetime.now(tz=dt.timezone.utc)
