from typing import List, Set

class Config:
    AD_SERVING_DOMAINS: Set[str] = {
        'doubleclick.net',
        'adservice.google.com',
        'googlesyndication.com',
        'googletagservices.com',
        'googletagmanager.com',
        'google-analytics.com',
        'adsystem.com',
        'adservice.com',
        'adnxs.com',
        'ads-twitter.com',
        'facebook.net',
        'fbcdn.net',
        'amazon-adsystem.com'
    }

    EXCLUDE_SELECTORS: List[str] = [
        # Navigation elements
        "header", "footer", "nav", "aside", "svg", "script", "style", "meta", "link", "noscript", "iframe",
        ".header", ".top", ".navbar", "#header",
        ".footer", ".bottom", "#footer",
        ".navigation", "#nav", ".menu",
        ".breadcrumbs", "#breadcrumbs", ".sidebar", ".side", ".aside", "#sidebar",
        ".widget", "#widget",
        
        # Popups and overlays
        ".modal", ".popup", "#modal", ".overlay",
        
        # Advertisements
        ".ad", ".ads", ".advert", "#ad",
        "[class*='ad-']", "[id*='ad-']",
        "[class*='advertisement']",
        
        # Social media
        ".social", ".social-media", ".social-links", "#social",
        ".share", "#share",
        
        # Language selectors
        ".lang-selector", ".language", "#language-selector",
        
        # Cookie notices
        ".cookie", "#cookie", ".cookie-banner",
        
        # Comments sections
        ".comments", "#comments", ".user-comments",
        
        # Other auxiliary content
        ".newsletter", ".subscribe",
        ".search", "#search",
        ".related", ".recommended", 
        "#omnisend-dynamic-container"
    ]

    FORCE_INCLUDE_SELECTORS: List[str] = [
        "#main",
        ".post-content", 
        ".main-content"
    ]

    DEFAULT_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Not A(Brand";v="99", "Safari";v="17"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'DNT': '1'
    }

    # Attributes to remove during cleaning
    REMOVE_ATTRIBUTES: Set[str] = {
        'aria-labelledby', 'aria-controls', 'data-section-type',
        'data-slick-index', 'data-aspectratio', 'data-section-id',
        'aria-expanded', 'data-index', 'data-product-id', 'aria-label',
        'aria-hidden', 'data-handle', 'data-alpha', 'data-position',
        'tabindex', 'role', 'aria-disabled', 'aria-atomic', 'aria-live',
        'data-autoplay', 'data-speed', 'data-aos', 'data-aos-delay',
        'data-testid', 'data-qa', 'handle-editor-events', 'dir', 'lang',
        'width', 'height', 'type', 'fallback'
    }