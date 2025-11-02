# @router.post("/login", summary="Вход в систему и выдача токена")
# async def login(user: Login, session: SessionDep):
#     db_user = await db_get_user(user.username, session)
#     if not db_user:
#         raise HTTPException(status_code=400, detail="User not found")
#     verify_result = verify_password(user.password, db_user.hashed_password)
#     if not verify_result:
#         raise HTTPException(status_code=401, detail="Invalid password")
#     token = create_token(db_user.id, user.username)
#     return {"access_token": token, "token_type": "bearer"}
