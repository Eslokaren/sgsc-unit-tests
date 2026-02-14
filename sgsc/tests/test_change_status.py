import pytest
from unittest.mock import Mock
from sgsc.models import Request, Status
from sgsc.services import change_request_status, ValidationError, NotFoundError, AuthorizationError


def test_change_status_success_received_to_in_progress():
    repo = Mock()
    existing = Request(
        id="REQ-1",
        request_type="Administrative Request",
        description="Desc",
        department="Citizen Services",
        priority="medium",
        status=Status.RECEIVED,
    )
    repo.get_by_id.return_value = existing
    repo.save.side_effect = lambda r: r

    updated = change_request_status(
        repo,
        user_is_authenticated=True,
        user_can_update=True,
        request_id="REQ-1",
        new_status=Status.IN_PROGRESS,
    )

    assert updated.status == Status.IN_PROGRESS
    repo.get_by_id.assert_called_once_with("REQ-1")
    repo.save.assert_called_once()


def test_change_status_invalid_transition_fails():
    repo = Mock()
    existing = Request(
        id="REQ-2",
        request_type="Administrative Request",
        description="Desc",
        department="Citizen Services",
        priority="medium",
        status=Status.RECEIVED,
    )
    repo.get_by_id.return_value = existing

    with pytest.raises(ValidationError):
        change_request_status(
            repo,
            user_is_authenticated=True,
            user_can_update=True,
            request_id="REQ-2",
            new_status=Status.FINISHED,
        )
    repo.save.assert_not_called()


def test_change_status_request_not_found():
    repo = Mock()
    repo.get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        change_request_status(
            repo,
            user_is_authenticated=True,
            user_can_update=True,
            request_id="REQ-404",
            new_status=Status.IN_PROGRESS,
        )
    repo.save.assert_not_called()


def test_change_status_unauthorized_fails():
    repo = Mock()
    with pytest.raises(AuthorizationError):
        change_request_status(
            repo,
            user_is_authenticated=True,
            user_can_update=False,
            request_id="REQ-1",
            new_status=Status.IN_PROGRESS,
        )
