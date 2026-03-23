from pydantic import BaseModel
from sqlalchemy import Sequence
from sqlalchemy.orm import joinedload

from models.comic import Comic, Page
from models.person import Person
from models.user import User
from schemas.comment import CommentCreate
from .base_service import BaseService
from db.types import CommentRefers
from models.comment import Comment

class CommentService(BaseService):
    model = Comment
    fk_fields_on_create = {
        Comment : ["parent_id"],
        # User : ["owner_id"],
    }
    fk_fields_on_update = {}

    async def create(
        self,
        comment_data: CommentCreate,
        comment_owner: User
    ):
        model_ids = {}
        model_ids.update(
            self.fk_fields_on_create
        )
        match comment_data.refers_to:
            case CommentRefers.PERSON:
                model_ids[Person] = ["record_id"]
            case CommentRefers.PAGE:
                model_ids[Page] = ["record_id"]
            case CommentRefers.COMIC:
                model_ids[Comic] = ["record_id"]

        
        await self.validate_ids(
            comment_data,
            model_ids
        )
        new_comment = Comment(**comment_data.model_dump(), owner_id=comment_owner.id)
        self._session.add(new_comment)
        await self._session.flush()
        return new_comment
    

    async def get_page_comments(
        self,
        page_id: int
    ) -> Sequence[Comment]:
        page_comments = await self.get_all(
            Comment.refers_to == CommentRefers.PAGE,
            Comment.record_id == page_id,
        )
        return page_comments

    async def get_person_comments(
        self,
        person_id: int
    ) -> Sequence[Comment]:
        person_comments = await self.get_all(
            Comment.refers_to == CommentRefers.PERSON,
            Comment.record_id == person_id
        )
        return person_comments

    async def get_comic_comments(
        self,
        comic_id: int
    ) -> Sequence[Comment]:
        comic_comments = await self.get_all(
            Comment.refers_to == CommentRefers.COMIC,
            Comment.record_id == comic_id,
            # options=[
            #     joinedload(
            #         Comment.childrens
            #     )
            # ]
        )
        return comic_comments
