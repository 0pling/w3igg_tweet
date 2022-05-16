"""A simple CLI tool to auto-generate Tweets for @web3isgreat."""

import argparse
import sys

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from dotenv import load_dotenv

from .core import get_entry, tweet


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="A CLI tool to auto-generate Tweets for @web3isgreat."
    )
    parser.add_argument("--url", type=str, help="URL of the entry to tweet")
    args = parser.parse_args()
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.headless = True
    firefox_options.set_preference("layout.css.devPixelsPerPx", "4")
    driver = webdriver.Firefox(
        service=Service(GeckoDriverManager(log_level=0).install()),
        options=firefox_options
    )
    entry = get_entry(driver, args.url)
    try:
        tweet(entry)
        title = entry["title"]
        print(f"Tweeted '{title}'.")
    except KeyError:
        print(
            "Error: Missing environment variables. Set the Twitter API access keys in .env.",
            file=sys.stderr,
        )
    finally:
        driver.quit()
