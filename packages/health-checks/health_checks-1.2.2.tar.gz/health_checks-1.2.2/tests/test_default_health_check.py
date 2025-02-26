from __future__ import annotations
import asyncio
import pathlib
import typing
from unittest import mock
from unittest.mock import patch

import fastapi
import litestar
import pytest

from health_checks.fastapi_healthcheck import build_fastapi_health_check_router
from health_checks.litestar_healthcheck import build_litestar_health_check_router


if typing.TYPE_CHECKING:
    from httpx import AsyncClient

    from health_checks import base, file_based, http_based


pytestmark = [pytest.mark.anyio]


async def test_default_http_health_check(http_default_health_check: http_based.DefaultHTTPHealthCheck) -> None:
    assert await http_default_health_check.update_health_status()
    assert (await http_default_health_check.check_health())["health_status"]


@pytest.mark.xdist_group(name="file-based")
async def test_default_file_health_check_startup_and_shutdown(
    default_file_health_check: file_based.DefaultFileHealthCheck,
) -> None:
    await default_file_health_check.startup()
    base_folder_path: typing.Final = pathlib.Path(default_file_health_check.base_folder)
    assert base_folder_path.exists()
    assert default_file_health_check.health_check_file_path.is_file()

    await default_file_health_check.shutdown()
    assert not default_file_health_check.health_check_file_path.is_file()


@pytest.mark.xdist_group(name="file-based")
async def test_default_file_health_check_time_period(
    default_file_health_check: file_based.DefaultFileHealthCheck,
) -> None:
    await default_file_health_check.startup()
    assert await default_file_health_check.update_health_status()
    assert not await default_file_health_check.update_health_status()
    await default_file_health_check.shutdown()


@pytest.mark.xdist_group(name="file-based")
async def test_default_file_health_check(
    short_lived_default_file_health_check: file_based.DefaultFileHealthCheck,
    short_live_time: int,
) -> None:
    # Perform an update, check everything is alright
    await short_lived_default_file_health_check.update_health_status()
    await short_lived_default_file_health_check.check_health()

    # Wait designated time for threshold crossing
    await asyncio.sleep(short_live_time + 1)
    health_check_data: typing.Final = await short_lived_default_file_health_check.check_health()
    assert not health_check_data["health_status"]

    await short_lived_default_file_health_check.shutdown()


async def test_litestar_healthcheck(
    litestar_client: AsyncClient,
    health_check_endpoint: str,
    expected_response: base.HealthCheckTypedDict,
    failed_response: base.HealthCheckTypedDict,
) -> None:
    """Check that default healthcheck works correctly with litestar."""
    assert (await litestar_client.get(health_check_endpoint)).json() == expected_response

    with patch(
        "health_checks.http_based.DefaultHTTPHealthCheck.check_health",
        return_value=failed_response,
    ):
        assert (
            await litestar_client.get(health_check_endpoint)
        ).status_code == litestar.status_codes.HTTP_500_INTERNAL_SERVER_ERROR


async def test_fastapi_healthcheck(
    fastapi_client: AsyncClient,
    health_check_endpoint: str,
    expected_response: base.HealthCheckTypedDict,
    failed_response: base.HealthCheckTypedDict,
) -> None:
    """Check that default healthcheck works correctly with FastAPI."""
    assert (await fastapi_client.get(health_check_endpoint)).json() == expected_response

    with patch(
        "health_checks.http_based.DefaultHTTPHealthCheck.check_health",
        return_value=failed_response,
    ):
        assert (
            await fastapi_client.get(health_check_endpoint)
        ).status_code == fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.parametrize("include_in_schema", [True, False])
def test_litestar_include_in_schema(include_in_schema: bool) -> None:
    health_check_router: typing.Final = build_litestar_health_check_router(
        health_check=mock.Mock(), include_in_schema=include_in_schema
    )
    application: typing.Final = litestar.Litestar(route_handlers=[health_check_router])

    assert bool(application.openapi_schema.paths) is include_in_schema


@pytest.mark.parametrize("include_in_schema", [True, False])
def test_fastapi_include_in_schema(include_in_schema: bool) -> None:
    health_check_router = build_fastapi_health_check_router(
        health_check=mock.Mock(), include_in_schema=include_in_schema
    )
    application: typing.Final = fastapi.FastAPI()
    application.include_router(health_check_router)

    assert bool(application.openapi()["paths"]) is include_in_schema
