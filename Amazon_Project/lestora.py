from bs4 import BeautifulSoup
import requests
import xlsxwriter
import time
import random

urls = [
    'https://www.amazon.com/dp/B07DPLLXS9/?th=1',
    'https://www.amazon.com/dp/B09HC57WDZ/',
    'https://www.amazon.com/dp/B0CJZMP7L1/?th=1',
    'https://www.amazon.com/dp/B000TVJ6XW/?th=1',
    'https://www.amazon.com/dp/B00D3OR58A/ref=sspa_dk_detail_3?psc=1&pd_rd_i=B00D3OR58A&pd_rd_w=VskSo&content-id=amzn1.sym.386c274b-4bfe-4421-9052-a1a56db557ab&pf_rd_p=386c274b-4bfe-4421-9052-a1a56db557ab&pf_rd_r=0P16CGAFC4A1RBX8YHZN&pd_rd_wg=Wv3ah&pd_rd_r=9ddb02d0-aeb8-4fd0-bad6-22b5a1b7927b&s=office-products&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWxfdGhlbWF0aWM',
    'https://www.amazon.com/LEVOIT-Humidifiers-Humidifier-Shut-off-BPA-Free/dp/B0C2C9NHZW?ref=dlx_deals_dg_dcl_B0C2C9NHZW_dt_sl14_cd&th=1',
    'https://www.amazon.com/SAMSUNG-ViewFinity-Ultrawide-Borderless-LS34C50DGANXZA/dp/B0C6LSD69F?ref=dlx_deals_dg_dcl_B0C6LSD69F_dt_sl14_cd&th=1',
    'https://www.amazon.com/dp/B0CJK4ZVDP/ref=sspa_dk_detail_5?pd_rd_i=B0CJK4ZVDP&pd_rd_w=VJccf&content-id=amzn1.sym.386c274b-4bfe-4421-9052-a1a56db557ab&pf_rd_p=386c274b-4bfe-4421-9052-a1a56db557ab&pf_rd_r=4DH8XBMNBX8CG09PT4PR&pd_rd_wg=c47E9&pd_rd_r=401b3e84-73bc-4726-a3d3-2a4463a89c9a&s=office-products&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWxfdGhlbWF0aWM&th=1'
    'https://www.amazon.com/Ninja-Single-Serve-Permanent-Removable-CM371/dp/B0CSDRZSGG?ref=dlx_deals_dg_dcl_B0CSDRZSGG_dt_sl14_cd&th=1',
    'https://www.amazon.com/BISSELL%C2%AE-Cordless-Portable-Lithium-Ion-3682/dp/B0BPDY3V3M?ref=dlx_deals_dg_dcl_B0BPDY3V3M_dt_sl14_cd&th=1',
    'https://www.amazon.com/BERIBES-Bluetooth-Headphones-Microphone-Lightweight/dp/B09LYF2ST7?ref=dlx_deals_dg_dcl_B09LYF2ST7_dt_sl14_cd&th=1',
    'https://www.amazon.com/dp/B0CPHRF7WW/ref=sspa_dk_detail_0?psc=1&pd_rd_i=B0CPHRF7WW&pd_rd_w=EyQWQ&content-id=amzn1.sym.386c274b-4bfe-4421-9052-a1a56db557ab&pf_rd_p=386c274b-4bfe-4421-9052-a1a56db557ab&pf_rd_r=S7NFSDRZ3TFP055DXAYH&pd_rd_wg=TpBfj&pd_rd_r=b79e5e52-5e72-4e8a-83bd-da7045f64ae2&s=office-products&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWxfdGhlbWF0aWM'
]


headers = {
    "User-Agent": random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    ]),
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1"
}

workbook = xlsxwriter.Workbook('Amazon.xlsx')
worksheet = workbook.add_worksheet()

headers_row = ["Product ID", "Product Name", "Actual Price", "Rating", "Number of Ratings", "Product Link", "Target"]
for col, header in enumerate(headers_row):
    worksheet.write(0, col, header)

def scrape_product(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        time.sleep(2) 
        soup = BeautifulSoup(response.content, 'html.parser')
        
        
        product_id = url.split("/dp/")[1].split("/")[0] if "/dp/" in url else "N/A"
        
        
        product_name = soup.find(id='productTitle')
        if product_name:
            product_name = product_name.get_text(strip=True)
        else:
            product_name = "N/A"

        
        updatedproductName = product_name[:20]

     
        actual_price = soup.find('span', {'class': 'a-offscreen'})
        if actual_price:
            actual_price = actual_price.get_text(strip=True).strip('$')
        else:
            actual_price = "N/A"
        
        print("..................................")
        print(actual_price)

      
        rating = soup.find('span', {'class': 'a-icon-alt'})
        if rating:
            rating = rating.get_text(strip=True).split()[0]
        else:
            rating = "N/A"

       
        num_ratings = soup.find('span', {'id': 'acrCustomerReviewText'})
        if num_ratings:
            num_ratings = num_ratings.get_text(strip=True).split()[0].replace(",", "")
        else:
            num_ratings = "N/A"

       
        target = random.choice([0, 1])

        return [product_id, updatedproductName, actual_price, rating, num_ratings, url, target]

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return [url, "Error", "Error", "Error", "Error", "Error", "Error"]


for row, url in enumerate(urls, start=1):
    product_details = scrape_product(url)
    for col, detail in enumerate(product_details):
        worksheet.write(row, col, detail)
    
    time.sleep(random.uniform(1, 3))

workbook.close()
print("Data written to Amazon.xlsx")
