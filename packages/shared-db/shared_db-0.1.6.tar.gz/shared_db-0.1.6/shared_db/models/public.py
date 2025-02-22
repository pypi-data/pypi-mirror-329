from .base import Base, HumanIDMixin
from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TEXT, UUID, JSONB, INTEGER, BOOLEAN


class Profile(Base, HumanIDMixin):
    __tablename__ = "profiles"
    __prefix__ = "prf"
    __id_length__ = 16

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE", onupdate="CASCADE"),
        unique=True,
    )

    # Relationships
    user = relationship("User", back_populates="profile")
    projects = relationship("Project", back_populates="owner")


class Project(Base, HumanIDMixin):
    __tablename__ = "projects"
    __prefix__ = "prj"
    __id_length__ = 16

    name = Column(TEXT, nullable=False)
    description = Column(TEXT, nullable=False)

    # Foreign Keys
    owner_id = Column(
        TEXT,
        ForeignKey("profiles.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    # Relationships
    owner = relationship("Profile", back_populates="projects")
    environments = relationship("Environment", back_populates="project")


class Environment(Base, HumanIDMixin):
    __tablename__ = "environments"
    __prefix__ = "env"
    __id_length__ = 16

    name = Column(TEXT, nullable=False)
    is_main = Column(BOOLEAN, nullable=False, server_default="false")
    is_active = Column(BOOLEAN, nullable=False, server_default="true")

    # Foreign Keys
    project_id = Column(
        TEXT,
        ForeignKey("projects.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    # Relationships
    project = relationship("Project", back_populates="environments")


# class Node(Base, HumanIDMixin):
#     __tablename__ = "nodes"

#     label = Column(TEXT, nullable=False)
#     type = Column(TEXT, nullable=False)
#     position = Column(JSONB, nullable=False)
#     width = Column(INTEGER, nullable=False)
#     height = Column(INTEGER, nullable=False)

#     # Foreign Keys
#     company_id = Column(
#         TEXT,
#         ForeignKey("companies.id", ondelete="CASCADE", onupdate="CASCADE"),
#         nullable=False,
#     )

#     # Relationships
#     company = relationship("Company", back_populates="nodes")


# class Edge(Base, HumanIDMixin):
#     __tablename__ = "edges"

#     source_id = Column(
#         TEXT,
#         ForeignKey("nodes.id", ondelete="CASCADE", onupdate="CASCADE"),
#         nullable=False,
#     )
#     target_id = Column(
#         TEXT,
#         ForeignKey("nodes.id", ondelete="CASCADE", onupdate="CASCADE"),
#         nullable=False,
#     )
#     source_handle = Column(TEXT, nullable=False)
#     target_handle = Column(TEXT, nullable=False)
#     label = Column(TEXT, nullable=False)
#     type = Column(TEXT, nullable=False)
#     animated = Column(BOOLEAN, nullable=False, server_default=text("false"))
#     style = Column(JSONB, nullable=False)

#     # Relationships
#     source = relationship("Node", foreign_keys=[source_id])
#     target = relationship("Node", foreign_keys=[target_id])
