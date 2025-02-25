from .base import Base, HumanIDMixin
from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import (
    TEXT,
    JSONB,
    INTEGER,
    BOOLEAN,
    ARRAY,
    TIMESTAMP,
)


class Integration(Base):
    __tablename__ = "integrations"

    id = Column(TEXT, primary_key=True)
    name = Column(TEXT, nullable=False)

    # Relationships
    inverters = relationship("Inverter", back_populates="integration")
    tokens = relationship("Token", back_populates="integration")


class Inverter(Base, HumanIDMixin):
    __tablename__ = "inverters"
    __prefix__ = "inv"
    __id_length__ = 16

    id = Column(TEXT, primary_key=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()"),
        nullable=False,
    )
    name = Column(TEXT, nullable=False)
    external_id = Column(TEXT, nullable=False)
    rated_power = Column(INTEGER, nullable=False)
    data = Column(JSONB, nullable=False)

    token_id = Column(
        TEXT,
        ForeignKey("token_vault.tokens.id", ondelete="CASCADE", onupdate="CASCADE"),
    )

    # Foreign Keys
    integration_id = Column(
        TEXT, ForeignKey("integrations.id", ondelete="CASCADE", onupdate="CASCADE")
    )

    # Relationships
    integration = relationship("Integration", back_populates="inverters")
    token = relationship("Token", back_populates="inverters")
    measurements = relationship("InverterMeasurement", back_populates="inverter")


class InverterMeasurement(Base):
    __tablename__ = "inverter_measurements"

    inverter_id = Column(
        TEXT,
        ForeignKey("inverters.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    time = Column(TIMESTAMP(timezone=True), primary_key=True)
    power = Column(INTEGER, nullable=False)

    inverter = relationship("Inverter", back_populates="measurements")
