from proxyscrape import create_collector

collector = create_collector('my-collector', 'http')

# Retrieve any http proxy
proxy = collector.get_proxy()

# Retrieve only 'us' proxies
proxy = collector.get_proxy({'code': 'us'})

# Retrieve only anonymous 'uk' or 'us' proxies
proxy = collector.get_proxy({'code': ('us', 'uk'), 'anonymous': True})

# Retrieve all 'ca' proxies
proxies = collector.get_proxies({'code': 'IND'})

print(proxies)