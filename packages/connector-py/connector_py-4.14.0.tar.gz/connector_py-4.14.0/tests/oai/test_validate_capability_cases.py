"""Test cases for ``validate_capability`` function."""

import typing as t

import pytest_cases
from connector.generated import (
    ListAccountsRequest,
    ListAccountsResponse,
    ListResourcesRequest,
    StandardCapabilityName,
)
from connector.oai.capability import (
    CapabilityCallableProto,
)

Case: t.TypeAlias = tuple[
    StandardCapabilityName,
    CapabilityCallableProto[t.Any],
]


class CustomListAccountsRequest(ListAccountsRequest):
    """Correct custom request for list-accounts capability."""

    extra: str


class CustomListAccountsRequestFromBadBase(ListResourcesRequest):
    """Incorrect base is used for custom request schema."""

    extra: str


class CustomListAccountsResponse(ListAccountsResponse):
    """Subclassing response type is always bad."""

    extra_resp: str


@pytest_cases.case(tags=("valid",))
def case_valid_capability_base_annotation() -> Case:
    def capability(request: ListAccountsRequest) -> ListAccountsResponse:
        raise NotImplementedError

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    return capability_name, capability  # type: ignore


@pytest_cases.case(tags=("valid",))
def case_valid_capability_custom_request() -> Case:
    """Using subclass of matching request type is valid.

    Using subclass of ListAccountsRequest for list-accounts capability
    is absolutely fine.
    """

    def capability(request: CustomListAccountsRequest) -> ListAccountsResponse:
        raise NotImplementedError

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    return capability_name, capability  # type: ignore


@pytest_cases.case(tags=("invalid",))
def case_invalid_capability_custom_response() -> Case:
    """Using subclass of SDK defined response is not correct.

    This would change the output of the method, making it super hard to
    use.
    """

    def capability(request: ListAccountsRequest) -> CustomListAccountsResponse:
        raise NotImplementedError

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    return capability_name, capability  # type: ignore


@pytest_cases.case(tags=("invalid",))
def case_invalid_capability_bad_request_model() -> Case:
    """Using mismatching request type for capability is invalid.

    Using ListResourcesRequest for list-accounts method is obviously
    invalid.
    """

    def capability(request: ListResourcesRequest) -> ListAccountsResponse:
        raise NotImplementedError

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    return capability_name, capability  # type: ignore


@pytest_cases.case(tags=("invalid",))
def case_invalid_capability_bad_request_base_model() -> Case:
    """Using mismatching base for request type is invalid.

    Using subslass of ListResourcesRequest for list-accounts method is
    obviously invalid.
    """

    def capability(
        request: CustomListAccountsRequestFromBadBase,
    ) -> ListAccountsResponse:
        raise NotImplementedError

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    return capability_name, capability  # type: ignore


@pytest_cases.case(tags=("invalid",))
def case_invalid_capability_bad_request_base() -> Case:
    """Using class unrelated to request type is invalid.

    Using classes unrelated to ``RequestData`` is obviously invalid.
    """

    def capability(request: int) -> ListAccountsResponse:  # type: ignore[type-var]
        raise NotImplementedError

    capability_name = StandardCapabilityName.LIST_ACCOUNTS
    return capability_name, capability  # type: ignore
