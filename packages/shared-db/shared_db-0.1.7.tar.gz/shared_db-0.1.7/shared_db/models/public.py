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
    nodes = relationship("Node", back_populates="project")


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


class Node(Base, HumanIDMixin):
    __tablename__ = "nodes"
    __prefix__ = "nde"
    __id_length__ = 16

    label = Column(TEXT, nullable=False)
    position = Column(JSONB, nullable=False)
    width = Column(INTEGER, nullable=False)
    height = Column(INTEGER, nullable=False)
    data = Column(JSONB, nullable=True)  # For any additional node-specific data

    # Foreign Keys
    environment_id = Column(
        TEXT,
        ForeignKey("environments.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    # Optional: Keep track of node across environments
    original_node_id = Column(
        TEXT,
        ForeignKey("nodes.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )

    # Relationships
    environment = relationship("Environment", back_populates="nodes")
    source_edges = relationship(
        "Edge", back_populates="source", foreign_keys="Edge.source_id"
    )
    target_edges = relationship(
        "Edge", back_populates="target", foreign_keys="Edge.target_id"
    )


class Edge(Base, HumanIDMixin):
    __tablename__ = "edges"
    __prefix__ = "edg"
    __id_length__ = 16

    source_id = Column(
        TEXT,
        ForeignKey("nodes.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    target_id = Column(
        TEXT,
        ForeignKey("nodes.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    source_handle = Column(TEXT, nullable=False)
    target_handle = Column(TEXT, nullable=False)
    label = Column(TEXT, nullable=True)
    type = Column(TEXT, nullable=False)
    animated = Column(BOOLEAN, nullable=False, server_default=text("false"))
    style = Column(JSONB, nullable=True)
    data = Column(JSONB, nullable=True)  # For any additional edge-specific data

    # Optional: Keep track of edge across environments
    original_edge_id = Column(
        TEXT,
        ForeignKey("edges.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )

    # Relationships
    source = relationship(
        "Node", foreign_keys=[source_id], back_populates="source_edges"
    )
    target = relationship(
        "Node", foreign_keys=[target_id], back_populates="target_edges"
    )
