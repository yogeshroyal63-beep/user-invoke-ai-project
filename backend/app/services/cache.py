# app/services/cache.py

domain_cache = {}

def get_cached_domain(domain):
    return domain_cache.get(domain)

def set_cached_domain(domain, data):
    domain_cache[domain] = data
