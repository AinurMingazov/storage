from pydantic import BaseModel
from typing import Optional


# Schemas for Keeper
class KeeperCreate(BaseModel):
    name: str


class KeeperRead(BaseModel):
    id: int
    name: str
    slug: str


# Schemas for Category
class CategoryCreate(BaseModel):
    name: str


class CategoryRead(BaseModel):
    id: int
    name: str
    slug: str


# Schemas for Tool
class ToolCreate(BaseModel):
    name: str
    keeper_id: Optional[int]
    category_id: Optional[int]
    quantity: int
    description: Optional[str] = None
    price: float
    available: bool = True


class ToolRead(BaseModel):
    id: int
    name: str
    keeper_id: Optional[int]
    category_id: Optional[int]
    quantity: int
    description: Optional[str]
    price: float
    available: bool


# Schemas for Operation
class OperationCreate(BaseModel):
    giver_id: int
    taker_id: int
    tool_id: int
    quantity: int


class OperationRead(BaseModel):
    id: int
    giver_id: int
    taker_id: int
    tool_id: int
    quantity: int
    created: str
