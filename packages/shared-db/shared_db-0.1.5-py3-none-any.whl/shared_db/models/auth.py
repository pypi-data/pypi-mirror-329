from sqlalchemy import Column, String, BOOLEAN, SmallInteger
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, TEXT, JSONB
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'auth'}

    id = Column(UUID(as_uuid=True), primary_key=True)
    instance_id = Column(UUID(as_uuid=True), nullable=True)
    aud = Column(String(255), nullable=True)
    role = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    encrypted_password = Column(String(255), nullable=True)
    email_confirmed_at = Column(TIMESTAMP(timezone=True), nullable=True)
    invited_at = Column(TIMESTAMP(timezone=True), nullable=True)
    confirmation_token = Column(String(255), nullable=True)
    confirmation_sent_at = Column(TIMESTAMP(timezone=True), nullable=True)
    recovery_token = Column(String(255), nullable=True)
    recovery_sent_at = Column(TIMESTAMP(timezone=True), nullable=True)
    email_change_token_new = Column(String(255), nullable=True)
    email_change = Column(String(255), nullable=True)
    email_change_sent_at = Column(TIMESTAMP(timezone=True), nullable=True)
    last_sign_in_at = Column(TIMESTAMP(timezone=True), nullable=True)
    raw_app_meta_data = Column(JSONB, nullable=True)
    raw_user_meta_data = Column(JSONB, nullable=True)
    is_super_admin = Column(BOOLEAN, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    phone = Column(TEXT, nullable=True)
    phone_confirmed_at = Column(TIMESTAMP(timezone=True), nullable=True)
    phone_change = Column(TEXT, nullable=True, default='')
    phone_change_token = Column(String(255), nullable=True, default='')
    phone_change_sent_at = Column(TIMESTAMP(timezone=True), nullable=True)
    email_change_token_current = Column(String(255), nullable=True, default='')
    email_change_confirm_status = Column(SmallInteger, nullable=True, default=0)
    banned_until = Column(TIMESTAMP(timezone=True), nullable=True)
    reauthentication_token = Column(String(255), nullable=True, default='')
    reauthentication_sent_at = Column(TIMESTAMP(timezone=True), nullable=True)
    is_sso_user = Column(BOOLEAN, nullable=False, default=False)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    # Relationships
    profile = relationship("Profile", back_populates="user")
