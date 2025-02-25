from .base import Base, HumanIDMixin
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TEXT, INTEGER, TIMESTAMP


class Token(Base, HumanIDMixin):
    __tablename__ = "tokens"
    __table_args__ = {"schema": "token_vault"}
    __prefix__ = "tkn"
    __id_length__ = 16

    id = Column(TEXT, primary_key=True)
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
