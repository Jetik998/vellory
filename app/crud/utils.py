from app.dependencies import SessionDep


async def save_and_refresh(session: SessionDep, obj):
    session.add(obj)
    try:
        await session.commit()
        await session.refresh(obj)
        return obj
    except Exception:
        await session.rollback()
        raise