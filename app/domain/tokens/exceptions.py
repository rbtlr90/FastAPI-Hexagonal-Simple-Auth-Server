from fastapi import HTTPException, status


invalid_token_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Token"
)
