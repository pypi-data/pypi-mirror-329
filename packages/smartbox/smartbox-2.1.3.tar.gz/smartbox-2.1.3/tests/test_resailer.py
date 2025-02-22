import pytest

from smartbox import AsyncSmartboxSession, ResailerNotExistError
from smartbox.resailer import AvailableResailers


def test_available_resailers_existing_resailer():
    resailer = AvailableResailers(api_url="api").resailer
    assert resailer.name == "Helki"
    assert resailer.api_url == "api"


def test_available_resailers_non_existing_resailer():
    with pytest.raises(ResailerNotExistError):
        AvailableResailers(api_url="non-existing-api").resailer


def test_available_resailers_custom_resailer():
    serial_id = 99
    _resailer = AvailableResailers(
        api_url="custom-api",
        basic_auth="custom-auth",
        web_url="https://custom-url.com",
        serial_id=serial_id,
        name="Custom",
    )
    resailer = _resailer.resailer
    assert resailer.name == "Custom"
    assert resailer.api_url == "custom-api"
    assert resailer.basic_auth == "custom-auth"
    assert resailer.web_url == "https://custom-url.com"
    assert resailer.serial_id == serial_id

    assert _resailer.name == "Custom"
    assert _resailer.api_url == "custom-api"
    assert _resailer.web_url == "https://custom-url.com"


def test_resailer_invalid_data():
    with pytest.raises(ResailerNotExistError):
        AvailableResailers(
            api_url="invalid-api",
            basic_auth="invalid-auth",
            web_url="invalid-url",
            serial_id="invalid-serial-id",
        ).resailer


@pytest.mark.asyncio
async def test_all_resailers():
    for resailer in AvailableResailers.resailers.values():
        _session = AsyncSmartboxSession(
            username="", password="", api_name=resailer.api_url
        )
        check = await _session.health_check()
        assert check is not None
        version = await _session.api_version()
        assert "major" in version
