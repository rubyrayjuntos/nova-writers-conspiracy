"""
Authentication service for user management and token handling
"""

from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.models.user import User, UserSession
from app.schemas.auth import UserRegister

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Authentication service class"""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Generate password hash"""
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email address"""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """Get user by username"""
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[User]:
        """Authenticate user with username/email and password"""
        # Try to find user by username or email
        user = await AuthService.get_user_by_username(db, username)
        if not user:
            user = await AuthService.get_user_by_email(db, username)
        
        if not user:
            return None
        
        if not AuthService.verify_password(password, user.hashed_password):
            return None
        
        return user
    
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserRegister) -> User:
        """Create a new user"""
        hashed_password = AuthService.get_password_hash(user_data.password)
        
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        return user
    
    @staticmethod
    async def create_user_session(
        db: AsyncSession,
        user_id: int,
        access_token: str,
        refresh_token: str,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> UserSession:
        """Create a new user session"""
        # Calculate expiration times
        access_expires = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_expires = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        session = UserSession(
            user_id=user_id,
            session_token=access_token,
            refresh_token=refresh_token,
            user_agent=user_agent,
            ip_address=ip_address,
            expires_at=refresh_expires,
        )
        
        db.add(session)
        await db.commit()
        await db.refresh(session)
        
        return session
    
    @staticmethod
    async def get_user_session(db: AsyncSession, session_token: str) -> Optional[UserSession]:
        """Get user session by token"""
        result = await db.execute(
            select(UserSession).where(
                UserSession.session_token == session_token,
                UserSession.is_active == True
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def invalidate_user_sessions(db: AsyncSession, user_id: int) -> None:
        """Invalidate all sessions for a user"""
        result = await db.execute(
            select(UserSession).where(
                UserSession.user_id == user_id,
                UserSession.is_active == True
            )
        )
        sessions = result.scalars().all()
        
        for session in sessions:
            session.is_active = False
        
        await db.commit()
    
    @staticmethod
    async def invalidate_session(db: AsyncSession, session_token: str) -> bool:
        """Invalidate a specific session"""
        session = await AuthService.get_user_session(db, session_token)
        if session:
            session.is_active = False
            await db.commit()
            return True
        return False
    
    @staticmethod
    async def update_session_activity(db: AsyncSession, session_token: str) -> None:
        """Update session last activity timestamp"""
        session = await AuthService.get_user_session(db, session_token)
        if session:
            session.last_used = datetime.utcnow()
            await db.commit()
    
    @staticmethod
    async def cleanup_expired_sessions(db: AsyncSession) -> int:
        """Clean up expired sessions"""
        result = await db.execute(
            select(UserSession).where(
                UserSession.expires_at < datetime.utcnow(),
                UserSession.is_active == True
            )
        )
        expired_sessions = result.scalars().all()
        
        count = 0
        for session in expired_sessions:
            session.is_active = False
            count += 1
        
        await db.commit()
        return count
    
    @staticmethod
    async def update_user_preferences(
        db: AsyncSession,
        user_id: int,
        preferences: dict
    ) -> Optional[User]:
        """Update user writing preferences"""
        user = await AuthService.get_user_by_id(db, user_id)
        if user:
            user.writing_preferences.update(preferences)
            await db.commit()
            await db.refresh(user)
        return user
    
    @staticmethod
    async def update_user_profile(
        db: AsyncSession,
        user_id: int,
        profile_data: dict
    ) -> Optional[User]:
        """Update user profile information"""
        user = await AuthService.get_user_by_id(db, user_id)
        if user:
            for field, value in profile_data.items():
                if hasattr(user, field) and value is not None:
                    setattr(user, field, value)
            
            await db.commit()
            await db.refresh(user)
        return user
    
    @staticmethod
    async def change_user_password(
        db: AsyncSession,
        user_id: int,
        current_password: str,
        new_password: str
    ) -> bool:
        """Change user password"""
        user = await AuthService.get_user_by_id(db, user_id)
        if not user:
            return False
        
        # Verify current password
        if not AuthService.verify_password(current_password, user.hashed_password):
            return False
        
        # Update password
        user.hashed_password = AuthService.get_password_hash(new_password)
        await db.commit()
        
        return True 