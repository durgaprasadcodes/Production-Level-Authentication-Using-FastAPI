from fastapi import Request,HTTPException,status,Depends
from sqlalchemy.orm import Session
from database.database import get_db
from models.model import User
from tokens.jwt import decode_access_token

def get_current_user(
    request:Request,
    db:Session=Depends(get_db)
):

    access_token=request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Token Not Found"
        )

    try:
        payload=decode_access_token(access_token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Access Token"
        )

    user_id=payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Access Token"
        )

    user=db.query(User).filter(User.id==int(user_id)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User Not Found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User Account Is Inactive"
        )

    return user