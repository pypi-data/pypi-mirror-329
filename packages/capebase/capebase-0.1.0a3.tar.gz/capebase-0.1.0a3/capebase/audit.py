from datetime import datetime
from typing import Any, Dict, Optional, Type
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from sqlalchemy import event, JSON
from sqlalchemy.orm import Session

class AuditLog(SQLModel, table=True):
    """Model for storing audit logs"""
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    table_name: str
    record_id: str
    user_id: Optional[str]
    action: str  # "INSERT", "UPDATE", "DELETE"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    old_values: Optional[Dict[str, Any]] = Field(default=None, sa_type=JSON)
    new_values: Optional[Dict[str, Any]] = Field(default=None, sa_type=JSON)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }

def _get_auth_user_id(session: Session) -> Optional[str]:
    """Extract user_id from session's auth context"""
    auth_context = session.info.get("auth_context")
    return auth_context.id if auth_context else None

def _serialize_model(model: SQLModel) -> dict:
    """Convert model to dictionary, handling special types"""
    data = model.__dict__.copy()
    data.pop('_sa_instance_state', None)
    
    # Convert special types to string representation
    for key, value in data.items():
        if isinstance(value, (datetime, UUID)):
            data[key] = str(value)
    return data

def enable_audit_trail(model_class: Type[SQLModel]):
    """Enable audit trail for a specific model"""
    table = str(model_class.__tablename__)

    # Model-level events (for SQLModel/ORM operations)
    @event.listens_for(model_class, 'after_insert')
    def after_insert(mapper, connection, target):
        audit = AuditLog(
            table_name=model_class.__tablename__,
            record_id=str(target.id),
            user_id=_get_auth_user_id(Session.object_session(target)),
            action="INSERT",
            new_values=_serialize_model(target)
        )
        # Insert directly using connection
        stmt = AuditLog.__table__.insert().values(**audit.model_dump(exclude={'id'}))
        connection.execute(stmt)

    @event.listens_for(model_class, 'after_update')
    def after_update(mapper, connection, target):
        # Get the history of changes
        changes = {}
        old_values = {}
        
        for attr in mapper.attrs:
            hist = getattr(target, '_sa_instance_state').attrs[attr.key].history
            if hist.has_changes():
                changes[attr.key] = hist.added[0] if hist.added else None
                old_values[attr.key] = hist.deleted[0] if hist.deleted else None

        if changes:  # Only create audit log if there were actual changes
            audit = AuditLog(
                table_name=model_class.__tablename__,
                record_id=str(target.id),
                user_id=_get_auth_user_id(Session.object_session(target)),
                action="UPDATE",
                old_values=old_values,
                new_values=changes
            )
            stmt = AuditLog.__table__.insert().values(**audit.model_dump(exclude={'id'}))
            connection.execute(stmt)

    @event.listens_for(model_class, 'after_delete')
    def after_delete(mapper, connection, target):
        audit = AuditLog(
            table_name=model_class.__tablename__,
            record_id=str(target.id),
            user_id=_get_auth_user_id(Session.object_session(target)),
            action="DELETE",
            old_values=_serialize_model(target)
        )
        stmt = AuditLog.__table__.insert().values(**audit.model_dump(exclude={'id'}))
        connection.execute(stmt)

    @event.listens_for(Session, "after_bulk_insert")
    def session_after_bulk_insert(session, query, query_context, result):
        # Check if the bulk INSERT was on the table we're auditing.
        if query_context.compiled.statement.table.name != table_name:
            return
        # query_context.parameters is a list of dicts (one per row inserted).
        for params in query_context.parameters:
            audit = AuditLog(
                table_name=table_name,
                # Bulk inserts may not return primary keys – adjust as needed.
                record_id=str(params.get("id", "unknown")),
                user_id=_get_auth_user_id(session),
                action="INSERT",
                new_values=params
            )
            session.add(audit)

    @event.listens_for(Session, "after_bulk_update")
    def session_after_bulk_update(session, query, query_context, result):
        if query_context.compiled.statement.table.name != table_name:
            return
        for params in query_context.parameters:
            audit = AuditLog(
                table_name=table_name,
                record_id=str(params.get("id", "unknown")),
                user_id=_get_auth_user_id(session),
                action="UPDATE",
                new_values=params
            )
            session.add(audit)

    @event.listens_for(Session, "after_bulk_delete")
    def session_after_bulk_delete(session, query, query_context, result):
        if query_context.compiled.statement.table.name != table_name:
            return
        for params in query_context.parameters:
            audit = AuditLog(
                table_name=table_name,
                record_id=str(params.get("id", "unknown")),
                user_id=_get_auth_user_id(session),
                action="DELETE",
                old_values=params
            )
            session.add(audit)