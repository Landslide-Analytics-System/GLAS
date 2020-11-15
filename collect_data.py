from core.scrapers.precip_scraper import PreciptationScraper


def main():
    precip_scr = PreciptationScraper()
    precip_scr.collect()
    print(precip_scr.data)


if __name__ == "__main__":
    main()