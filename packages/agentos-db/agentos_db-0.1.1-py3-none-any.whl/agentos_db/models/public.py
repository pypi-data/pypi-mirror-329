from .base import Base, HumanIDMixin
from sqlalchemy import Column, ForeignKey, text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TEXT, UUID, JSONB, INTEGER, BOOLEAN, ARRAY


class User(Base, HumanIDMixin):
    __tablename__ = "users"
    __prefix__ = "usr"
    __id_length__ = 16

    id = Column(TEXT, primary_key=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    # Relationships
    user = relationship("User", back_populates="user")
    projects = relationship("Project", back_populates="owner")


class Project(Base, HumanIDMixin):
    __tablename__ = "projects"
    __prefix__ = "prj"
    __id_length__ = 16

    id = Column(TEXT, primary_key=True)
    api_key = Column(TEXT, nullable=False, unique=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    name = Column(TEXT, nullable=False)
    description = Column(TEXT, nullable=False)

    # Foreign Keys
    owner_id = Column(
        TEXT,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    # Relationships
    owner = relationship("User", back_populates="projects")
    environments = relationship("Environment", back_populates="project")


class Environment(Base, HumanIDMixin):
    __tablename__ = "environments"
    __prefix__ = "env"
    __id_length__ = 16

    id = Column(TEXT, primary_key=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
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
    agents = relationship("Agent", back_populates="environment")


class Agent(Base, HumanIDMixin):
    __tablename__ = "agents"
    __prefix__ = "agt"
    __id_length__ = 16

    id = Column(TEXT, primary_key=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    # Relationships
    name = Column(TEXT, nullable=False)
    prompt = Column(TEXT, nullable=False)
    tools = Column(ARRAY(TEXT), nullable=False)
    model = Column(TEXT, nullable=False)

    # Foreign Keys
    environment_id = Column(
        TEXT,
        ForeignKey("environments.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    # Relationships
    environment = relationship("Environment", back_populates="agents")


# class Node(Base, HumanIDMixin):
#     __tablename__ = "nodes"
#     __prefix__ = "nde"
#     __id_length__ = 16

#     id = Column(TEXT, primary_key=True)
#     created_at = Column(
#         TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
#     )
#     type = Column(TEXT, nullable=False)
#     label = Column(TEXT, nullable=False)
#     position = Column(JSONB, nullable=False)
#     width = Column(INTEGER, nullable=False)
#     height = Column(INTEGER, nullable=False)
#     data = Column(JSONB, nullable=True)  # For any additional node-specific data

#     # Foreign Keys
#     environment_id = Column(
#         TEXT,
#         ForeignKey("environments.id", ondelete="CASCADE", onupdate="CASCADE"),
#         nullable=False,
#     )

#     # Optional: Keep track of node across environments
#     original_node_id = Column(
#         TEXT,
#         ForeignKey("nodes.id", ondelete="SET NULL", onupdate="CASCADE"),
#         nullable=True,
#     )

#     # Relationships
#     environment = relationship("Environment", back_populates="nodes")
#     source_edges = relationship(
#         "Edge", back_populates="source", foreign_keys="Edge.source_id"
#     )
#     target_edges = relationship(
#         "Edge", back_populates="target", foreign_keys="Edge.target_id"
#     )
#     agent = relationship("Agent", back_populates="node")


# class Edge(Base, HumanIDMixin):
#     __tablename__ = "edges"
#     __prefix__ = "edg"
#     __id_length__ = 16

#     id = Column(TEXT, primary_key=True)
#     created_at = Column(
#         TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
#     )
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
#     label = Column(TEXT, nullable=True)
#     type = Column(TEXT, nullable=False)
#     animated = Column(BOOLEAN, nullable=False, server_default=text("false"))
#     style = Column(JSONB, nullable=True)
#     data = Column(JSONB, nullable=True)  # For any additional edge-specific data

#     # Optional: Keep track of edge across environments
#     original_edge_id = Column(
#         TEXT,
#         ForeignKey("edges.id", ondelete="SET NULL", onupdate="CASCADE"),
#         nullable=True,
#     )

#     # Relationships
#     source = relationship(
#         "Node", foreign_keys=[source_id], back_populates="source_edges"
#     )
#     target = relationship(
#         "Node", foreign_keys=[target_id], back_populates="target_edges"
#     )
