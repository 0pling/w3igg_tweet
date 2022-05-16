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
    parser.add_argument("-s", "--skip-check", action="store_true", help="tweet immediately without asking for confirmation")
    parser.add_argument("--url", type=str, help="URL of the entry to tweet (default is the latest entry)")
    args = parser.parse_args()
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.headless = True
    firefox_options.set_preference("layout.css.devPixelsPerPx", "4")
    driver = webdriver.Firefox(
        service=Service(GeckoDriverManager(log_level=0).install()),
        options=firefox_options
    )
    entry = get_entry(driver, args.url)
    if not args.skip_check:
        print("\nTitle")
        print("=====")
        print(entry['title'])
        print("\nDate")
        print("====")
        print(entry['date'])
        print("\nLink")
        print("====")
        print(entry['url'])
        print("\nScreenshot")
        print("==========")
        print(entry['screenshot'])
        print("\nAlt text")
        print("==========")
        print(entry['body-text'])
        confirmation = input("\nTweet it? [y/N]: ")
        if confirmation.lower() != 'y':
            sys.exit()
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
