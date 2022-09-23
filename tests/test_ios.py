import pytest
from ios import test_setup_ios

@pytest.mark.usefixtures('test_setup_ios')
class TestLink:

    def test_1(self):
        el1 = self.driver.find_element_by_id("color")
        el1.click()
        
    def test_2(self):
        el2 = self.driver.find_element_by_id("colour")
        el2.click()