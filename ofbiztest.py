from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
import random
import time

class OfbizTest:

    def __init__(self):
        self.display = Display(visible=0, size=(1200, 800))
        self.display.start()
        
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--proxy-server=127.0.0.1:3128')
        
        self.chPATH = '/opt/chrome-driver/chromedriver_linux64/chromedriver'
        self.driver = webdriver.Chrome(executable_path=self.chPATH, chrome_options=self.options)
        self.driver.implicitly_wait(10)

        self.logfile = 'ofbiztest.log'
        self.log = open(self.logfile, "w")

        self.waitingMin = 2
        self.waitingMax = 5

    def reset(self):
        self.driver = webdriver.Chrome(executable_path=self.chPATH, chrome_options=self.options)
        self.__log("reset", "Reset chrome driver")
        time.sleep(self.__getWaiting())
        
    def __getLink(self, text):
        return self.driver.find_element_by_link_text(text)

    def __getById(self, id):
        return self.driver.find_element_by_id(id)

    def __getByName(self, name):
        return self.driver.find_element_by_name(name)

    def __getByXPath(self, path):
        return self.driver.find_element_by_xpath(path)

    def __getWaiting(self):
        return random.choice(range(self.waitingMin, self.waitingMax + 1))

    def __log(self, method, message):
        self.log.write(time.asctime())
        self.log.write(" ")
        self.log.write("method: " + method)
        self.log.write(", ")
        self.log.write("message: " + message.encode('utf-8', errors='ignore'))
        self.log.write("\n")

    def go(self, url="https://172.25.12.14", pageTitle="OT AIOps eCommerce Store"):
        self.driver.get(url)
        self.__log("go", self.driver.title)
        time.sleep(self.__getWaiting())
        
    def createAccount(self, credentials):
        registerBtn = self.__getById("header-bar-register")
        registerBtn.click()
        time.sleep(self.__getWaiting())

        first = self.__getById("USER_FIRST_NAME")
        last = self.__getById("USER_LAST_NAME")
        address = self.__getById("CUSTOMER_ADDRESS1")
        city = self.__getById("CUSTOMER_CITY")
        postal = self.__getById("CUSTOMER_POSTAL_CODE")
        email = self.__getById("CUSTOMER_EMAIL")
        user = self.__getById("USERNAME")
        passwd = self.__getById("PASSWORD")
        confirm = self.__getById("CONFIRM_PASSWORD")

        inputs = (first, last, address, city, postal, email, user, passwd, confirm)

        for (input, credential) in zip(inputs, credentials):
            input.send_keys(credential)

        saveLink = self.__getLink("Save")
        saveLink.click()
        time.sleep(self.__getWaiting())

        userWelcome = self.__getById("welcome-message").get_property("innerText")
        self.__log("createAccount", userWelcome)

    def login(self, credentials, mainTitle="OT AIOps eCommerce Store"):
        loginBtn = self.__getById("header-bar-login")
        loginBtn.click()
        time.sleep(self.__getWaiting())
        #assert "Login" in self.driver.title
        (user, password, userName) = credentials
        (userInput, passwdInput) = (self.__getById("userName"), self.__getById("password"))
        userInput.send_keys(user)
        passwdInput.send_keys(password)
        loginForm = self.__getByName("loginform")
        time.sleep(self.__getWaiting())
        loginForm.submit()
        time.sleep(self.__getWaiting())

        #self.__getById("header-bar-main").click()
        userWelcome = self.__getById("welcome-message").get_property("innerText")
        self.__log("login", userWelcome)
        

    def searchAll(self, searchTitle="Search Results"):
        searchForm = self.__getById("keywordsearchbox_keywordsearchform")
        searchForm.submit()
        self.__log("searchAll", self.driver.title)
        time.sleep(self.__getWaiting())
        
    
    def searchByKeyword(self, keyword, searchTitle="Search Results"):
        searchInput = self.__getByName("SEARCH_STRING")
        searchInput.send_keys(keyword)
        self.__log("searchByKeyword", "Search by keyword " + keyword)
        self.searchAll()
       

    def viewProduct(self, keyword):
        productName = "OT." + keyword.upper()
        pLink = self.__getByXPath("//div[@class='productinfo']/div/a[@class='linktext']")
        pLink.click()
        self.__log("viewProduct", "Looking at product " + productName)
        time.sleep(self.__getWaiting())

    def viewRandomProduct(self):
        productId = random.choice(range(4)) + 1
        pDiv = "//div[@class='productsummary-container']/div[" + str(productId) + "]"
        pLink = self.__getByXPath(pDiv + "/div/div/a[@class='linktext']")
        pLink.click()
        productName = ["asum", "bpm", "rca", "platform"][productId-1]
        self.__log("viewRandomProduct", "Looking at product " + productName)
        time.sleep(self.__getWaiting())

    def addToCartFromView(self):
        addForm = self.__getByName("addform")
        addForm.submit()
        self.__log("addToCartFromView", self.driver.title)
        time.sleep(self.__getWaiting())

    def addToCart(self, pNumber, cartTitle="OT AIOps eCommerce Store"):
        addToCartForm = self.__getByName("the" + str(pNumber) + "form")
        addToCartForm.submit()
        self.__log("addToCart", self.driver.title)
        time.sleep(self.__getWaiting())
        

    def addRandomToCart(self, pCount=4):
        selectedProduct = random.choice(range(pCount))
        self.addToCart(pNumber=selectedProduct)
        productName = ["asum", "bpm", "rca", "platform"][selectedProduct]
        self.__log("addRandomToCart", productName)
        time.sleep(self.__getWaiting())
        

    def viewCart(self, cartTitle="Shopping Cart"):
        cartView = self.__getLink("[View Cart]")
        cartView.click()
        self.__log("viewCart", self.driver.title)
        time.sleep(self.__getWaiting())
        

    def doQuickCheckout(self, result="continue"):
        
        quickCheckoutView = self.__getLink("[Quick Checkout]")
        quickCheckoutView.click()

        toBtn = self.__getByName("shipping_contact_mech_id")
        toBtn.click()
        time.sleep(self.__getWaiting())

        shippingMethod = self.__getByXPath("//input[@name='shipping_method'][@value='NO_SHIPPING@_NA_']")
        shippingMethod.click()
        time.sleep(self.__getWaiting())

        paymentMethod = self.__getByXPath("//input[@name='checkOutPaymentId'][@value='EXT_COD']")
        paymentMethod.click()
        time.sleep(self.__getWaiting())

        continueLink = self.__getLink("Continue to Final Order Review")
        backLink = self.__getLink("Continue to Final Order Review")
        
        if result=="back":
            backLink.click()
            time.sleep(self.__getWaiting())
            return
        
        continueLink.click()
        time.sleep(self.__getWaiting())
        orderForm = self.__getByName("orderreview")
        orderForm.submit()
        self.__log("doQuickCheckout", self.driver.title)
        time.sleep(self.__getWaiting())
        

    def buyProducts(self, pKeywords, buyCount=1): 
        for loop in range(buyCount):
            addChoice = random.choice([0, 1])
            keyword = random.choice([random.choice(pKeywords), ""])
            pcount = len(pKeywords) if (keyword=="") else 1
            self.searchByKeyword(keyword)
            if addChoice==0:
                self.addRandomToCart(pcount)
            else:
                if pcount==1:
                    self.viewProduct(keyword)
                else:
                    self.viewRandomProduct()
                self.addToCartFromView()
        self.viewCart()
        self.doQuickCheckout()
        self.__log("buyProducts", "Loop count = " + str(buyCount))
        

    def finish(self):
        self.__log("finish",  "Closing self.driver")
        self.log.close()
        self.driver.close()
        