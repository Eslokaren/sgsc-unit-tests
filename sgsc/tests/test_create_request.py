import pytest
from unittest.mock import Mock
from sgsc.services import create_request, ValidationError, AuthorizationError
from sgsc.models import Request, Status


def test_create_request_success():
    repo = Mock()
    repo.save.side_effect = lambda r: r

    req = create_request(
        repo,
        user_is_authenticated=True,
        user_can_create=True,
        request_type="Administrative Request",
        description="Request for document processing",
        department="Citizen Services",
        priority="Medium",
    )

    assert isinstance(req, Request)
    assert req.status == Status.RECEIVED
    assert req.priority == "medium"
    repo.save.assert_called_once()


def test_create_request_missing_description_fails():
    repo = Mock()
    with pytest.raises(ValidationError):
        create_request(
            repo,
            user_is_authenticated=True,
            user_can_create=True,
            request_type="Administrative Request",
            description="   ",
            department="Citizen Services",
            priority="Medium",
        )
    repo.save.assert_not_called()


def test_create_request_unauthenticated_fails():
    repo = Mock()
    with pytest.raises(AuthorizationError):
        create_request(
            repo,
            user_is_authenticated=False,
            user_can_create=True,
            request_type="Administrative Request",
            description="Ok",
            department="Citizen Services",
            priority="Medium",
        )
    repo.save.assert_not_called()


def test_create_request_invalid_priority_fails():
    repo = Mock()
    with pytest.raises(ValidationError):
        create_request(
            repo,
            user_is_authenticated=True,
            user_can_create=True,
            request_type="Administrative Request",
            description="Ok",
            department="Citizen Services",
            priority="Urgent",
        )
    repo.save.assert_not_called()
