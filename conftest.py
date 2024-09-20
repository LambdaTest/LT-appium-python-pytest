from os import environ
import pytest
from appium import webdriver
from appium.options.common import AppiumOptions

@pytest.fixture(scope='function')
def test_setup_android(request):
    test_name = request.node.name
    build = environ.get('BUILD', "Pytest Android Sample")

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
    
    def fin():
        if request.node.rep_call.failed:
            driver.execute_script('lambda-status=failed')
        else:
            driver.execute_script('lambda-status=passed')
        driver.quit()
    request.addfinalizer(fin)
    
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # this sets the result as a test attribute for LambdaTest reporting.
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)

