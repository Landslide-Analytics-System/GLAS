from core.scrapers.elevation_scraper import ElevationScraper

scraper = ElevationScraper()

scraper.getUrls()
print("Waiting for user to finish storing credentials as cookies...")
print("Hit ENTER to continue once you're done")
input()
scraper.getCredentials()
scraper.downloadAll()