from collections import defaultdict
from typing import Any, List

from pydantic import BaseModel
from sqlalchemy import Sequence
from sqlalchemy.orm import joinedload

from models.comic import Comic, Page
from models.person import Person
from models.user import User
from schemas.comment import CommentCreate, CommentResponse
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
        page_comments = await self.get_structed_comments(
            comment_type=CommentRefers.PAGE,
            record_id=page_id
        )
        return page_comments

    async def get_person_comments(
        self,
        person_id: int
    ) -> Sequence[Comment]:
        person_comments = await self.get_structed_comments(
            comment_type=CommentRefers.PERSON,
            record_id=person_id
        )
        return person_comments

    async def get_comic_comments(
        self,
        comic_id: int
    ) -> Sequence[Comment]:
        comic_comments = await self.get_structed_comments(
            comment_type=CommentRefers.COMIC,
            record_id=comic_id
        )
        return comic_comments
    
    def link_comments_by_id(
        comments: Sequence[Any]|List
    ) -> List[CommentResponse]:
        comments_by_depth = defaultdict(dict)
        while comments:
            comment = comments.pop(0)
            comments_by_depth[comment.depth][comment.id] = comment

        for depth in range(len(comments_by_depth), 0, -1):
            upper_level_comments = comments_by_depth[depth+1]
            for comment_id, comment in comments_by_depth[depth].items():
                upper_comment: Comment = upper_level_comments.get(comment.parent_id)
                upper_comment.childrens.append(comment)

        return comments_by_depth[0]

    
    async def get_structed_comments(
        self,
        comment_type: CommentRefers,
        record_id: int
    ) -> List[CommentResponse]:
        comments = await self.get_all(
            Comment.refers_to == comment_type,
            Comment.record_id == record_id,
            order_by=[
                Comment.depth.asc()
            ]
        )
        
