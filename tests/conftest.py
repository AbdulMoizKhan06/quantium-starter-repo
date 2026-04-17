import os
import pytest
from dash.testing.composite import DashComposite
from dash.testing.application_runners import ThreadedRunner
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """
    Ensure chromedriver is on PATH for dash.testing.
    DashComposite (in this dash-testing version) spawns 'chromedriver' by name.
    """
    driver_path = ChromeDriverManager().install()  
    driver_dir = os.path.dirname(driver_path)


    os.environ["PATH"] = driver_dir + os.pathsep + os.environ.get("PATH", "")


@pytest.hookimpl
def pytest_setup_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,800")
    return options


@pytest.fixture
def dash_duo(request, dash_thread_server, tmp_path_factory):
    """
    Use Dash's normal DashComposite, but now chromedriver is discoverable via PATH.
    """
    download_path = tmp_path_factory.mktemp("download")

    with DashComposite(
        server=ThreadedRunner(),
        browser="chrome",
        headless=True,
        options=pytest_setup_options(),
        download_path=str(download_path),
    ) as dc:
        yield dc