from fastapi import HTTPException


UsernameAlreadyTaken = HTTPException(
    status_code=400,
    detail="A user with this name already exists."
)

InvalidUserName = HTTPException(
    status_code=400,
    detail="No user with this name exists."
)

InvalidUserPass = HTTPException(
    status_code=400,
    detail="Invalid username or password.",
    headers={"WWW-Authenticate": "Basic"}
)


InvalidPermissions = HTTPException(
    status_code=401,
    detail="You do not have permission for this action."
)