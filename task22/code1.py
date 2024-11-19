# packages/utils.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_web_assets(url):
    try:
        # Gửi request GET tới URL
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

        # Kiểm tra nếu request thành công
        if response.status_code == 200:
            # Phân tích cú pháp nội dung HTML
            soup = BeautifulSoup(response.content, 'html.parser')

            # Lấy các liên kết CSS
            css_links = [
                urljoin(url, link['href']) for link in soup.find_all('link', rel='stylesheet', href=True)
            ]

            # Lấy liên kết favicon
            favicon_links = [
                urljoin(url, link['href']) for link in soup.find_all('link', rel='icon', href=True)
            ] + [
                urljoin(url, link['href']) for link in soup.find_all('link', rel='shortcut icon', href=True)
            ]

            # Lấy các liên kết hình ảnh
            image_links = [
                urljoin(url, img['src']) for img in soup.find_all('img', src=True)
            ]

            # Lấy các liên kết JavaScript
            js_links = [
                urljoin(url, script['src']) for script in soup.find_all('script', src=True)
            ]

            # In thông tin thu thập được
            print(f"CSS Links: {css_links}")
            print(f"Favicon Links: {favicon_links}")
            print(f"Image Links: {image_links}")
            print(f"JavaScript Links: {js_links}")

            # Trả về thông tin đã thu thập
            return {
                'css_links': css_links,
                'favicon_links': favicon_links,
                'image_links': image_links,
                'js_links': js_links
            }
        else:
            print(f"Failed to fetch data from {url}, Status Code: {response.status_code}")
            return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
