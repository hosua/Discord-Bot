from selenium import webdriver
from datetime import datetime
import time




def scrape(item, num_items):
    
    driver = webdriver.Chrome()
    ebay_home = "https://www.ebay.com/"
    driver.get(ebay_home)
    textBox = driver.find_element_by_id("gh-ac")

    textBox.send_keys(item + "\n")
    
    #now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    item_dict = {}

    rtn = "============================================================\n"

    def get_items():
        return driver.find_elements_by_class_name("s-item__info")

    def get_dict():
        for i in range(1):
            items = get_items()
            #rtn += "==================Page " + str(i+1) + "===================="
            try:
                next_page = driver.find_element_by_class_name("pagination__next") # f'`{url}`
            except:
                print("END OF PAGE!\n")
                #rtn += "Could not find next page! Finishing...\n"
            for j in range(len(items)):
                try:
                    link = items[j].find_element_by_class_name("s-item__link").get_attribute("href")
                    title = items[j].find_element_by_class_name("s-item__title").text.replace("NEW LISTING", "")
                    details = items[j].find_element_by_class_name("s-item__details")
                    detail = details.find_element_by_class_name("s-item__detail")
                    price = detail.find_element_by_class_name("s-item__price").text
                    item_dict[title] = {"price": price, "link": link}
                    #rtn += str(k-1) + ". " + price + " - " + title + "\n"
                    #rtn += link + "\n"
                except:
                    pass
                #rtn += "============================================================\n"
            try:
                next_page.click()
            except: # It kinda seems dumb to do it this way but this throws weird errors.
                break
        #print(item_dict)
        return item_dict
    item_dict = get_dict()
    #print(item_dict)
    return item_dict
    """
    i = 0
    rtn = "Your ebay results:\n\n"
    rtn += "============================================================\n"
    for item in item_dict:
        
        i += 1
        rtn += str(i) + ". " + item_dict[item]["price"] + " - " + item + "\n"
        rtn += item_dict[item]["link"] + "\n"
        rtn += "============================================================\n"
        if i == num_items:
            break
    
    return rtn
    """


#print(scrape("table", 5))
