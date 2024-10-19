from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, func, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Keeper(Base):
    """Model describing the owner of a tool"""

    __tablename__ = "store_keeper"

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    slug = Column(String(50), unique=True, nullable=True)

    def __str__(self):
        return self.name


class Category(Base):
    """Model for categorizing tools"""

    __tablename__ = "store_category"

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    slug = Column(String(50), unique=True, nullable=True)

    def __str__(self):
        return self.name


class Tool(Base):
    """Model describing a tool"""

    __tablename__ = "store_tool"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    image = Column(String, nullable=True)  # You can handle image paths as strings
    keeper_id = Column(Integer, ForeignKey("store_keeper.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("store_category.id"), nullable=True)
    quantity = Column(Integer, default=0)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=True)
    available = Column(Boolean, default=True)
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, onupdate=func.now())

    def __str__(self):
        return self.name


class Operation(Base):
    """Model describing tool transfers"""

    __tablename__ = "store_operation"

    id = Column(Integer, primary_key=True)
    giver_id = Column(Integer, ForeignKey("store_keeper.id"), nullable=False)
    taker_id = Column(Integer, ForeignKey("store_keeper.id"), nullable=False)
    tool_id = Column(Integer, ForeignKey("store_tool.id"), nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    created = Column(DateTime, default=func.now())

    def __str__(self):
        return f"{self.giver.name} -> {self.taker.name} ({self.quantity} x {self.tool.name})"
