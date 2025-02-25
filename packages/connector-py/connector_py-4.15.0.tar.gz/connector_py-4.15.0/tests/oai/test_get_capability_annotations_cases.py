"""Test cases for ``get_capability_annotations`` function."""

import typing as t

import pytest_cases
from connector.generated import (
    ValidateCredentialsRequest,
    ValidateCredentialsResponse,
    ValidatedCredentials,
)
from connector.oai.capability import CapabilityCallableProto, Request, Response

Case: t.TypeAlias = tuple[
    CapabilityCallableProto[t.Any],
    tuple[type[Request], type[Response]],
]


@pytest_cases.case(tags=("correct",))
def case_correct_capability() -> Case:
    def capability(
        args: ValidateCredentialsRequest,
    ) -> ValidateCredentialsResponse:
        return ValidateCredentialsResponse(
            response=ValidatedCredentials(valid=True, unique_tenant_id="testing-unique-tenant-id"),
            raw_data=None,
        )

    expected_annotations = (
        ValidateCredentialsRequest,
        ValidateCredentialsResponse,
    )
    return capability, expected_annotations


@pytest_cases.case(tags=("missing_annotation",))
def case_missing_argument_annotation() -> CapabilityCallableProto[t.Any]:
    def capability(args) -> ValidateCredentialsResponse:
        return ValidateCredentialsResponse(
            response=ValidatedCredentials(valid=True, unique_tenant_id="testing-unique-tenant-id"),
            raw_data=None,
        )

    return capability  # type: ignore[return-value]


@pytest_cases.case(tags=("missing_annotation",))
def case_missing_return_annotation() -> CapabilityCallableProto[t.Any]:
    def capability(args: ValidateCredentialsRequest):
        return ValidateCredentialsResponse(
            response=ValidatedCredentials(valid=True, unique_tenant_id="testing-unique-tenant-id"),
            raw_data=None,
        )

    return capability  # type: ignore[return-value]


@pytest_cases.case(tags=("missing_annotation",))
def case_missing_annotations() -> CapabilityCallableProto[t.Any]:
    def capability(args):
        return ValidateCredentialsResponse(
            response=ValidatedCredentials(valid=True, unique_tenant_id="testing-unique-tenant-id"),
            raw_data=None,
        )

    return capability  # type: ignore[return-value]
