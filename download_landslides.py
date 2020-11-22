from core.scrapers.landslide_scraper import LandslideScraper


def main():
    landslide_scr = LandslideScraper()
    landslide_scr.download_data()
    print("Downloading data from " + landslide_scr.csv_url)


if __name__ == "__main__":
    main()