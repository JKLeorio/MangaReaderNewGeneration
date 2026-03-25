from .comic import comic_router
from .chapter import chapter_router
from .page import page_router
from .genre import genre_router

__all__ = [
    "comic_router",
    "page_router", 
    "chapter_router", 
    "genre_router"
    ]