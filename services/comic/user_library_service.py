from fastapi import status, HTTPException
from sqlalchemy import select, func, case

from models.association import UserLibraryItem
from models.comic import Comic
from models.user import User
from schemas.user_library_item import UserLibraryItemCreate
from services.base_service import BaseService

class UserLibraryService(BaseService):
    fk_fields_on_create = {
        Comic : ["comic_id"]
    }

    async def create(
        self,
        user: User,
        create_data: UserLibraryItemCreate,
    ):
        comic_id = create_data.comic_id
        user_id = user.id
        exact_match_stmt = (
            select(
                func.max(
                    case(
                        (
                            (UserLibraryItem.comic_id == comic_id) & 
                            (UserLibraryItem.user_id == user_id),
                            1
                        ),
                        else_=0
                    ).label("exact_match")
                ),
                # func.max(
                #     case(
                #         (
                #             (UserLibraryItem.comic_id == comic_id),
                #             1
                #         ),
                #         else_=0
                #     ).label("comic_exists")
                # )
            )
        )

        await self.validate_ids(
            create_data,
            self.fk_fields_on_create
        )
        exact_match_result = (await self._session.execute(exact_match_stmt)).first()
        exact_match = exact_match_result[0]
        if exact_match:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='comic is already in library'
            )
        new_user_library_item = UserLibraryItem(
            **create_data.model_dump(),
            user_id = user.id
        )
        self._session.add(new_user_library_item)
        await self._session.flush()
        return new_user_library_item