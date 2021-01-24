from server.scrapers import keystone, kijiji, mckinnon, panadew

scrapers = {
    "keystone": keystone.execute,
    "kijiji": kijiji.execute,
    "mckinnon": mckinnon.execute,
    "panadew"
}