"""
Project model for novel writing projects
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.core.database import Base


class Project(Base):
    """Project model for novel writing projects"""
    
    __tablename__ = "projects"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Basic project info
    title = Column(String(255), nullable=False)
    concept = Column(Text, nullable=False)  # Core concept/logline
    genre = Column(JSON, nullable=False)  # List of genres
    tone = Column(JSON, nullable=False)  # List of tones
    
    # Collaboration level
    collaboration_level = Column(String(50), default="collaborator")  # architect, director, collaborator, assistant
    
    # Project status
    status = Column(String(50), default="planning")  # planning, researching, world_building, character_design, plotting, writing, editing, completed, paused
    current_phase = Column(String(50), default="planning")
    progress_percentage = Column(Float, default=0.0)
    
    # Project metadata
    target_word_count = Column(Integer, default=80000)
    current_word_count = Column(Integer, default=0)
    estimated_completion_date = Column(DateTime)
    
    # Project settings
    settings = Column(JSON, default={
        "auto_save": True,
        "version_control": True,
        "collaboration_enabled": True,
        "export_formats": ["docx", "pdf", "epub"],
        "notification_preferences": {
            "email": True,
            "in_app": True,
            "agent_updates": True,
        }
    })
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="projects")
    chapters = relationship("Chapter", back_populates="project", cascade="all, delete-orphan")
    characters = relationship("Character", back_populates="project", cascade="all, delete-orphan")
    world_elements = relationship("WorldElement", back_populates="project", cascade="all, delete-orphan")
    plot_points = relationship("PlotPoint", back_populates="project", cascade="all, delete-orphan")
    snapshots = relationship("ProjectSnapshot", back_populates="project", cascade="all, delete-orphan")
    agent_conversations = relationship("AgentConversation", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project(id={self.id}, title='{self.title}', status='{self.status}')>"
    
    def to_dict(self) -> dict:
        """Convert project to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "concept": self.concept,
            "genre": self.genre,
            "tone": self.tone,
            "collaboration_level": self.collaboration_level,
            "status": self.status,
            "current_phase": self.current_phase,
            "progress_percentage": self.progress_percentage,
            "target_word_count": self.target_word_count,
            "current_word_count": self.current_word_count,
            "estimated_completion_date": self.estimated_completion_date.isoformat() if self.estimated_completion_date else None,
            "settings": self.settings,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
        }
    
    def update_progress(self):
        """Update project progress based on current state"""
        if self.current_word_count and self.target_word_count:
            self.progress_percentage = min(100.0, (self.current_word_count / self.target_word_count) * 100)
        else:
            # Progress based on phases
            phase_progress = {
                "planning": 5.0,
                "researching": 15.0,
                "world_building": 25.0,
                "character_design": 35.0,
                "plotting": 45.0,
                "writing": 75.0,
                "editing": 90.0,
                "completed": 100.0,
            }
            self.progress_percentage = phase_progress.get(self.current_phase, 0.0)


class Chapter(Base):
    """Chapter model for manuscript content"""
    
    __tablename__ = "chapters"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    # Chapter info
    chapter_number = Column(Integer, nullable=False)
    title = Column(String(255))
    content = Column(Text)
    word_count = Column(Integer, default=0)
    
    # Chapter status
    status = Column(String(50), default="draft")  # draft, in_progress, completed, edited, approved
    version = Column(Integer, default=1)
    
    # Chapter metadata
    summary = Column(Text)
    notes = Column(Text)
    tags = Column(JSON, default=[])
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="chapters")
    comments = relationship("ChapterComment", back_populates="chapter", cascade="all, delete-orphan")
    versions = relationship("ChapterVersion", back_populates="chapter", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Chapter(id={self.id}, project_id={self.project_id}, chapter_number={self.chapter_number})>"
    
    def to_dict(self) -> dict:
        """Convert chapter to dictionary"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "chapter_number": self.chapter_number,
            "title": self.title,
            "content": self.content,
            "word_count": self.word_count,
            "status": self.status,
            "version": self.version,
            "summary": self.summary,
            "notes": self.notes,
            "tags": self.tags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class ChapterVersion(Base):
    """Chapter version history"""
    
    __tablename__ = "chapter_versions"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=False)
    
    # Version info
    version_number = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    word_count = Column(Integer, default=0)
    
    # Version metadata
    change_summary = Column(Text)
    created_by = Column(String(50), default="system")  # user, agent, system
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    chapter = relationship("Chapter", back_populates="versions")
    
    def __repr__(self):
        return f"<ChapterVersion(id={self.id}, chapter_id={self.chapter_id}, version_number={self.version_number})>"


class ChapterComment(Base):
    """Comments on chapters"""
    
    __tablename__ = "chapter_comments"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Comment content
    content = Column(Text, nullable=False)
    comment_type = Column(String(50), default="general")  # general, suggestion, question, feedback
    
    # Comment metadata
    line_number = Column(Integer)  # For inline comments
    selection_text = Column(Text)  # For selected text comments
    is_resolved = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    chapter = relationship("Chapter", back_populates="comments")
    user = relationship("User")
    
    def __repr__(self):
        return f"<ChapterComment(id={self.id}, chapter_id={self.chapter_id}, user_id={self.user_id})>"


class ProjectSnapshot(Base):
    """Project snapshots for version control"""
    
    __tablename__ = "project_snapshots"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    # Snapshot info
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Snapshot data (JSON representation of project state)
    snapshot_data = Column(JSON, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="snapshots")
    
    def __repr__(self):
        return f"<ProjectSnapshot(id={self.id}, project_id={self.project_id}, name='{self.name}')>" 