from .comic import comic_router
from .chapter import chapter_router
from .page import page_router
from .genre import genre_router
from .user_library import user_library_router

__all__ = [
    "comic_router",
    "page_router", 
    "chapter_router", 
    "genre_router",
    "user_library_router"
    ]