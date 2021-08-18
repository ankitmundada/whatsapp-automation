from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import argparse
import csv
import urllib
from tqdm import tqdm

SEND_STATUS_COL = 'is_sent'

WA_WEB_URL = 'https://web.whatsapp.com'
SEND_BUTTON_XPATH = '/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[2]/button'

input_header = None
output_header = None

args = argparse.ArgumentParser()

args.add_argument("--template", type=str, required=True, default=None)
args.add_argument("--data", type=str, required=True, default=None)

args = args.parse_args()


options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=chrome-data")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)


with open(args.template, "r", encoding="utf-8") as f:
    template = f.read().strip()

with open(args.data, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    input_header = reader.fieldnames
    output_header = input_header + [SEND_STATUS_COL]
    input_data = list(reader)

print("Total {} contacts will be processed".format(len(input_data)))


failure_count = 0
with open(args.data.split('.')[0] + "-results.csv", "a") as results_file:
    writer = csv.DictWriter(results_file, output_header)
    writer.writeheader()

    count = 0
    for data in tqdm(input_data):
        if 'is_sent' in data and data['is_sent'] == 'True':
            continue
        else:
            count += 1
            phone = "+91" + data['phone'].replace("+91", "")
            message = template.format(**data)

            # print("processing contact number: {}".format(count))

            try:
                params = {"phone": phone, "text": message}
                browser.get(WA_WEB_URL + "/send?" +
                            urllib.parse.urlencode(params))
                time.sleep(10)

                send = browser.find_element_by_xpath(SEND_BUTTON_XPATH)
                send.click()

                time.sleep(5)
                data[SEND_STATUS_COL] = True
            except:
                # print("FAILED TO PROCESS: contact number  {}".format(count))
                failure_count += 1
                data[SEND_STATUS_COL] = False

        writer.writerow(data)

print("FAILED TO PROCESS {} CONTACTS".format(failure_count))
