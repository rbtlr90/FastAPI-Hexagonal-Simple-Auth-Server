from fastapi import HTTPException, status


credential_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)
