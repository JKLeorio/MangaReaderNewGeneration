from fastapi import APIRouter, Depends, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_async_session
from schemas.comic import PageCreate, PageResponse
from services.comic.page_service import PageService

page_router = APIRouter()

@page_router.post(
    "/",
    response_model=PageResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_page(
    page_img: UploadFile,
    create_data: PageCreate = Depends(PageCreate.as_form),
    session: AsyncSession = Depends(get_async_session)
):
    page_service = PageService(session=session)
    new_page = await page_service.create(
        create_data, page_img
        )
    page_service.commit()
    page_service.refresh(new_page)
    response = PageResponse.model_validate(new_page, from_attributes=True)
    return response
