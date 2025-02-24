from typing import Literal, Optional, Callable, Awaitable
from fastapi import Response, Form, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated
import logging

logger = logging.getLogger(__name__)

class TurboStreams:
    """Handles Turbo Streams functionality for HTMX responses"""
    
    def __init__(self, schema, get_session, crud_methods):
        self.schema = schema
        self.get_session = get_session
        self._create_item = crud_methods['create']
        self._update_item = crud_methods['update']
        self._delete_item = crud_methods['delete']
        self._get_item = crud_methods['get']

    def _turbo_stream(
        self,
        action: Literal["append", "prepend", "replace", "update", "remove"],
        target: str,
        content: Optional[str] = None
    ) -> Response:
        """Create a Turbo Stream response with the given action and content."""
        if action == "remove":
            turbo_stream = f'<turbo-stream action="{action}" target="{target}"></turbo-stream>'
        else:
            turbo_stream = (
                f'<turbo-stream action="{action}" target="{target}">'
                f'<template>{content}</template>'
                f'</turbo-stream>'
            )
        
        return Response(
            content=turbo_stream,
            media_type="text/vnd.turbo-stream.html"
        )

    def create_route(self) -> Callable[..., Awaitable[Response]]:
        async def route(
                item: Annotated[self.schema, Form()],
                session: AsyncSession = Depends(self.get_session)
        ) -> Response:
            item = await self._create_item(item, session)
            html = item._generate_item_html()
            return self._turbo_stream(
                action="append",
                target=f"{self.schema.__name__.lower()}s",
                content=html
            )

        return route
    
    def update_route(self, default_action: str = "replace") -> Callable[..., Awaitable[Response]]:
        async def route(
            item_id: int,
            item: Annotated[self.schema, Form()],
            session: AsyncSession = Depends(self.get_session),
            action: str = Query(default=default_action)
        ) -> Response:
            logger.warning(f"Updating item: {item}")
            item = await self._update_item(item_id, item.model_dump(exclude_unset=True), session)
            html = item._generate_item_html()
            return self._turbo_stream(
                action=action, 
                target=f"{self.schema.__name__.lower()}-{item_id}", 
                content=html
            )
        
        return route
        
    def delete_route(self) -> Callable[..., Awaitable[Response]]:
        async def route(
            item_id: int,
            session: AsyncSession = Depends(self.get_session)
        ) -> Response:
            await self._delete_item(item_id, session)
            return self._turbo_stream(
                action="remove", 
                target=f"{self.schema.__name__.lower()}-{item_id}"
            )
        
        return route
    
    def get_route(self, default_action: str = "replace") -> Callable[..., Awaitable[Response]]:
        async def route(
            item_id: int,
            session: AsyncSession = Depends(self.get_session),
            action: str = Query(default=default_action)
        ) -> Response:
            item = await self._get_item(item_id, session)
            html = item._generate_item_html()
            return self._turbo_stream(
                action=action, 
                target=f"{self.schema.__name__.lower()}-{item_id}", 
                content=html
            )
        
        return route 