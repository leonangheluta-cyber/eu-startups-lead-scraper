import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import logging
from config_europe_lead import  HEADERS, SELECTORS_FIRST_PAGE, TIMEOUT, SLEEP_TIME, COUNTRIES
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    filename="script_european_companies.log")
headers=HEADERS 
session=requests.Session()
second_tag, second_class = SELECTORS_FIRST_PAGE["second_tag"]
def helper(data, tag, class_name, log_tag, article):
    try:
        result=data.find(tag, class_=class_name).text.strip()
    except AttributeError:
        result=None
        if article is None:
            logging.warning(f"{log_tag} not found")
        else:
            logging.warning(f"{log_tag} not found for {article} ")
    return result

def normalize_link(link):
    link_ok=link.lower()
    link_ok_2=link_ok.replace("http://", "").replace("https://", "").replace("www.", "")
    link_ok_3=link_ok_2.rstrip("/")
    return link_ok_3

def access_request_find_data():
    tg, clas = SELECTORS_FIRST_PAGE["details"]
    ntg, nclass = SELECTORS_FIRST_PAGE["name"]
    ltg, lclass = SELECTORS_FIRST_PAGE["location"]
    ttg, tclass = SELECTORS_FIRST_PAGE["tag"]
    ytg, yclass = SELECTORS_FIRST_PAGE["year"]
    link_tag, link_tag_2 = SELECTORS_FIRST_PAGE["link"]
    link_class = SELECTORS_FIRST_PAGE["link_second"]
    count=0
    companies=[]
    attempts=0
    link_seen=set()
    while True:
        c=input("Enter the country name in english: ").lower()
        if c in COUNTRIES:
            break
    country=COUNTRIES[c]
    while True:
        try:
            quantity=int(input("Enter the number of companies you want to download: "))
            if quantity<=0:
                print("Please enter a number:")
            else:
                break
        except ValueError:
                print("Please enter a number:" )
    while True:
        count+=1
        url=f"https://www.eu-startups.com/directory/wpbdp_category/{country}/page/{count}/"
        if len(companies)>=quantity:
            break
        time.sleep(SLEEP_TIME)
        try:
            access_request=session.get(url, headers=headers, timeout=(TIMEOUT))
            status=access_request.status_code
            if status==404:
                break
            access_request.raise_for_status()
        except requests.exceptions.RequestException as error:
            logging.error(f"Error: {error}")
            attempts+=1
            count-=1
            if attempts==3:
                count+=1
                attempts=0
            continue
        attempts=0
                
        access_request.encoding="utf-8"
        page=BeautifulSoup(access_request.text, "html.parser")
        title=page.find_all(tg, class_=clas)
        if not title:
            break
        for data in title:
            n=data.find(ntg, class_=nclass)
            name=helper(n, second_tag, second_class, "Name", None)
            loc=data.find(ltg, class_=lclass)
            base=helper(loc, second_tag, second_class, "Based in", name)    
            tag=data.find(ttg, class_=tclass)
            tags=helper(tag, second_tag, second_class, "Tag", name)
            y=data.find(ytg, class_=yclass)
            year=helper(y, second_tag, second_class, "Year", name)
            try:
                l=n.find(link_tag).find(link_tag_2)
                link=l[link_class]
            except (AttributeError, TypeError, KeyError):
                link=None
                logging.warning(f"Link not found for {name}")
            try:
                link_ok=normalize_link(link)
            except AttributeError:
                link_ok=None
            if link_ok and link_ok in link_seen:
                continue
            if link_ok:
                link_seen.add(link_ok)
            companies.append({"Name": name, "Based in": base, "Foundation year": year, "Funding": None, "Description": None, "Tags": tags, "Direct link": link})
    return companies, country, quantity

def find_data(companies, country):
    ddesc, dclass = SELECTORS_FIRST_PAGE ["description"]
    tfund, tclass =SELECTORS_FIRST_PAGE["funding"]
    n=0
    for info in companies:
        time.sleep(SLEEP_TIME)
        n+=1
        link=info["Direct link"]
        if not link:
            logging.warning(f"Link not found for {info['Name']}")
            continue
        try:
            access_request=session.get(link, headers=headers, timeout=(TIMEOUT))
            access_request.raise_for_status()
        except requests.exceptions.RequestException as error:
            logging.error(f"Error: {error}")
            continue
        access_request.encoding="utf-8"
        page=BeautifulSoup(access_request.text, "html.parser")
        fund=page.find(tfund, class_=tclass) 
        funding=helper(fund, second_tag, second_class, "Funding", info['Name'])
        desc=page.find(ddesc, class_=dclass)
        desc2=helper(desc, second_tag, second_class, "Description", info['Name'])
        description=desc2.replace("\"", "") if desc2 else None
        info["Description"]=description
        info["Funding"]=funding
        if n%10==0:
            save_file(companies, country)    
    return companies

def save_file(data, country):
    conv=pd.DataFrame(data)
    try:
        conv.to_excel(f"Lead_{country}_companies.xlsx", index=False)
    except PermissionError:
        logging.warning("Attention: file open")
        print("Failed to save due to an open file during the records download")
    
if __name__=="__main__":
    companies, country, quantity=access_request_find_data()
    companies_limit=companies[:quantity]
    data=find_data(companies_limit, country)
    session.close()
    save_file(data, country)

