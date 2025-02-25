from .base import Base, HumanIDMixin
from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TEXT, UUID, JSONB, INTEGER, BOOLEAN, ARRAY


class Inverter(Base, HumanIDMixin):
    __tablename__ = "inverters"
    __prefix__ = "inv"
    __id_length__ = 16

    id = Column(TEXT, primary_key=True)
    name = Column(TEXT, nullable=False)

    # Foreign Keys
    integration_id = Column(
        TEXT, ForeignKey("integrations.id", ondelete="CASCADE", onupdate="CASCADE")
    )

    # Relationships
    integration = relationship("Integration", back_populates="inverters")


class Integration(Base):
    __tablename__ = "integrations"

    id = Column(TEXT, primary_key=True)
    name = Column(TEXT, nullable=False)

    # Relationships
    inverters = relationship("Inverter", back_populates="integration")
    tokens = relationship("Token", back_populates="integration")
