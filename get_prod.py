# This script allows to get the information about new version 
# of open source products from vmssoftware.com and download them.

import locators, requests, re, ssl, wget
from bs4 import BeautifulSoup

class UserInput():
    
    def ask_input(self, products):
        """ Ask user to input the product or exit"""
        while True:
            self.user_input = input("Enter the product name or exit: \n\r")
            if "exit" in self.user_input:
                exit()

            self.asked_prod = "/products/" + self.user_input
            match = self.check_user_input(products)

            if match == True:
                break
            else:
                print(self.user_input, " wasn't found in product list.\n\r")

    def check_user_input(self, products):
        """ Check if the product is on the list"""
        match = self.asked_prod in products.prod_list
        return match


class Products():

    def __init__(self):
        self.link = locators.PROD_LIST_LINK

    def get_data(self):
        """ Get the list of available products."""
        self.r = requests.get(self.link)
        self.prod_list = re.findall(locators.PROD_LIST_REQ, self.r.text)

class Product(Products):

    def __init__(self, user):
        self.link = locators.PROD_LINK + user.user_input + "/"

    def get_data(self):
        """ Get the page of the product"""
        self.r = requests.get(self.link)

    def get_version(self, user):
        """ Parse the page and get info about the product version."""
        self.soup = BeautifulSoup(self.r.text, 'html.parser')
        text = self.soup.get_text()
        version = text[text.index(locators.PROD_START) + len(locators.PROD_START):text.index(locators.PROD_END)]

        string = "The latest version of " + user.user_input + " is " + version
        print(string)

    def download_product(self):
        """ Download the specified product."""
        link_list = self.soup.select(locators.PROD_EXE_CSS)

        for lnk in list(link_list):
            res = re.search(locators.PROD_REGEXP, str(lnk))
            if res:
                string = res.group(0)
                a = string.split('"')

                ssl._create_default_https_context = ssl._create_unverified_context
                wget.download(a[0], a[1][1::], bar=None)


        
def ask():
    """ Promote to download the latest version of the product."""
    while True:
        msg = "Would you like to download the product (y|n)?\n\r"
        answer = str(input(msg).strip().lower())
        if answer == 'y' or answer == 'n':
            break
        else:
            continue
    return answer



def main():
    while True:
        user = UserInput()
        products = Products()
        products.get_data()

        user.ask_input(products)
        user.check_user_input(products)

        product = Product(user)
        product.get_data()
        product.get_version(user)

        answer = ask()
        if answer == "y":
            product.download_product()
            print("Product is downloaded.")
            break
        elif answer == "n":
            continue
        


if __name__=="__main__":
    main()
