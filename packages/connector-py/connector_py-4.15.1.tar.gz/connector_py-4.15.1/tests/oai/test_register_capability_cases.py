"""Test cases for ``Integration.info`` function."""

import typing as t

from connector.generated import (
    AccountStatus,
    BasicCredential,
    CreateAccountRequest,
    CreateAccountResponse,
    CreatedAccount,
    ListAccountsRequest,
    ListAccountsResponse,
    StandardCapabilityName,
)
from connector.oai.capability import CapabilityCallableProto
from connector.oai.integration import (
    DescriptionData,
    Integration,
    InvalidCapabilityNameError,
    ReservedCapabilityNameError,
)

from .shared_types import (
    AccioRequestObject,
    AccioResponse,
    AccioResponseObject,
)

Case: t.TypeAlias = tuple[
    str,
    dict[str, CapabilityCallableProto[t.Any]],
]


def new_integration() -> Integration:
    return Integration(
        app_id="test",
        version="0.1.0",
        auth=BasicCredential,
        exception_handlers=[],
        handle_errors=True,
        description_data=DescriptionData(
            user_friendly_name="testing thing",
            categories=[],
        ),
    )


def case_register_capability_success() -> Case:
    integration = new_integration()
    capability_name = StandardCapabilityName.LIST_ACCOUNTS

    @integration.register_capability(capability_name)
    async def capability(
        args: ListAccountsRequest,
    ) -> ListAccountsResponse:
        return ListAccountsResponse(
            response=[],
            raw_data=None,
        )

    return capability_name.value, integration.capabilities


def case_register_capability_with_metadata_success() -> Case:
    integration = new_integration()
    capability_name = StandardCapabilityName.CREATE_ACCOUNT

    @integration.register_capability(
        capability_name,
        display_name="Invite User via Email",
        description="Send an email to invite a user to your organization",
    )
    async def capability(
        args: CreateAccountRequest,
    ) -> CreateAccountResponse:
        return CreateAccountResponse(
            response=CreatedAccount(
                status=AccountStatus.ACTIVE,
                created=True,
            ),
            raw_data=None,
        )

    return capability_name.value, integration.capabilities


def case_register_custom_capability_success() -> Case:
    integration = new_integration()
    capability_name = "accio"

    @integration.register_custom_capability(
        capability_name,
        description="A summoning charm.",
    )
    async def custom_capability(
        args: AccioRequestObject,
    ) -> AccioResponseObject:
        return AccioResponseObject(
            response=AccioResponse(success=True),
        )

    return capability_name, integration.capabilities


def case_register_custom_capability_reserved_name() -> Case:
    integration = new_integration()
    capability_name = "list_accounts"

    try:

        @integration.register_custom_capability(
            capability_name,
            description="A summoning charm.",
        )
        async def custom_capability(
            args: AccioRequestObject,
        ) -> AccioResponseObject:
            return AccioResponseObject(
                response=AccioResponse(success=True),
            )
    except Exception as e:
        assert isinstance(e, ReservedCapabilityNameError)
    else:
        raise Exception("Test failed to raise exception")

    return capability_name, integration.capabilities


def case_register_custom_capability_numeric_name() -> Case:
    integration = new_integration()
    capability_name = "name_with_numb3rs"

    try:

        @integration.register_custom_capability(
            capability_name,
            description="A summoning charm.",
        )
        async def custom_capability(
            args: AccioRequestObject,
        ) -> AccioResponseObject:
            return AccioResponseObject(
                response=AccioResponse(success=True),
            )
    except Exception as e:
        assert isinstance(e, InvalidCapabilityNameError)
        assert "Capability names must only contain alphabetic characters and underscores" in str(e)
    else:
        raise Exception("Test failed to raise exception")

    return capability_name, integration.capabilities


def case_register_custom_capability_camel_case() -> Case:
    integration = new_integration()
    capability_name = "CamelCaseName"

    try:

        @integration.register_custom_capability(
            capability_name,
            description="A summoning charm.",
        )
        async def custom_capability(
            args: AccioRequestObject,
        ) -> AccioResponseObject:
            return AccioResponseObject(
                response=AccioResponse(success=True),
            )
    except Exception as e:
        assert isinstance(e, InvalidCapabilityNameError)
        assert "Capability names must use snake casing" in str(e)
    else:
        raise Exception("Test failed to raise exception")

    return capability_name, integration.capabilities
