from typing import TypeVar, Generic, Optional, Type, Dict
from pydantic import BaseModel, EmailStr
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta
import secrets
import asyncio

UserSchemaT = TypeVar('UserSchemaT', bound=BaseModel)

class CapeSecurityBase(Generic[UserSchemaT]):
    """Base class for handling authentication and user management.
    
    This class should be subclassed to implement specific authentication methods.
    The subclass must define UserSchema and implement _get_user_from_token.
    """
    
    def __init__(self, user_schema: Type[UserSchemaT]):
        """Initialize the security base with a user schema.
        
        Args:
            user_schema: Pydantic model class that defines the user structure
        """
        self.user_schema = user_schema
        self.security = HTTPBearer()

    async def _get_user_from_token(self, token: str) -> Optional[UserSchemaT]:
        """Extract and validate user from authentication token.
        
        Args:
            token: The authentication token
            
        Returns:
            Optional[UserSchemaT]: The user object if valid, None otherwise
            
        This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement _get_user_from_token")

    async def get_current_user(
        self,
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> UserSchemaT:
        """FastAPI dependency for getting the current authenticated user.
        
        Args:
            request: FastAPI request object
            credentials: HTTP Bearer token credentials
            
        Returns:
            UserSchemaT: The current authenticated user
            
        Raises:
            HTTPException: If authentication fails or user is not found
        """
        try:
            user = await self._get_user_from_token(credentials.credentials)
            if user is None:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid authentication credentials"
                )
            return user
        except Exception as e:
            raise HTTPException(
                status_code=401,
                detail=str(e)
            )

    def requires_auth(self):
        """Get dependency that requires authentication.
        
        Returns:
            Callable: Dependency that will return the current user
        """
        return self.get_current_user

class MagicLinkUserSchema(BaseModel):
    """Basic user schema for magic link authentication"""
    email: EmailStr
    is_verified: bool = False

class MagicLinkSecurity(CapeSecurityBase[MagicLinkUserSchema]):
    """Implementation of magic link authentication"""
    
    def __init__(
        self,
        secret_key: str,
        token_expire_minutes: int = 15,
        magic_link_expire_minutes: int = 10
    ):
        super().__init__(MagicLinkUserSchema)
        self.secret_key = secret_key
        self.token_expire_minutes = token_expire_minutes
        self.magic_link_expire_minutes = magic_link_expire_minutes
        # Store pending magic links: email -> (token, expiry)
        self._pending_links: Dict[str, tuple[str, datetime]] = {}

    def _create_magic_link_token(self, email: str) -> str:
        """Create a short-lived token for magic link"""
        token = secrets.token_urlsafe(32)
        expiry = datetime.utcnow() + timedelta(minutes=self.magic_link_expire_minutes)
        self._pending_links[email] = (token, expiry)
        return token

    def _create_session_token(self, email: str) -> str:
        """Create a longer-lived JWT session token"""
        expiry = datetime.utcnow() + timedelta(minutes=self.token_expire_minutes)
        return jwt.encode(
            {
                'sub': email,
                'exp': expiry,
                'type': 'session'
            },
            self.secret_key,
            algorithm='HS256'
        )

    async def create_magic_link(self, email: str) -> str:
        """Create a magic link for email verification
        
        Args:
            email: User's email address
            
        Returns:
            str: Magic link token to be sent via email
        """
        return self._create_magic_link_token(email)

    async def verify_magic_link(self, email: str, token: str) -> str:
        """Verify a magic link and return a session token
        
        Args:
            email: User's email address
            token: Magic link token
            
        Returns:
            str: Session token for API authentication
            
        Raises:
            HTTPException: If verification fails
        """
        if email not in self._pending_links:
            raise HTTPException(status_code=400, detail="No pending magic link")
            
        stored_token, expiry = self._pending_links[email]
        if datetime.utcnow() > expiry:
            del self._pending_links[email]
            raise HTTPException(status_code=400, detail="Magic link expired")
            
        if not secrets.compare_digest(stored_token, token):
            raise HTTPException(status_code=400, detail="Invalid magic link")
            
        del self._pending_links[email]
        return self._create_session_token(email)

    async def _get_user_from_token(self, token: str) -> Optional[MagicLinkUserSchema]:
        """Validate session token and return user
        
        Args:
            token: Session JWT token
            
        Returns:
            Optional[MagicLinkUserSchema]: User if token is valid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            if payload.get('type') != 'session':
                return None
            return MagicLinkUserSchema(
                email=payload['sub'],
                is_verified=True
            )
        except jwt.PyJWTError:
            return None
