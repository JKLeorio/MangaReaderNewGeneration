from typing import List
from fastapi import Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_async_session
from models.comment import Comment
from models.user import User
from services.comment_service import CommentService
from schemas.comment import CommentBase, CommentCreate, CommentPartialUpdate, CommentResponse
from api.auth.depends import current_user

comment_router = APIRouter()


@comment_router.get(
    "/page/{page_id}",
    response_model=List[CommentResponse],
    status_code=status.HTTP_200_OK
)
async def get_page_comments(
    page_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    comment_service = CommentService(session=session)
    comments = await comment_service.get_page_comments(
        page_id=page_id
    )
    return comments

@comment_router.get(
    "/person/{person_id}",
    response_model=List[CommentResponse],
    status_code=status.HTTP_200_OK
)
async def get_person_comments(
    person_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    comment_service = CommentService(session=session)
    comments = await comment_service.get_person_comments(
        person_id=person_id
    )
    return comments

@comment_router.get(
    "/comic/{comic_id}",
    response_model=List[CommentResponse],
    status_code=status.HTTP_200_OK
)
async def get_comic_comments(
    comic_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    comment_service = CommentService(session=session)
    comments = await comment_service.get_comic_comments(
        comic_id=comic_id
    )
    return comments

@comment_router.post(
    "/",
    response_model=CommentBase,
    status_code=status.HTTP_201_CREATED
)
async def create_comment(
    comment_data: CommentCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    comment_service = CommentService(session=session)
    new_comment = await comment_service.create(
        comment_data=comment_data,
        comment_owner=user
    )
    await comment_service.commit()
    await comment_service.refresh(new_comment)
    return new_comment


@comment_router.patch(
    "/{comment_id}",
    status_code=status.HTTP_200_OK,
    response_model=CommentResponse
)
async def update_comment(
    comment_id: int,
    comment_update: CommentPartialUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    comment_service = CommentService(session=session)
    updated_comment = await comment_service.update_by_id(
        comment_id,
        comment_update
    )
    await comment_service.commit()
    await comment_service.refresh(updated_comment)
    return updated_comment


@comment_router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_comment(
    comment_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    comment_service = CommentService(session=session)
    comment = await comment_service.delete_by_id(id=comment_id)
    await comment_service.commit()
    return

