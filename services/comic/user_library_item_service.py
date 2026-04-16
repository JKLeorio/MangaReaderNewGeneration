from sqlalchemy import select, func, case

from models.association import UserLibraryItem
from models.comic import Comic
from models.user import User
from schemas.user_library_item import UserLibraryItemCreate
from services.base_service import BaseService

class UserLibraryItemService(BaseService):
    
    async def create(
        self,
        user: User,
        create_data: UserLibraryItemCreate,
    ):
        comic_id = create_data.comic_id
        user_id = user.id
        stmt = (
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
                func.max(
                    case(
                        (
                            (UserLibraryItem.comic_id == comic_id),
                            1
                        ),
                        else_=0
                    ).label("comic_exists")
                )
            )
        )
        result = await self._session.execute(stmt)
        scalar = result.scalar_one()
        
        new_user_library_item = UserLibraryItem(
            **create_data.model_dump(),
            user_id = user.id
        )