from dataclasses import replace
from typing import Set
from uuid import uuid4

from .models import Request, Status


VALID_PRIORITIES: Set[str] = {"low", "medium", "high"}

ALLOWED_TRANSITIONS = {
    Status.RECEIVED: {Status.IN_PROGRESS, Status.OBSERVED},
    Status.IN_PROGRESS: {Status.OBSERVED, Status.FINISHED},
    Status.OBSERVED: {Status.IN_PROGRESS, Status.FINISHED},
    Status.FINISHED: set(),
}


class ValidationError(ValueError):
    pass


class NotFoundError(LookupError):
    pass


class AuthorizationError(PermissionError):
    pass


def create_request(
    repo,
    *,
    user_is_authenticated: bool,
    user_can_create: bool,
    request_type: str,
    description: str,
    department: str,
    priority: str,
) -> Request:
    if not user_is_authenticated:
        raise AuthorizationError("User must be authenticated.")
    if not user_can_create:
        raise AuthorizationError("User not authorized to create requests.")

    if not request_type.strip():
        raise ValidationError("request_type is required.")
    if not description.strip():
        raise ValidationError("description is required.")
    if not department.strip():
        raise ValidationError("department is required.")
    if priority.lower().strip() not in VALID_PRIORITIES:
        raise ValidationError("priority must be low/medium/high.")

    req = Request(
        id=str(uuid4()),
        request_type=request_type.strip(),
        description=description.strip(),
        department=department.strip(),
        priority=priority.lower().strip(),
        status=Status.RECEIVED,
    )
    return repo.save(req)


def change_request_status(
    repo,
    *,
    user_is_authenticated: bool,
    user_can_update: bool,
    request_id: str,
    new_status: Status,
) -> Request:
    if not user_is_authenticated:
        raise AuthorizationError("User must be authenticated.")
    if not user_can_update:
        raise AuthorizationError("User not authorized to update status.")

    existing = repo.get_by_id(request_id)
    if existing is None:
        raise NotFoundError("Request not found.")

    allowed = ALLOWED_TRANSITIONS.get(existing.status, set())
    if new_status not in allowed:
        raise ValidationError(f"Invalid transition: {existing.status} -> {new_status}")

    updated = replace(existing, status=new_status)
    return repo.save(updated)
