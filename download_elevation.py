from core.scrapers.elevation_scraper import ElevationScraper


def main():
    elevation_scr = ElevationScraper()
    elevation_scr.download_data()
    print("Downloading data from " + elevation_scr.data_url)
    

if __name__ == "__main__":
    main()