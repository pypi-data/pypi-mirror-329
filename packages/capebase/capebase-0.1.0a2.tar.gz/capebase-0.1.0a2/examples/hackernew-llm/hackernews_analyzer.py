import asyncio
import logging
from datetime import datetime
from typing import List, Optional

import httpx
from capebase.main import CapeBase
from capebase.models import AuthContext, AuthContextProvider, ModelChange
from fastapi import Depends, FastAPI, Request
from sqlmodel import Field, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from examples.basic.db import create_db_and_tables
from examples.basic.scheme import UserCreate, UserRead, UserUpdate
from examples.basic.db import User
from examples.basic.users import auth_backend, fastapi_users, current_active_user


from starlette_prometheus import PrometheusMiddleware, metrics

logger = logging.getLogger(__name__)


# Define our SQLModels
class HackerNewsItem(SQLModel, table=True):
    """Model to store raw HackerNews items"""

    id: Optional[int] = Field(default=None, primary_key=True)
    hn_id: int = Field(index=True)  # Original HN ID
    title: str
    url: Optional[str]
    text: Optional[str]
    type: str  # story, comment, etc
    by: str  # author
    score: Optional[int]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    processed: bool = Field(default=False)


class ContentAnalysis(SQLModel, table=True):
    """Model to store the analysis results"""

    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="hackernewsitem.id")
    summary: str
    tags: str = Field(default="")  # Comma-separated tags
    sentiment_score: float
    analysis_timestamp: datetime = Field(default_factory=datetime.utcnow)


class CreateContentAnalysis(SQLModel):
    item_id: int = Field(foreign_key="hackernewsitem.id")
    summary: str
    sentiment_score: float


class UpdateContentAnalysis(SQLModel):
    summary: str


# Simple auth provider that gives admin access
class DemoAuthProvider(AuthContextProvider):
    async def __call__(self, request: Request, user: Optional[User] = Depends(current_active_user)) -> AuthContext:
        return AuthContext(id="admin", role="admin")


# Stub LLM client
class LLMClient:
    async def analyze_content(
        self, title: str, text: str = ""
    ) -> tuple[str, List[str], float]:
        """Stub for LLM analysis - in real world, this would call an actual LLM API"""
        # Return fake analysis (summary, tags, sentiment)
        return (f"Summary of: {title[:50]}...", ",".join(["technology", "news"]), 0.8)


class HackerNewsIngester:
    def __init__(self, cape: CapeBase, llm_client: LLMClient):
        self.cape = cape
        self.llm_client = llm_client
        self.http_client = httpx.AsyncClient()

    async def fetch_latest_stories(self) -> List[int]:
        """Fetch latest story IDs from HackerNews API"""
        response = await self.http_client.get(
            "https://hacker-news.firebaseio.com/v0/newstories.json"
        )
        return response.json()[:10]  # Limit to 10 stories for demo

    async def fetch_story_details(self, story_id: int) -> dict:
        """Fetch details for a specific story"""
        response = await self.http_client.get(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        )
        return response.json()

    async def ingest(self):
        """Main ingestion and analysis loop"""
        while True:
            try:
                story_ids = await self.fetch_latest_stories()

                async with self.cape.get_privileged_session() as session:
                    for story_id in story_ids:
                        # Check if we already have this story
                        existing = await session.get(HackerNewsItem, story_id)
                        if existing:
                            continue

                        # Fetch and store story
                        story_data = await self.fetch_story_details(story_id)
                        if not story_data:
                            continue

                        hn_item = HackerNewsItem(
                            hn_id=story_data["id"],
                            title=story_data.get("title", ""),
                            url=story_data.get("url"),
                            text=story_data.get("text"),
                            type=story_data.get("type", "story"),
                            by=story_data.get("by", "anonymous"),
                            score=story_data.get("score", 0),
                        )
                        session.add(hn_item)
                        await session.commit()
                        await session.refresh(hn_item)

            except Exception as e:
                print(f"Error in ingestion loop: {e}")

            # Wait before next iteration
            await asyncio.sleep(30)  # 5 minutes


async def handle_hn_item(
    llm_client: LLMClient, session: AsyncSession, hn_item: HackerNewsItem
):
    """Analyze content of a HackerNews item"""
    # Analyze content
    summary, tags, sentiment = await llm_client.analyze_content(
        hn_item.title, hn_item.text or ""
    )

    # Store analysis
    analysis = ContentAnalysis(
        item_id=hn_item.id, summary=summary, tags=tags, sentiment_score=sentiment
    )

    session.add(analysis)
    await session.commit()


def create_app():
    app = FastAPI(title="HackerNews Analyzer")
    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", metrics)

    app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth", tags=["auth"])

    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_verify_router(UserRead),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_users_router(UserRead, UserUpdate),
        prefix="/users",
        tags=["users"],
    )

    llm_client = LLMClient()

    # db_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/hackernews"

    # Initialize Cape
    cape = CapeBase(
        app=app,
        db_path="sqlite+aiosqlite:///hackernews.db",
        # db_path=db_url,
        auth_provider=DemoAuthProvider(),
    )

    # Register our models
    cape.publish(HackerNewsItem, routes=["list", "get", "create"])
    cape.publish(
        ContentAnalysis,
        create_schema=CreateContentAnalysis,
        update_schema=UpdateContentAnalysis
    )
    cape.permission_required(HackerNewsItem, role="*", actions=["read"])
    cape.permission_required(ContentAnalysis, role="*", actions=["read", "create", "update", "delete"])
    # cape.enable_audit_trail(HackerNewsItem)
    # cape.enable_audit_trail(ContentAnalysis)

    @cape.subscribe(HackerNewsItem)
    async def on_hackernews_item_change(change: ModelChange):
        logger.warning(f"HackerNews item changed: {change}")
        async with cape.get_privileged_session() as session:
            await handle_hn_item(llm_client, session, change.payload)

    @cape.subscribe(ContentAnalysis)
    async def on_analysis_change(change):
        logger.warning(f"Analysis added for item: {change.payload.item_id}")

    async def start_ingester():
        ingester = HackerNewsIngester(cape, LLMClient())
        asyncio.create_task(ingester.ingest())

    app.add_event_handler("startup", start_ingester)

    return app



if __name__ == "__main__":
    import uvicorn
    import asyncio

    asyncio.run(create_db_and_tables())

    uvicorn.run(create_app(), host="0.0.0.0", port=8000)
