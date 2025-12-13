from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from .auth import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        is_admin: bool = payload.get("is_admin")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {"username": username, "is_admin": is_admin}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token validation failed",
        )


def admin_only(user=Depends(get_current_user)):
    if not user["is_admin"]:
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required",
        )
    return user
