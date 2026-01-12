import pandas as pd

# Création directe du DataFrame X_test
X_test = pd.DataFrame([
    # 0. Phishing Crypto
    {
        'IsHTTPS': 0, 'URLLength': 95, 'IsDomainIP': 0, 'URLSimilarityIndex': 45,
        'CharContinuationRate': 0.68, 'TLDLegitimateProb': 0.15, 'TLDLength': 3,
        'NoOfSubDomain': 5, 'HasObfuscation': 1, 'NoOfObfuscatedChar': 12,
        'LetterRatioInURL': 0.72, 'DegitRatioInURL': 0.12, 'NoOfEqualsInURL': 2,
        'NoOfQMarkInURL': 1, 'NoOfAmpersandInURL': 1, 'SpacialCharRatioInURL': 0.16,
        'LargestLineLength': 5200, 'HasTitle': 1, 'DomainTitleMatchScore': 20,
        'URLTitleMatchScore': 18, 'HasFavicon': 0, 'Robots': 0, 'IsResponsive': 0,
        'NoOfURLRedirect': 1, 'NoOfSelfRedirect': 0, 'HasDescription': 0,
        'NoOfPopup': 1, 'NoOfiFrame': 2, 'HasExternalFormSubmit': 1,
        'HasSocialNet': 0, 'HasSubmitButton': 1, 'HasHiddenFields': 1,
        'HasPasswordField': 1, 'Bank': 0, 'Pay': 0, 'Crypto': 1,
        'HasCopyrightInfo': 0, 'NoOfEmptyRef': 15, 'JS_to_CSS_ratio': 6.2,
        'External_to_Self_ratio': 0.88, 'Code_density': 0.92
    },
    
    # 1. Phishing Banking
    {
        'IsHTTPS': 1, 'URLLength': 88, 'IsDomainIP': 0, 'URLSimilarityIndex': 50,
        'CharContinuationRate': 0.55, 'TLDLegitimateProb': 0.20, 'TLDLength': 2,
        'NoOfSubDomain': 6, 'HasObfuscation': 1, 'NoOfObfuscatedChar': 8,
        'LetterRatioInURL': 0.78, 'DegitRatioInURL': 0.10, 'NoOfEqualsInURL': 3,
        'NoOfQMarkInURL': 2, 'NoOfAmpersandInURL': 2, 'SpacialCharRatioInURL': 0.12,
        'LargestLineLength': 3800, 'HasTitle': 1, 'DomainTitleMatchScore': 15,
        'URLTitleMatchScore': 12, 'HasFavicon': 0, 'Robots': 0, 'IsResponsive': 0,
        'NoOfURLRedirect': 1, 'NoOfSelfRedirect': 0, 'HasDescription': 0,
        'NoOfPopup': 2, 'NoOfiFrame': 1, 'HasExternalFormSubmit': 1,
        'HasSocialNet': 0, 'HasSubmitButton': 1, 'HasHiddenFields': 1,
        'HasPasswordField': 1, 'Bank': 1, 'Pay': 1, 'Crypto': 0,
        'HasCopyrightInfo': 0, 'NoOfEmptyRef': 20, 'JS_to_CSS_ratio': 4.5,
        'External_to_Self_ratio': 0.85, 'Code_density': 0.89
    },
    
    # 2. Légitime E-commerce
    {
        'IsHTTPS': 1, 'URLLength': 42, 'IsDomainIP': 0, 'URLSimilarityIndex': 85,
        'CharContinuationRate': 0.18, 'TLDLegitimateProb': 0.48, 'TLDLength': 3,
        'NoOfSubDomain': 2, 'HasObfuscation': 0, 'NoOfObfuscatedChar': 0,
        'LetterRatioInURL': 0.85, 'DegitRatioInURL': 0.05, 'NoOfEqualsInURL': 1,
        'NoOfQMarkInURL': 1, 'NoOfAmpersandInURL': 0, 'SpacialCharRatioInURL': 0.10,
        'LargestLineLength': 1200, 'HasTitle': 1, 'DomainTitleMatchScore': 88,
        'URLTitleMatchScore': 85, 'HasFavicon': 1, 'Robots': 1, 'IsResponsive': 1,
        'NoOfURLRedirect': 0, 'NoOfSelfRedirect': 0, 'HasDescription': 1,
        'NoOfPopup': 0, 'NoOfiFrame': 0, 'HasExternalFormSubmit': 0,
        'HasSocialNet': 1, 'HasSubmitButton': 0, 'HasHiddenFields': 0,
        'HasPasswordField': 0, 'Bank': 0, 'Pay': 1, 'Crypto': 0,
        'HasCopyrightInfo': 1, 'NoOfEmptyRef': 2, 'JS_to_CSS_ratio': 1.2,
        'External_to_Self_ratio': 0.28, 'Code_density': 0.42
    },
    
    # 3. Légitime Corporate
    {
        'IsHTTPS': 1, 'URLLength': 28, 'IsDomainIP': 0, 'URLSimilarityIndex': 95,
        'CharContinuationRate': 0.08, 'TLDLegitimateProb': 0.52, 'TLDLength': 3,
        'NoOfSubDomain': 1, 'HasObfuscation': 0, 'NoOfObfuscatedChar': 0,
        'LetterRatioInURL': 0.90, 'DegitRatioInURL': 0.02, 'NoOfEqualsInURL': 0,
        'NoOfQMarkInURL': 0, 'NoOfAmpersandInURL': 0, 'SpacialCharRatioInURL': 0.08,
        'LargestLineLength': 780, 'HasTitle': 1, 'DomainTitleMatchScore': 95,
        'URLTitleMatchScore': 92, 'HasFavicon': 1, 'Robots': 1, 'IsResponsive': 1,
        'NoOfURLRedirect': 0, 'NoOfSelfRedirect': 0, 'HasDescription': 1,
        'NoOfPopup': 0, 'NoOfiFrame': 0, 'HasExternalFormSubmit': 0,
        'HasSocialNet': 1, 'HasSubmitButton': 0, 'HasHiddenFields': 0,
        'HasPasswordField': 0, 'Bank': 0, 'Pay': 0, 'Crypto': 0,
        'HasCopyrightInfo': 1, 'NoOfEmptyRef': 0, 'JS_to_CSS_ratio': 0.8,
        'External_to_Self_ratio': 0.22, 'Code_density': 0.35
    }
])

# 8. Site gouvernemental (.gov)
legitimate_government = {
    'URLLength': 35,
    'IsDomainIP': 0,
    'URLSimilarityIndex': 98,  # Très élevé pour sites officiels
    'CharContinuationRate': 0.05,
    'TLDLegitimateProb': 0.52,
    'TLDLength': 3,
    'NoOfSubDomain': 1,
    'HasObfuscation': 0,
    'NoOfObfuscatedChar': 0,
    'LetterRatioInURL': 0.92,
    'DegitRatioInURL': 0.01,
    'NoOfEqualsInURL': 0,
    'NoOfQMarkInURL': 0,
    'NoOfAmpersandInURL': 0,
    'SpacialCharRatioInURL': 0.07,
    'LargestLineLength': 650,  # Code très propre
    'HasTitle': 1,
    'DomainTitleMatchScore': 98,
    'URLTitleMatchScore': 95,
    'HasFavicon': 1,
    'Robots': 1,
    'IsResponsive': 1,
    'NoOfURLRedirect': 0,
    'NoOfSelfRedirect': 0,
    'HasDescription': 1,
    'NoOfPopup': 0,
    'NoOfiFrame': 0,
    'HasExternalFormSubmit': 0,
    'HasSocialNet': 1,
    'HasSubmitButton': 0,
    'HasHiddenFields': 0,
    'HasPasswordField': 0,
    'Bank': 0,
    'Pay': 0,
    'Crypto': 0,
    'HasCopyrightInfo': 1,
    'NoOfEmptyRef': 0,
    'JS_to_CSS_ratio': 0.5,  # Peu de JS
    'External_to_Self_ratio': 0.15,  # Tout en local
    'Code_density': 0.28
}

# 9. Site éducatif (.edu / université)
legitimate_education = {
    'URLLength': 48,
    'IsDomainIP': 0,
    'URLSimilarityIndex': 90,
    'CharContinuationRate': 0.10,
    'TLDLegitimateProb': 0.52,
    'TLDLength': 3,
    'NoOfSubDomain': 2,  # portal.university.edu
    'HasObfuscation': 0,
    'NoOfObfuscatedChar': 0,
    'LetterRatioInURL': 0.87,
    'DegitRatioInURL': 0.04,
    'NoOfEqualsInURL': 0,
    'NoOfQMarkInURL': 0,
    'NoOfAmpersandInURL': 0,
    'SpacialCharRatioInURL': 0.09,
    'LargestLineLength': 1100,
    'HasTitle': 1,
    'DomainTitleMatchScore': 90,
    'URLTitleMatchScore': 88,
    'HasFavicon': 1,
    'Robots': 1,
    'IsResponsive': 1,
    'NoOfURLRedirect': 0,
    'NoOfSelfRedirect': 0,
    'HasDescription': 1,
    'NoOfPopup': 0,
    'NoOfiFrame': 1,  # Vidéos de cours
    'HasExternalFormSubmit': 0,
    'HasSocialNet': 1,
    'HasSubmitButton': 0,
    'HasHiddenFields': 0,
    'HasPasswordField': 0,
    'Bank': 0,
    'Pay': 0,
    'Crypto': 0,
    'HasCopyrightInfo': 1,
    'NoOfEmptyRef': 1,
    'JS_to_CSS_ratio': 1.1,
    'External_to_Self_ratio': 0.30,
    'Code_density': 0.40
}

# 10. Startup tech / SaaS moderne
legitimate_saas = {
    'URLLength': 32,
    'IsDomainIP': 0,
    'URLSimilarityIndex': 88,
    'CharContinuationRate': 0.15,
    'TLDLegitimateProb': 0.48,
    'TLDLength': 3,
    'NoOfSubDomain': 2,  # app.startup.com
    'HasObfuscation': 0,
    'NoOfObfuscatedChar': 0,
    'LetterRatioInURL': 0.86,
    'DegitRatioInURL': 0.03,
    'NoOfEqualsInURL': 0,
    'NoOfQMarkInURL': 0,
    'NoOfAmpersandInURL': 0,
    'SpacialCharRatioInURL': 0.11,
    'LargestLineLength': 1400,
    'HasTitle': 1,
    'DomainTitleMatchScore': 85,
    'URLTitleMatchScore': 82,
    'HasFavicon': 1,
    'Robots': 1,
    'IsResponsive': 1,
    'NoOfURLRedirect': 0,
    'NoOfSelfRedirect': 0,
    'HasDescription': 1,
    'NoOfPopup': 0,
    'NoOfiFrame': 0,
    'HasExternalFormSubmit': 0,
    'HasSocialNet': 1,
    'HasSubmitButton': 1,  # Formulaire d'inscription
    'HasHiddenFields': 0,
    'HasPasswordField': 0,
    'Bank': 0,
    'Pay': 0,
    'Crypto': 0,
    'HasCopyrightInfo': 1,
    'NoOfEmptyRef': 2,
    'JS_to_CSS_ratio': 1.8,  # SPA moderne, plus de JS
    'External_to_Self_ratio': 0.35,
    'Code_density': 0.45
}

# 11. Forum / communauté légitime
legitimate_forum = {
    'URLLength': 55,
    'IsDomainIP': 0,
    'URLSimilarityIndex': 82,
    'CharContinuationRate': 0.20,
    'TLDLegitimateProb': 0.45,
    'TLDLength': 3,
    'NoOfSubDomain': 1,
    'HasObfuscation': 0,
    'NoOfObfuscatedChar': 0,
    'LetterRatioInURL': 0.80,
    'DegitRatioInURL': 0.10,  # IDs de posts
    'NoOfEqualsInURL': 1,
    'NoOfQMarkInURL': 1,
    'NoOfAmpersandInURL': 1,
    'SpacialCharRatioInURL': 0.10,
    'LargestLineLength': 1600,
    'HasTitle': 1,
    'DomainTitleMatchScore': 80,
    'URLTitleMatchScore': 75,
    'HasFavicon': 1,
    'Robots': 1,
    'IsResponsive': 1,
    'NoOfURLRedirect': 0,
    'NoOfSelfRedirect': 0,
    'HasDescription': 1,
    'NoOfPopup': 0,
    'NoOfiFrame': 0,
    'HasExternalFormSubmit': 0,
    'HasSocialNet': 1,
    'HasSubmitButton': 1,  # Formulaire de commentaire
    'HasHiddenFields': 1,  # CSRF token
    'HasPasswordField': 0,
    'Bank': 0,
    'Pay': 0,
    'Crypto': 0,
    'HasCopyrightInfo': 1,
    'NoOfEmptyRef': 3,
    'JS_to_CSS_ratio': 1.4,
    'External_to_Self_ratio': 0.28,
    'Code_density': 0.42
}

# 12. Banque légitime (interface de connexion)
legitimate_banking = {
    'URLLength': 40,
    'IsDomainIP': 0,
    'URLSimilarityIndex': 95,
    'CharContinuationRate': 0.08,
    'TLDLegitimateProb': 0.52,
    'TLDLength': 3,
    'NoOfSubDomain': 2,  # online.bank.com
    'HasObfuscation': 0,
    'NoOfObfuscatedChar': 0,
    'LetterRatioInURL': 0.88,
    'DegitRatioInURL': 0.02,
    'NoOfEqualsInURL': 0,
    'NoOfQMarkInURL': 0,
    'NoOfAmpersandInURL': 0,
    'SpacialCharRatioInURL': 0.10,
    'LargestLineLength': 800,  # Code sécurisé et propre
    'HasTitle': 1,
    'DomainTitleMatchScore': 95,
    'URLTitleMatchScore': 93,
    'HasFavicon': 1,
    'Robots': 1,
    'IsResponsive': 1,
    'NoOfURLRedirect': 0,
    'NoOfSelfRedirect': 0,
    'HasDescription': 1,
    'NoOfPopup': 0,
    'NoOfiFrame': 0,
    'HasExternalFormSubmit': 0,  # Important: formulaire local
    'HasSocialNet': 1,
    'HasSubmitButton': 1,  # Login button
    'HasHiddenFields': 1,  # CSRF protection
    'HasPasswordField': 1,  # Login form
    'Bank': 1,  # Mentions banking
    'Pay': 0,
    'Crypto': 0,
    'HasCopyrightInfo': 1,
    'NoOfEmptyRef': 0,
    'JS_to_CSS_ratio': 0.9,
    'External_to_Self_ratio': 0.12,  # Très peu d'externe
    'Code_density': 0.32
}

# 13. Petit blog personnel (WordPress)
legitimate_personal_blog = {
    'URLLength': 44,
    'IsDomainIP': 0,
    'URLSimilarityIndex': 75,
    'CharContinuationRate': 0.25,
    'TLDLegitimateProb': 0.40,
    'TLDLength': 3,
    'NoOfSubDomain': 1,
    'HasObfuscation': 0,
    'NoOfObfuscatedChar': 0,
    'LetterRatioInURL': 0.83,
    'DegitRatioInURL': 0.07,
    'NoOfEqualsInURL': 1,
    'NoOfQMarkInURL': 1,
    'NoOfAmpersandInURL': 0,
    'SpacialCharRatioInURL': 0.10,
    'LargestLineLength': 1800,
    'HasTitle': 1,
    'DomainTitleMatchScore': 70,
    'URLTitleMatchScore': 68,
    'HasFavicon': 1,
    'Robots': 1,
    'IsResponsive': 1,
    'NoOfURLRedirect': 0,
    'NoOfSelfRedirect': 0,
    'HasDescription': 1,
    'NoOfPopup': 0,
    'NoOfiFrame': 1,  # YouTube embeds
    'HasExternalFormSubmit': 0,
    'HasSocialNet': 1,
    'HasSubmitButton': 1,  # Comment form
    'HasHiddenFields': 1,
    'HasPasswordField': 0,
    'Bank': 0,
    'Pay': 0,
    'Crypto': 0,
    'HasCopyrightInfo': 1,
    'NoOfEmptyRef': 4,
    'JS_to_CSS_ratio': 1.3,
    'External_to_Self_ratio': 0.40,  # WordPress utilise CDNs
    'Code_density': 0.48
}