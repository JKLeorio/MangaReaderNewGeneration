from collections import defaultdict
from typing import Any, List
from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import Sequence
from sqlalchemy.orm import joinedload, noload

from models.comic import Comic, Page
from models.person import Person
from models.user import User
from schemas.comment import CommentCreate, CommentPaginated, CommentResponse
from schemas.pagination import Pagination
from .base_service import BaseService
from db.types import CommentRefers
from models.comment import Comment

class CommentService(BaseService):
    model = Comment
    fk_fields_on_create = {
        # Comment : ["parent_id"],
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
        
        depth = 0
        if comment_data.parent_id is not None:
            parent_comment = await self.get(
                Comment.id == comment_data.parent_id
            )
            depth = parent_comment.depth + 1

        new_comment = Comment(
            **comment_data.model_dump(), 
            owner_id=comment_owner.id,
            depth=depth
            )
        self._session.add(new_comment)
        await self._session.flush()
        return new_comment
    

    async def get_page_comments(
        self,
        page_id: int,
        pagination: Pagination
    ) -> Sequence[Comment]:
        page_comments = await self.get_structed_comments(
            comment_type=CommentRefers.PAGE,
            record_id=page_id,
            pagination=pagination
        )
        return page_comments

    async def get_person_comments(
        self,
        person_id: int,
        pagination: Pagination
    ) -> Sequence[Comment]:
        person_comments = await self.get_structed_comments(
            comment_type=CommentRefers.PERSON,
            record_id=person_id,
            pagination=pagination
        )
        return person_comments

    async def get_comic_comments(
        self,
        comic_id: int,
        pagination: Pagination
    ) -> Sequence[Comment]:
        comic_comments = await self.get_structed_comments(
            comment_type=CommentRefers.COMIC,
            record_id=comic_id,
            pagination=pagination
        )
        return comic_comments
    
    def link_comments_by_id(
        self,
        comments: Sequence[Any]|List,
    ) -> List[CommentResponse]:
        comments_by_depth = defaultdict(dict)
        while comments:
            comment = comments.pop(0)
            comments_by_depth[comment.depth][comment.id] = comment

        for depth in range(len(comments_by_depth), 0, -1):
            upper_level_comments = comments_by_depth[depth-1]
            for comment_id, comment in comments_by_depth[depth].items():
                upper_comment: Comment = upper_level_comments.get(comment.parent_id)
                upper_comment.childrens.append(comment)

        return list(comments_by_depth[0].values())

    
    async def get_structed_comments(
        self,
        comment_type: CommentRefers,
        record_id: int,
        pagination: Pagination
    ) -> CommentPaginated:
        paginated_comments = await self.get_paginated_comments(
            refers_to=comment_type,
            record_id=record_id,
            options=[
                noload(Comment.childrens),
                joinedload(Comment.owner)
            ],
            order_by=[
                Comment.depth.asc()
            ],
            pagination=pagination
        )
        comments_linked = self.link_comments_by_id(
            paginated_comments.items
        )
        comments_response = CommentPaginated(
            items=comments_linked,
            pagination=paginated_comments.pagination
        )
        return comments_response
    
    async def get_paginated_comments(
        self,
        record_id: int,
        refers_to: CommentRefers,
        pagination: Pagination,
        filter: Filter = None,
        options: list[Any] = [],
        order_by: Sequence[Any] = [],
    )-> CommentPaginated:
        comments_paginated = await self.get_paginated(
            Comment.record_id == record_id,
            Comment.refers_to == refers_to,
            total_conditions=[
                Comment.record_id == record_id,
                Comment.refers_to == refers_to,
            ],
            options=options,
            filter=filter,
            order_by=order_by,
            limit=pagination.size,
            page=pagination.page
        )
        comments_response = CommentPaginated(
            items=comments_paginated['items'],
            pagination=comments_paginated['pagination']
        )
        return comments_response