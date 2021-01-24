from server.scrapers import keystone, kijiji, mckinnon

scrapers = {
    "keystone": keystone.execute,
    "kijiji": kijiji.execute,
    "mickinnon": mckinnon.execute
}