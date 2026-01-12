FEATURE_ORDER = [
    "URLLength",
    "IsDomainIP",
    "URLSimilarityIndex",
    "CharContinuationRate",
    "TLDLegitimateProb",
    "TLDLength",
    "NoOfSubDomain",
    "HasObfuscation",
    "LetterRatioInURL",
    "DegitRatioInURL",
    "NoOfEqualsInURL",
    "NoOfQMarkInURL",
    "NoOfAmpersandInURL",
    "SpacialCharRatioInURL",
    "LargestLineLength",
    "HasTitle",
    "URLTitleMatchScore",
    "HasFavicon",
    "Robots",
    "IsResponsive",
    "NoOfURLRedirect",
    "NoOfSelfRedirect",
    "HasDescription",
    "NoOfPopup",
    "NoOfiFrame",
    "HasExternalFormSubmit",
    "HasSocialNet",
    "HasSubmitButton",
    "HasHiddenFields",
    "HasPasswordField",
    "Bank",
    "Pay",
    "Crypto",
    "HasCopyrightInfo",
    "NoOfEmptyRef",
    "JS_to_CSS_ratio",
    "External_to_Self_ratio",
    "Code_density"
]



# Liste de TLD considérés comme légitimes / très populaires
LEGITIMATE_TLDS = {
    "com": 1.0,
    "org": 0.95,
    "net": 0.9,
    "gov": 1.0,
    "edu": 0.95,
    "mil": 1.0,
    "int": 0.9,
    "co": 0.9,
    "io": 0.85,
    "fr": 0.9,
    "uk": 0.9,
    "de": 0.9,
    "ca": 0.9,
    "au": 0.9,
    "jp": 0.85,
    "es": 0.85,
    "it": 0.85,
    "nl": 0.85,
    "ru": 0.7,
    "cn": 0.7,
    "xyz": 0.3,
    "top": 0.2,
    "club": 0.4,
    "site": 0.4,
    "online": 0.4,
    "info": 0.6,
    "biz": 0.5
    # Tu peux étendre cette liste selon tes besoins
}




# Liste très longue d'URLs légitimes connues pour le calcul de similarité
KNOWN_LEGITIMATE_URLS = [
    # Moteurs de recherche
    "https://www.google.com",
    "https://www.bing.com",
    "https://www.yahoo.com",
    "https://www.duckduckgo.com",
    "https://www.baidu.com",
    "https://www.yandex.com",
    "https://www.ask.com",

    # Réseaux sociaux
    "https://www.facebook.com",
    "https://www.twitter.com",
    "https://www.instagram.com",
    "https://www.linkedin.com",
    "https://www.pinterest.com",
    "https://www.snapchat.com",
    "https://www.tiktok.com",
    "https://www.reddit.com",

    # E-commerce
    "https://www.amazon.com",
    "https://www.ebay.com",
    "https://www.alibaba.com",
    "https://www.etsy.com",
    "https://www.walmart.com",
    "https://www.bestbuy.com",
    "https://www.target.com",

    # Services cloud et tech
    "https://www.microsoft.com",
    "https://www.apple.com",
    "https://www.github.com",
    "https://www.gitlab.com",
    "https://www.dropbox.com",
    "https://www.box.com",
    "https://www.slack.com",
    "https://www.trello.com",
    "https://www.atlassian.com",
    "https://www.cloudflare.com",
    "https://www.spotify.com",
    "https://www.netflix.com",
    "https://www.adobe.com",
    "https://www.salesforce.com",

    # Banques internationales
    "https://www.chase.com",
    "https://www.bankofamerica.com",
    "https://www.citi.com",
    "https://www.hsbc.com",
    "https://www.wellsfargo.com",
    "https://www.barclays.com",
    "https://www.nab.com.au",
    "https://www.rbc.com",
    "https://www.scotiabank.com",

    # Sites gouvernementaux
    "https://www.usa.gov",
    "https://www.gov.uk",
    "https://www.canada.ca",
    "https://www.australia.gov.au",
    "https://www.europe.eu",
    "https://www.senat.fr",
    "https://www.service-public.fr",

    # Médias et informations
    "https://www.bbc.com",
    "https://www.cnn.com",
    "https://www.nytimes.com",
    "https://www.theguardian.com",
    "https://www.reuters.com",
    "https://www.forbes.com",
    "https://www.bloomberg.com",
    "https://www.nbcnews.com",
    "https://www.foxnews.com",

    # Autres services populaires
    "https://www.wikipedia.org",
    "https://www.stackoverflow.com",
    "https://www.quora.com",
    "https://www.medium.com",
    "https://www.imdb.com",
    "https://www.yelp.com",
    "https://www.tripadvisor.com",
    "https://www.khanacademy.org",
    "https://www.coursera.org",
    "https://www.udemy.com",
    "https://www.edx.org",
    
    # Extensions populaires internationales
    "https://www.google.co.uk",
    "https://www.google.ca",
    "https://www.google.fr",
    "https://www.google.de",
    "https://www.google.es",
    "https://www.google.it",
    "https://www.google.com.au",
    "https://www.amazon.co.uk",
    "https://www.amazon.ca",
    "https://www.amazon.de",
    "https://www.amazon.fr",
    "https://www.amazon.it"
]
