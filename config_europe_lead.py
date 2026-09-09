HEADERS = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36",
    "Accept-Encoding" : "gzip, deflate",
    "Accept-Language" : "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7"} 

SELECTORS_FIRST_PAGE= {
    "details" : ("div", "listing-details"),
    "name" : ("div", "wpbdp-field-business_name"),
    "location" : ("div", "wpbdp-field-based_in"),
    "tag" : ("div", "wpbdp-field-tags"),
    "year" : ("div", "wpbdp-field-founded"),
    "link" : ("div", "a"),
    "link_second" : "href",
    "description" : ("div", "wpbdp-field-business_description"),
    "second_tag" : ("div", "value"),
    "funding": ("div", "wpbdp-field-total_funding")
}

COUNTRIES = {"austria": "austrian-startups", "belgium": "belgian-startups", "bulgaria": "bulgarian-startups", 
        "croatia":"croatian-startups", "cyprus": "cyprus-startups", "czechia": "czech-rep-startups", 
        "denmark": "danish-startups", "estonia": "estonian-startups", "finland": "finnish-startups",
        "france": "french-startups", "germany": "german-startups", "greece": "greek-startups",
        "hungary": "hungarian-startups", "ireland": "irish-startups", "italy": "italian-startups",
        "latvia": "latvian-startups", "lithuania": "lithuanian-startups", "luxembourg": "luxembourg-based-startups",
        "malta": "maltese-startups", "netherlands": "dutch-startups", "norway": "norwegian-startups",
        "poland": "polish-startups", "portugal": "portuguese-startups", "romania": "romanian-startups",
        "slovenia": "slovenian-startups", "slovakia":"slovakia", "spain": "spanish-startups", "sweden": "swedish-startups", 
        "switzerland":"Switzerland", "uk": "british-startups"}

TIMEOUT = (3, 10)

SLEEP_TIME = 2