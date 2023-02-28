from fastapi import HTTPException, status


bad_request_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request"
)

unauthorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
)

not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Not Found"
)

conflict_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Already Exists"
)
