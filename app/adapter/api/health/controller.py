from fastapi import APIRouter, Request

router = APIRouter(prefix="")


@router.get("/")
async def health(request: Request):
    return {"message": "healthy"}
