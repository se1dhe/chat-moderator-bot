"""ORM models — core moderation domain (M1)."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Chat(TimestampMixin, Base):
    """A connected group or channel."""

    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    type: Mapped[str] = mapped_column(String(32), default="group")
    title: Mapped[str | None] = mapped_column(String(256))
    lang: Mapped[str] = mapped_column(String(8), default="en")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    # White-label isolation: which brand bot manages this chat (its Telegram id).
    # NULL = legacy/primary; set on first contact. See BotInstance.
    bot_id: Mapped[int | None] = mapped_column(BigInteger, index=True)

    settings: Mapped[ChatSettings] = relationship(
        back_populates="chat", uselist=False, cascade="all, delete-orphan"
    )


class ChatSettings(Base):
    """Per-chat configuration. Free-form fields live in `data` (JSONB)."""

    __tablename__ = "chat_settings"

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), primary_key=True)
    warn_limit: Mapped[int] = mapped_column(Integer, default=3)
    warn_action: Mapped[str] = mapped_column(String(16), default="mute")  # mute|ban|kick
    ai_mode: Mapped[str] = mapped_column(String(16), default="off")  # off|quarantine|autoban
    ai_threshold: Mapped[int] = mapped_column(Integer, default=80)  # 0..100 confidence %
    ai_provider: Mapped[str] = mapped_column(String(16), default="ollama", server_default="ollama")
    ai_model: Mapped[str | None] = mapped_column(String(64), nullable=True)
    ai_api_key_encrypted: Mapped[str | None] = mapped_column(Text, nullable=True)
    data: Mapped[dict] = mapped_column(JSONB, default=dict)

    chat: Mapped[Chat] = relationship(back_populates="settings")


class User(TimestampMixin, Base):
    """Global user profile (basis for cross-chat reputation later)."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(64))
    full_name: Mapped[str | None] = mapped_column(String(256))
    lang: Mapped[str] = mapped_column(String(8), default="en")
    trust_score: Mapped[int] = mapped_column(Integer, default=50)  # 0..100


class Warn(TimestampMixin, Base):
    __tablename__ = "warns"
    __table_args__ = (Index("ix_warns_chat_user", "chat_telegram_id", "user_telegram_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_telegram_id: Mapped[int] = mapped_column(BigInteger)
    user_telegram_id: Mapped[int] = mapped_column(BigInteger)
    issued_by: Mapped[int] = mapped_column(BigInteger)
    reason: Mapped[str | None] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class ModAction(TimestampMixin, Base):
    """Audit log of every moderation action."""

    __tablename__ = "mod_actions"
    __table_args__ = (Index("ix_modactions_chat", "chat_telegram_id", "created_at"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_telegram_id: Mapped[int] = mapped_column(BigInteger)
    user_telegram_id: Mapped[int | None] = mapped_column(BigInteger)
    actor_id: Mapped[int | None] = mapped_column(BigInteger)  # None = RedQueen/AI
    action: Mapped[str] = mapped_column(String(32))  # ban|kick|mute|warn|unban|ai_quarantine
    reason: Mapped[str | None] = mapped_column(Text)
    meta: Mapped[dict] = mapped_column(JSONB, default=dict)


class AIVerdict(TimestampMixin, Base):
    """Explainable AI moderation verdict on a message."""

    __tablename__ = "ai_verdicts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_telegram_id: Mapped[int] = mapped_column(BigInteger, index=True)
    user_telegram_id: Mapped[int] = mapped_column(BigInteger)
    message_id: Mapped[int | None] = mapped_column(BigInteger)
    category: Mapped[str] = mapped_column(String(32))  # spam|scam|toxicity|nsfw|flood|ok
    score: Mapped[int] = mapped_column(Integer)  # 0..100
    explanation: Mapped[str | None] = mapped_column(Text)
    text: Mapped[str | None] = mapped_column(Text)  # flagged message text (queue view + Rule action)
    status: Mapped[str] = mapped_column(String(16), default="pending")  # pending|approved|rejected
    decided_by: Mapped[int | None] = mapped_column(BigInteger)


class Subscription(TimestampMixin, Base):
    """Pro subscription per chat."""

    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    plan: Mapped[str] = mapped_column(String(16), default="free")  # free|pro
    active_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class BotInstance(TimestampMixin, Base):
    """Registry of brand bots running over this shared database (white-label / clones).

    Tokens live in env (BOT_TOKENS), not here; this table records identity + branding so
    the fleet can be listed and data can be isolated per bot via `Chat.bot_id`.
    """

    __tablename__ = "bot_instances"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bot_telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(64))
    brand: Mapped[str] = mapped_column(String(64), default="RedQueen")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class ChatMember(Base):
    """A member the bot has seen in a chat — the searchable roster the Mini App acts on.

    Telegram's Bot API can't enumerate chat members, so we build this from observed
    messages: who wrote, when, how often. Powers member search + moderation from the TMA.
    """

    __tablename__ = "chat_members"
    __table_args__ = (
        UniqueConstraint("chat_telegram_id", "user_telegram_id", name="uq_chat_member"),
        Index("ix_chat_members_chat", "chat_telegram_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_telegram_id: Mapped[int] = mapped_column(BigInteger)
    user_telegram_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str | None] = mapped_column(String(64))
    full_name: Mapped[str | None] = mapped_column(String(256))
    message_count: Mapped[int] = mapped_column(Integer, default=0)
    # Last known moderation state, so the Mini App can show contextual actions
    # (only offer "unban" for a banned member, "unmute" for a muted one, etc.).
    state: Mapped[str] = mapped_column(String(16), default="active")  # active|muted|banned
    muted_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Payment(TimestampMixin, Base):
    """Telegram Stars payment ledger — one row per successful charge (and refunds)."""

    __tablename__ = "payments"
    __table_args__ = (Index("ix_payments_chat", "chat_telegram_id", "created_at"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_telegram_id: Mapped[int] = mapped_column(BigInteger)
    payer_id: Mapped[int] = mapped_column(BigInteger)
    stars: Mapped[int] = mapped_column(Integer)  # XTR amount
    plan: Mapped[str] = mapped_column(String(16), default="pro")
    period_days: Mapped[int] = mapped_column(Integer, default=30)
    telegram_payment_charge_id: Mapped[str | None] = mapped_column(String(128), unique=True)
    status: Mapped[str] = mapped_column(String(16), default="paid")  # paid|refunded


class CaptchaSession(TimestampMixin, Base):
    """A pending/resolved join-verification challenge for one user in one chat."""

    __tablename__ = "captcha_sessions"
    __table_args__ = (Index("ix_captcha_chat_user", "chat_telegram_id", "user_telegram_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_telegram_id: Mapped[int] = mapped_column(BigInteger)
    user_telegram_id: Mapped[int] = mapped_column(BigInteger)
    kind: Mapped[str] = mapped_column(String(16))  # button|math
    answer: Mapped[int] = mapped_column(Integer, default=1)  # correct choice value
    is_join_request: Mapped[bool] = mapped_column(Boolean, default=False)
    prompt_message_id: Mapped[int | None] = mapped_column(BigInteger)
    status: Mapped[str] = mapped_column(String(16), default="pending")  # pending|passed|failed|expired
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class RaidEvent(TimestampMixin, Base):
    """Audit record of a raid-shield auto-lock (coordinated join surge)."""

    __tablename__ = "raid_events"
    __table_args__ = (Index("ix_raid_events_chat", "chat_telegram_id", "created_at"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_telegram_id: Mapped[int] = mapped_column(BigInteger)
    join_count: Mapped[int] = mapped_column(Integer)
    window_seconds: Mapped[int] = mapped_column(Integer)
    locked_until: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    resolved_by: Mapped[int | None] = mapped_column(BigInteger)  # admin who ran /unlock early, if any
