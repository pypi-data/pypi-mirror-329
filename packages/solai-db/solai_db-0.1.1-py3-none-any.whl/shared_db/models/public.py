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
    brand_id = Column(
        TEXT, ForeignKey("brands.id", ondelete="CASCADE", onupdate="CASCADE")
    )

    # Relationships
    brand = relationship("Brand", back_populates="inverters")


class Brand(Base):
    __tablename__ = "brands"

    id = Column(TEXT, primary_key=True)
    name = Column(TEXT, nullable=False)

    # Relationships
    inverters = relationship("Inverter", back_populates="brand")
