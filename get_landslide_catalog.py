from core.scrapers.landslide_scraper import LandslideScraper

def main():
    landslide_scr = LandslideScraper()
    landslide_scr.download_data()


if __name__ == "__main__":
    main()