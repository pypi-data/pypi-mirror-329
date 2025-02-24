import logging
from contextlib import asynccontextmanager
from typing import Any, Optional

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import field_validator
from sqlmodel import Field, SQLModel, select

from capebase.main import AuthContext, AuthContextProvider, CapeBase
from capebase.models import FROM_AUTH_ID
from examples.basic.db import create_db_and_tables
from examples.basic.scheme import UserCreate, UserRead, UserUpdate
from examples.basic.users import User, auth_backend, fastapi_users

# Configure logging
# logging.basicConfig(
#     level=logging.WARNING,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
# )
logger = logging.getLogger(__name__)


# Initialize FastAPI and Cape
app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up auth")
    await create_db_and_tables()
    yield

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

@app.post("/auth/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key="todo_auth")
    return response


async def get_user_context(request: Request, user: Optional[User] = Depends(fastapi_users.current_user(active=True))) -> AuthContext:
    if not user:
        return AuthContext()

    return AuthContext(
        id=str(user.id),
        role=user.role,
        context={}
    )

app.router.lifespan_context = lifespan
cape = CapeBase(app=app, db_path="sqlite+aiosqlite:///test.db", auth_provider=get_user_context)

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

@cape.publish
@cape.permission_required(role="admin", actions=["*"])
@cape.permission_required(role="*", actions=["read", "create", "update","delete"])
class SecureDocument(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    owner_id: str
    org_id: str 

@cape.publish
@cape.permission_required(role="*", actions=["read", "create", "update"])
@cape.permission_required(role="*", actions=["delete"], owner_field="owner_id")
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    completed: bool = Field(default=False)

    owner_id: FROM_AUTH_ID

    org_id: str = Field(default="system")
    

    @field_validator("completed", mode="before")
    @classmethod
    def validate_completed(cls, value: Any) -> bool:
        print("type of value:", type(value))
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes", "on")
        if isinstance(value, int):
            return value == 1
        return False  # Default fallback

    def _generate_item_html(self) -> str:
        completed_class = "line-through text-gray-500" if self.completed else ""
        checked = "checked" if self.completed else ""
        
        return f"""
            <div class="flex items-center justify-between bg-white p-4 rounded shadow">
                <div class="flex items-center gap-4">
                    <form action="/turbo/todo/{self.id}/toggle" method="POST" data-turbo-stream>
                        <input type="checkbox" {checked} class="w-5 h-5" onchange="this.form.requestSubmit()">
                    </form>
                    <span class="{completed_class}">{self.title}</span>
                </div>
                <form action="/turbo/todo/{self.id}" method="DELETE" data-turbo-stream>
                    <button type="submit" class="text-red-500 hover:text-red-700">Delete</button>
                </form>
            </div>
        """


@app.get("/")
async def index(request: Request, user: Optional[User] = Depends(fastapi_users.current_user(optional=True))):
    """Serve the index page with all securedocument."""
    auth_context = AuthContext(id="admin", context={"org_id": "123"})
    async with cape.get_session(auth_context) as session:
        result = await session.execute(select(Todo))
        todos = result.scalars().all()
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "todos": todos, "user": user}
        )
    
@app.get("/login")
async def login_page(
    request: Request,
    user: Optional[User] = Depends(fastapi_users.current_user(optional=True))
):
    # If user is already logged in, redirect to home page
    if user:
        return RedirectResponse(url="/", status_code=303)
    
    # Get the next URL from query parameters, defaulting to home page
    next_url = request.query_params.get("next", "/")
    
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "next": next_url
        }
    )
    
@app.post("/todo/{todo_id}/toggle")
async def toggle_todo(request: Request, todo_id: int):
    """Toggle a todo's completion status."""
    async with cape.get_session(id="admin", context={"org_id": "123"}) as session:
        todo = await session.get(Todo, todo_id)
        if todo:
            todo.completed = not todo.completed
            session.add(todo)
            await session.commit()
            return RedirectResponse(url="/", status_code=303)
    raise HTTPException(status_code=404, detail="Todo not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, lifespan="auto") 