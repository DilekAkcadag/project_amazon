import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class Locators(object):
    AMAZON_ARAMA_KUTUSU = (By.ID, "twotabsearchtextbox")
    HOME_PAGE_CEREZ = (By.ID, "sp-cc-accept")
    IKINCI_SAYFA_ICON = (By.XPATH, "(//*[text()='2'])[3]")
    URUN_SAYFASINDA_TEST = (By.LINK_TEXT, "Sonuçlara dön")
    SEPETE_EKLE = (By.CSS_SELECTOR, "#add-to-cart-button")
    SEPETTE_MIYIM = (By.NAME, "proceedToRetailCheckout")
    SEPETE_GIT = (By.XPATH, "//*[@id='sw-gtc']")
    ANASAYFAYA_DONUS = (By.ID, "nav-logo-sprites")

class AmazonTest(unittest.TestCase):
    base_url = 'http://www.amazon.com.tr'

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.implicitly_wait(10)

    def test_amazon_urun_ekleme(self):

        # 1. http://www.amazon.com sitesine gidilecek ve anasayfanın açıldığı assertion ile #onaylatılacak.
        cerez = self.driver.find_element(*Locators.HOME_PAGE_CEREZ)
        cerez.click()
        time.sleep(2)

        assert "Amazon.com" in self.driver.title

        # 2. Ekranin üstündeki Search alanına 'samsung' yazıp arama işlemi gerçekleştirilecek.
        search_box = self.driver.find_element(*Locators.AMAZON_ARAMA_KUTUSU)
        search_box.send_keys("samsung")
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        # 3. Gelen sayfada samsung icin sonuc bulunduğu onaylatılacak.
        assert "samsung" in self.driver.title

        # 4. Sayfanın aşağısına inilip sayfa sayılarından 2. sayfaya tıklanıp ve açılan sayfada 2.
        # #sayfanin şu an gösterimde olduğu onaylatılacak.

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        target_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(Locators.IKINCI_SAYFA_ICON)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", target_element)
        second_page_icon = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(Locators.IKINCI_SAYFA_ICON)
        )
        second_page_icon.click()
        time.sleep(3)

        assert "page=2" in self.driver.current_url

        # 5.Üstten 5. Satır 1. Sütun içerisindeki ürüne tıklanacak.
        target_product = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//*[@*='a-section aok-relative s-image-square-aspect'])[17]"))
        )
        target_product.click()

        # 6. Ürün sayfasında olduğumuz doğrulanacak.
        assert self.driver.find_element(*Locators.URUN_SAYFASINDA_TEST).is_displayed()

        # 7. Ürün sepete eklenir
        add_to_cart_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#add-to-cart-button"))
        )
        add_to_cart_button.click()
        time.sleep(3)


        # 8. Sepete gidilir ve sepet sayfasında olduğumuz doğrulanır
        go_to_cart_button = WebDriverWait(self.driver, 10).until(
         EC.element_to_be_clickable((By.XPATH, "//*[@id='sw-gtc']"))
        )
        go_to_cart_button.click()
        time.sleep(3)

        assert self.driver.find_element(*Locators.SEPETTE_MIYIM).is_displayed()


        # 9. Logo’ya tıklanarak ana sayfaya geri dönüş sağlanır
        amazon_logo = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "nav-logo-sprites"))
        )
        amazon_logo.click()


    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()












