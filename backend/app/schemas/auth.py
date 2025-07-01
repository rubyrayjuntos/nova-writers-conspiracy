"""
Authentication schemas for request/response models
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """User registration request model"""
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., min_length=8, description="Password")
    first_name: Optional[str] = Field(None, max_length=100, description="First name")
    last_name: Optional[str] = Field(None, max_length=100, description="Last name")
    
    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john.doe@example.com",
                "password": "securepassword123",
                "first_name": "John",
                "last_name": "Doe"
            }
        }


class UserLogin(BaseModel):
    """User login request model"""
    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="Password")
    user_agent: Optional[str] = Field(None, description="User agent string")
    ip_address: Optional[str] = Field(None, description="IP address")
    
    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "securepassword123",
                "user_agent": "Mozilla/5.0...",
                "ip_address": "192.168.1.1"
            }
        }


class UserResponse(BaseModel):
    """User response model"""
    id: int
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool
    is_verified: bool
    is_premium: bool
    created_at: Optional[str] = None
    last_login: Optional[str] = None
    writing_preferences: dict
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token response model"""
    access_token: str
    refresh_token: str
    token_type: str
    user: UserResponse
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": 1,
                    "username": "johndoe",
                    "email": "john.doe@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "is_active": True,
                    "is_verified": False,
                    "is_premium": False
                }
            }
        }


class PasswordReset(BaseModel):
    """Password reset request model"""
    email: EmailStr = Field(..., description="Email address")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "john.doe@example.com"
            }
        }


class PasswordChange(BaseModel):
    """Password change request model"""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")
    
    class Config:
        schema_extra = {
            "example": {
                "current_password": "oldpassword123",
                "new_password": "newpassword123"
            }
        }


class UserUpdate(BaseModel):
    """User profile update request model"""
    first_name: Optional[str] = Field(None, max_length=100, description="First name")
    last_name: Optional[str] = Field(None, max_length=100, description="Last name")
    bio: Optional[str] = Field(None, description="User bio")
    avatar_url: Optional[str] = Field(None, description="Avatar URL")
    
    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "bio": "Aspiring novelist and AI enthusiast",
                "avatar_url": "https://example.com/avatar.jpg"
            }
        }


class WritingPreferencesUpdate(BaseModel):
    """Writing preferences update request model"""
    writing_style: Optional[str] = Field(None, description="Writing style preference")
    narrative_structures: Optional[List[str]] = Field(None, description="Preferred narrative structures")
    custom_instructions: Optional[str] = Field(None, description="Custom instructions for agents")
    preferred_genres: Optional[List[str]] = Field(None, description="Preferred genres")
    preferred_tones: Optional[List[str]] = Field(None, description="Preferred tones")
    collaboration_level: Optional[str] = Field(None, description="Collaboration level preference")
    
    class Config:
        schema_extra = {
            "example": {
                "writing_style": "descriptive",
                "narrative_structures": ["three_act", "hero_journey"],
                "custom_instructions": "Always avoid clichés and focus on character development",
                "preferred_genres": ["fantasy", "mystery"],
                "preferred_tones": ["serious", "adventurous"],
                "collaboration_level": "collaborator"
            }
        } 