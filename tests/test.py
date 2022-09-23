import pytest

@pytest.mark.usefixtures('test_setup_android')
class TestLink:

    def test_1(self):
        el1 = self.driver.find_element_by_id("com.lambdatest.proverbial:id/color")
        el1.click()
        
    def test_2(self):
        el2 = self.driver.find_element_by_id("com.lambdatest.proverbial:id/colour")
        el2.click()
    



