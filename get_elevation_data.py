from core.scrapers.elevation_scraper import ElevationScraper


def main():
    elevation_scr = ElevationScraper()
    elevation_scr.download_from_urls()
    elevation_scr.unzip_all()
    

if __name__ == "__main__":
    main()