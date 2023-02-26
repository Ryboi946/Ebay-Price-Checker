#Importing necessary packages
from ast import Lambda
from ctypes import sizeof
from tokenize import Double
from dotenv import load_dotenv
import os
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
import text
import streamlit as st
import time




#Getting environmental variables from .env
load_dotenv()
API_Key = "RyanCurr-EPN-PRD-2ee6b197e-a4f41278"
user = "alert.notification10@gmail.com"
password = "getdpenbwpockapk"


#Ebay Price Checker - actual class that communicates with the Ebay API to get products/prices
class Ebay_Reciever (object):
    #Constructor(initalizing class variables)
    def __init__(self, API_Key, searchTerm, lowRange, highRange):
        self.API_Key = API_Key
        self.searchTerm = searchTerm
        self.lowRange = lowRange
        self.highRange = highRange
        self.current_price = 0
        self.list = dict()
        self.URL_List = dict()
        self.price_list = dict()
       
    #This function takes the list of products mapped to prices, and sorts them by price(lowest to highest)
    #Then returns the lowest priced product
    def parse(self):
        
        self.price_list = sorted(self.list.items(), key = lambda p: p[1])
        Lowest_price = self.price_list[0]
        
        return Lowest_price
    
    #This function returns the url that is associated with the lowest priced product
    def parseURL(self):
        #Before you continue, you need to get a better understanding of python dictionaries
        URL = self.URL_List[self.price_list[0][0]]
        return URL
        
        
        
        
    #This function connects with Ebay API, and feteches products based on searchterm, and price range
    def fetch(self):
        #Establishing a connection between python script and Ebay servers
        try:
            api = Connection(appid=self.API_Key, config_file=None)
            response = api.execute('findItemsAdvanced', {'keywords': self.searchTerm}, {'ItemFilter'})
            for item in response.reply.searchResult.item:
                current_itemPrice = float(item.sellingStatus.currentPrice.value)
                if current_itemPrice > self.lowRange:
                    if current_itemPrice < self.highRange:
                       self.list[item.title] = current_itemPrice
                       self.URL_List[item.title] = item.get('viewItemURL')

                
        except ConnectionError as e:
            print(e)
            print(e.response.dict())

    

    
        
        
        



    # main driver
if __name__=='__main__':
    #streamlit configuration
    st.set_page_config(page_title='Ebay_Price_Checker', page_icon=":smile:", layout="wide")
    st.subheader("Hello!")
    
    searchTerm = st.text_input("What is the name of the product that you would like to track?", key=None)
    
    lowerRange = st.number_input("What is the lower range of your price point?", min_value=0, key=None)
    
    highRange = st.number_input("What is the higher range of your price point?", min_value=0, key=None)

    Phone_number = st.text_input("What is your phone number?", key=None)

    Provider = st.selectbox("What is your phone provider?", ("Select an option", "AT&T", "Verizon", "T-Mobile", "Sprint"))
    
    #Gives program the proper adress for provider
    Provider_text = ""

    if(Provider == 'AT&T'):
        Provider_text = '@txt.att.net'
    elif(Provider == 'Verizon'):
        Provider_text = '@vtext.com'
    elif(Provider == 'T-Mobile'):
        Provider_text = '@tmomail.net'
    elif(Provider == 'Sprint'):
        Provider_text= '@messaging.sprintpcs.com'

    #Allows user to select how many times they would like the program to check eBay and send them a text
    NumberofNoifications = st.number_input("How many times would you like to be notified today?", min_value=0, max_value=3, key=None)
    #Allows user to select a time interval in betweem texts
    TimeInterval = st.selectbox("How long between notifications do you want us to wait before notifying you?", ("1 Hour", "2 Hours", "3 Hours", "4 Hours", "5 Hours"))

    if(TimeInterval == "1 Hour"):
        TimeInterval = 3600
    elif(TimeInterval == "2 Hours"):
        TimeInterval = 7200
    elif(TimeInterval == "3 Hours"):
        TimeInterval = 10800
    elif(TimeInterval == "4 Hours"):
        TimeInterval = 14400
    else:
        TimeInterval = 18000  

    #If all input boxes have been filled, the portion of code that connects with the eBay API will be run
    if(len(searchTerm) != 0 and highRange != 0 and len(Phone_number) != 0 and len(Provider_text) != 0 and len(TimeInterval) != 0):
        
        
        #Initializes class that connects to eBay API
        lowrange =float(lowerRange)
        hrange = float(highRange)
        e = Ebay_Reciever(API_Key, searchTerm, lowrange, hrange)
        #for loop that will run how ever many times the user wished to be conntacted, and will wait the specified time interval amount before contacting them again
        for i in range(NumberofNoifications):
            e.fetch()
            Found = str(e.parse())
            Link = str(e.parseURL())

            text.text_alert("We found a product in your price range!", Found + " URL: " + Link, Phone_number+Provider_text, user, password)
            time.sleep(TimeInterval)
        
        
    
    

