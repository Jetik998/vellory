# async def db_add_user(user: UserRegister, session):
#     hashed_password = get_password_hash(user.password)
#     user_dict = user.model_dump(exclude={"password"})
#     user_dict["hashed_password"] = hashed_password
#     db_user = User(**user_dict)
#     await save_and_refresh(session, db_user)
#     return db_user
#
#
