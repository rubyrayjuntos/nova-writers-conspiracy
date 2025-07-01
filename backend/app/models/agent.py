"""
Agent-related models for storing AI agent interactions and generated content
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class AgentConversation(Base):
    """Model for storing conversations with AI agents"""
    
    __tablename__ = "agent_conversations"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Conversation info
    agent_type = Column(String(50), nullable=False)  # project_manager, researcher, world_builder, character_architect, plotter, writer, editor, illustrator
    conversation_title = Column(String(255))
    
    # Conversation status
    is_active = Column(Boolean, default=True)
    is_resolved = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_message_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="agent_conversations")
    messages = relationship("AgentMessage", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<AgentConversation(id={self.id}, project_id={self.project_id}, agent_type='{self.agent_type}')>"
    
    def to_dict(self) -> dict:
        """Convert conversation to dictionary"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "user_id": self.user_id,
            "agent_type": self.agent_type,
            "conversation_title": self.conversation_title,
            "is_active": self.is_active,
            "is_resolved": self.is_resolved,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_message_at": self.last_message_at.isoformat() if self.last_message_at else None,
        }


class AgentMessage(Base):
    """Model for individual messages in agent conversations"""
    
    __tablename__ = "agent_messages"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    conversation_id = Column(Integer, ForeignKey("agent_conversations.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Message content
    content = Column(Text, nullable=False)
    message_type = Column(String(50), default="text")  # text, command, choice, suggestion, error
    
    # Message metadata
    sender_type = Column(String(50), nullable=False)  # user, agent, system
    agent_type = Column(String(50))  # Only for agent messages
    is_processed = Column(Boolean, default=False)
    
    # Message context
    context_data = Column(JSON, default={})  # Additional context for the message
    referenced_entities = Column(JSON, default=[])  # References to characters, locations, etc.
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("AgentConversation", back_populates="messages")
    user = relationship("User")
    
    def __repr__(self):
        return f"<AgentMessage(id={self.id}, conversation_id={self.conversation_id}, sender_type='{self.sender_type}')>"
    
    def to_dict(self) -> dict:
        """Convert message to dictionary"""
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "user_id": self.user_id,
            "content": self.content,
            "message_type": self.message_type,
            "sender_type": self.sender_type,
            "agent_type": self.agent_type,
            "is_processed": self.is_processed,
            "context_data": self.context_data,
            "referenced_entities": self.referenced_entities,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Character(Base):
    """Model for character profiles created by the Character Architect agent"""
    
    __tablename__ = "characters"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    # Character info
    name = Column(String(255), nullable=False)
    role = Column(String(50), default="supporting")  # protagonist, antagonist, supporting, minor
    
    # Character details
    description = Column(Text)
    backstory = Column(Text)
    personality = Column(JSON, default={})
    physical_description = Column(Text)
    
    # Character relationships
    relationships = Column(JSON, default=[])  # List of relationship objects
    goals = Column(JSON, default=[])
    conflicts = Column(JSON, default=[])
    
    # Character development
    character_arc = Column(Text)
    growth_points = Column(JSON, default=[])
    
    # Character metadata
    tags = Column(JSON, default=[])
    notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="characters")
    
    def __repr__(self):
        return f"<Character(id={self.id}, project_id={self.project_id}, name='{self.name}')>"
    
    def to_dict(self) -> dict:
        """Convert character to dictionary"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "role": self.role,
            "description": self.description,
            "backstory": self.backstory,
            "personality": self.personality,
            "physical_description": self.physical_description,
            "relationships": self.relationships,
            "goals": self.goals,
            "conflicts": self.conflicts,
            "character_arc": self.character_arc,
            "growth_points": self.growth_points,
            "tags": self.tags,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class WorldElement(Base):
    """Model for world-building elements created by the World Builder agent"""
    
    __tablename__ = "world_elements"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    # Element info
    name = Column(String(255), nullable=False)
    element_type = Column(String(50), nullable=False)  # location, culture, technology, magic, history, geography
    
    # Element details
    description = Column(Text, nullable=False)
    details = Column(JSON, default={})
    
    # Element relationships
    connections = Column(JSON, default=[])  # Connections to other world elements
    rules = Column(JSON, default=[])  # Rules or laws governing this element
    
    # Element metadata
    importance_level = Column(String(50), default="medium")  # low, medium, high, critical
    tags = Column(JSON, default=[])
    notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="world_elements")
    
    def __repr__(self):
        return f"<WorldElement(id={self.id}, project_id={self.project_id}, name='{self.name}', type='{self.element_type}')>"
    
    def to_dict(self) -> dict:
        """Convert world element to dictionary"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "element_type": self.element_type,
            "description": self.description,
            "details": self.details,
            "connections": self.connections,
            "rules": self.rules,
            "importance_level": self.importance_level,
            "tags": self.tags,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class PlotPoint(Base):
    """Model for plot points created by the Plotter agent"""
    
    __tablename__ = "plot_points"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    # Plot point info
    title = Column(String(255), nullable=False)
    plot_point_type = Column(String(50), nullable=False)  # inciting_incident, rising_action, climax, falling_action, resolution
    
    # Plot point details
    description = Column(Text, nullable=False)
    summary = Column(Text)
    
    # Plot point structure
    act_number = Column(Integer)  # Which act this belongs to
    sequence_number = Column(Integer)  # Order within the act
    chapter_target = Column(Integer)  # Target chapter for this plot point
    
    # Plot point elements
    characters_involved = Column(JSON, default=[])
    locations_involved = Column(JSON, default=[])
    conflicts = Column(JSON, default=[])
    
    # Plot point metadata
    importance_level = Column(String(50), default="medium")  # low, medium, high, critical
    status = Column(String(50), default="planned")  # planned, in_progress, completed
    notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="plot_points")
    
    def __repr__(self):
        return f"<PlotPoint(id={self.id}, project_id={self.project_id}, title='{self.title}')>"
    
    def to_dict(self) -> dict:
        """Convert plot point to dictionary"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "plot_point_type": self.plot_point_type,
            "description": self.description,
            "summary": self.summary,
            "act_number": self.act_number,
            "sequence_number": self.sequence_number,
            "chapter_target": self.chapter_target,
            "characters_involved": self.characters_involved,
            "locations_involved": self.locations_involved,
            "conflicts": self.conflicts,
            "importance_level": self.importance_level,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        } 