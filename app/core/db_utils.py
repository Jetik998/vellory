async def save_and_refresh(session, obj):
    session.add(obj)
    try:
        await session.commit()
        await session.refresh(obj)
        return obj
    except Exception:
        await session.rollback()
        raise


async def delete_and_commit(session, obj):
    try:
        await session.delete(obj)
        await session.commit()
    except Exception:
        await session.rollback()
        raise
