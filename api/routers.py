from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db import get_session
from models.store import Keeper, Category, Tool, Operation
from schemas import (
    KeeperCreate,
    KeeperRead,
    CategoryCreate,
    CategoryRead,
    ToolCreate,
    ToolRead,
    OperationCreate,
    OperationRead,
)

router = APIRouter()

# ------------------ Keeper Routes ------------------


@router.post("/keepers/", response_model=KeeperRead)
async def create_keeper(keeper: KeeperCreate, session: AsyncSession = Depends(get_session)):
    new_keeper = Keeper(name=keeper.name)
    session.add(new_keeper)
    await session.commit()
    await session.refresh(new_keeper)
    return new_keeper


@router.get("/keepers/", response_model=list[KeeperRead])
async def get_keepers(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Keeper))
    keepers = result.scalars().all()
    return keepers


# ------------------ Category Routes ------------------


@router.post("/categories/", response_model=CategoryRead)
async def create_category(category: CategoryCreate, session: AsyncSession = Depends(get_session)):
    new_category = Category(name=category.name)
    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)
    return new_category


@router.get("/categories/", response_model=list[CategoryRead])
async def get_categories(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Category))
    categories = result.scalars().all()
    return categories


# ------------------ Tool Routes ------------------


@router.post("/tools/", response_model=ToolRead)
async def create_tool(tool: ToolCreate, session: AsyncSession = Depends(get_session)):
    new_tool = Tool(
        name=tool.name,
        keeper_id=tool.keeper_id,
        category_id=tool.category_id,
        quantity=tool.quantity,
        description=tool.description,
        price=tool.price,
        available=tool.available,
    )
    session.add(new_tool)
    await session.commit()
    await session.refresh(new_tool)
    return new_tool


@router.get("/tools/", response_model=list[ToolRead])
async def get_tools(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Tool))
    tools = result.scalars().all()
    return tools


# ------------------ Operation Routes ------------------


@router.post("/operations/", response_model=OperationRead)
async def create_operation(operation: OperationCreate, session: AsyncSession = Depends(get_session)):
    new_operation = Operation(
        giver_id=operation.giver_id, taker_id=operation.taker_id, tool_id=operation.tool_id, quantity=operation.quantity
    )
    session.add(new_operation)
    await session.commit()
    await session.refresh(new_operation)
    return new_operation


@router.get("/operations/", response_model=list[OperationRead])
async def get_operations(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Operation))
    operations = result.scalars().all()
    return operations
