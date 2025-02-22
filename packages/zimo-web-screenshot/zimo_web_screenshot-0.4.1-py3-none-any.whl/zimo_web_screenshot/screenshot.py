import argparse
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def set_local_storage(driver, data):
    driver.execute_script(
        f"localStorage.setItem('websiteSettings', '{json.dumps(data)}');")


def take_screenshot(width, height, theme_name, pathname, delay, filename, quality, scrollY, custom_data=None):
    try:
        chrome_options = Options()
        chrome_options.add_argument(f"--window-size={width},{height}")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--hide-scrollbars")
        chrome_options.add_argument('--force-device-scale-factor=1')
        chrome_options.add_argument('--high-dpi-support=1')

        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {
            'width': width,
            'height': height,
            'deviceScaleFactor': quality,
            'mobile': False
        })
        driver.get(f"https://www.zimoluo.me/{pathname}")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Prepare websiteSettings data
        if custom_data:
            settings_data = {
                "pageTheme": {x: "custom" for x in ["home", "blog", "photos", "projects", "about", "design", "management", "themeMaker"]},
                "customThemeIndex": 0,
                "customThemeData": [custom_data],
                "navigationBar": "always",
            }
        else:
            settings_data = {
                "pageTheme": {x: theme_name for x in ["home", "blog", "photos", "projects", "about", "design", "management", "themeMaker"]},
                "navigationBar": "always",
            }

        set_local_storage(driver, settings_data)

        driver.refresh()

        time.sleep(2)

        driver.execute_script("window.scrollTo(0, arguments[0]);", scrollY)

        time.sleep(1.5)

        time.sleep(delay)  # Optional delay before taking the screenshot

        driver.save_screenshot(f'{filename}.png')
    except KeyboardInterrupt:
        print("Screenshot taking was aborted by the user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


def main():
    parser = argparse.ArgumentParser(
        description="Take a screenshot of a Zimo Web's page with specified settings.")
    parser.add_argument('-w', '--width', type=int,
                        default=1600, help='Width of the browser window')
    parser.add_argument('-H', '--height', type=int,
                        default=900, help='Height of the browser window')
    parser.add_argument('-t', '--theme', type=str,
                        default="pixelland", help='Theme name to apply')
    parser.add_argument('-p', '--pathname', type=str,
                        default="design", help='Path within Zimo Web')
    parser.add_argument('-d', '--delay', type=float,
                        default=0, help='Delay before taking the screenshot')
    parser.add_argument('-f', '--filename', type=str,
                        default='webpage_screenshot', help='Output filename without suffix')
    parser.add_argument('-q', '--quality', type=float,
                        default=1.5, help='The quality of the output image')
    parser.add_argument('-c', '--custom', type=str,
                        help='Path to the custom theme JSON config data')
    parser.add_argument('-sy', '--scrollY', type=int,
                        default=0, help='Vertical scroll offset (in pixels)')

    args = parser.parse_args()

    try:
        custom_data = None
        if args.custom:
            with open(args.custom, 'r') as file:
                custom_data = json.load(file)

        take_screenshot(args.width, args.height, args.theme,
                        args.pathname, args.delay, args.filename, args.quality, args.scrollY, custom_data)
    except Exception as e:
        print(f"Failed to take screenshot: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program was interrupted by the user.")
