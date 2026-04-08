from os import environ
import pytest
from appium import webdriver
from appium.options.common import AppiumOptions

def finalize_driver(request, driver):
    def fin():
        if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
            driver.execute_script('lambda-status=failed')
        else:
            driver.execute_script('lambda-status=passed')
        driver.quit()
    request.addfinalizer(fin)

@pytest.fixture(scope='function')
def test_setup_android(request):
    username = environ.get('LT_USERNAME')
    access_key = environ.get('LT_ACCESS_KEY')
    
    if not username or not access_key:
        raise ValueError("LT_USERNAME or LT_ACCESS_KEY environment variables are not set!")

    caps = {
        "lt:options": {
		"w3c": True,
		"platformName": "Android",
		"deviceName": "Galaxy.*",
		"platformVersion": "11",
		"isRealMobile": True,
        "app":"lt://proverbial-android",   #Enter the app (.apk) url here
        "build":"Android Pytest"
	}
    }

    driver = webdriver.Remote("https://<username>:<accessKey>@mobile-hub.lambdatest.com/wd/hub",
            options=AppiumOptions().load_capabilities(caps))
    request.cls.driver = driver
    yield driver
    finalize_driver(request, driver)

@pytest.fixture(scope='function')
def test_setup_ios(request):
    username = environ.get('LT_USERNAME')
    access_key = environ.get('LT_ACCESS_KEY')

    if not username or not access_key:
        raise ValueError("LT_USERNAME or LT_ACCESS_KEY environment variables are not set!")

    caps = {
        "lt:options": {
		"w3c": True,
		"platformName": "iOS",
		"deviceName": "iPhone.*",
		"platformVersion": "14",
		"isRealMobile": True,
        "app":"lt://proverbial-iOS",   #Enter the app (.ipa) url here
        "build":"iOS Pytest"
	}
    }

    remote_url = f"https://{username}:{access_key}@mobile-hub.lambdatest.com/wd/hub"
    driver = webdriver.Remote(remote_url, options=AppiumOptions().load_capabilities(caps))
    request.cls.driver = driver
    yield driver
    finalize_driver(request, driver)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
