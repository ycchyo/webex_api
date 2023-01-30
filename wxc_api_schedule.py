import requests
import json
import datetime
import pandas as pd
import jpholiday
import collections as cl
import os

# 当年の祝日を出力
# YEAR = "2023"


# print(list_Date[0])
# print(list_name)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)
#
file_path = resource_path('./userinfo.csv')
df = pd.read_csv(file_path, encoding='utf_8', keep_default_na=False, low_memory=False)
# print(df.iloc[0,1])

TOKEN = df.iloc[0, 1]
ORG_ID = df.iloc[1, 1]
LOCID = df.iloc[2, 1]
HOLIDAY_NAME = df.iloc[3, 1]
YEAR = df.iloc[4, 1]

holiday = jpholiday.year_holidays(int(YEAR))
df_holiday = pd.DataFrame(holiday, columns=["Date", "name"])
print(df_holiday)
list_name = df_holiday["name"].to_list()
list_Date = df_holiday["Date"].to_list()

# TOKEN = "OTkxZDJhNGItN2M3My00NTdhLWI0ZWMtMTc2MTdiMmM2OWZmMDk1NDhiYjEtZDI0_PF84_0198f08a-3880-4871-b55e-4863ccf723d5"
# ORG_ID = "4206e26d-776d-4a38-a8fc-7b8cc8b73452"
# LOCID = 'Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzQzODM4ZDYyLTdmMWEtNDA5YS05ZDM4LWVmMGYzZDYxNmZmMQ'
# HOLIDAY_NAME = "API-Holiday3"
now = datetime.datetime.now()

url = f"https://webexapis.com/v1/telephony/config/numbers?orgId={ORG_ID}"
url_base = f"https://webexapis.com/v1/"
url_base_wxc = f"https://webexapis.com/v1/telephony/config/"
payload = {}
headers = {
  'Authorization': f'Bearer {TOKEN}',
  'Content-Type': 'application/json'
}




def main():

    st_true = True
    h_date = dict()
    data = cl.OrderedDict()

    data["events"] = []

    for i in range(len(list_name)):
        data["events"].append({
            "name": f"{list_name[i]}",
            "startDate": f"{list_Date[i]}",
            "endDate": f"{list_Date[i]}",
            "allDayEnabled": st_true
        })
    h_date = data["events"]

    # print(h_date)
    #日本語文字化けascii

    payload = json.dumps({
        # "name": HOLIDAY_NAME,
        "name": "API-Holiday3",
        "type": "holidays",
        "events": h_date
    }, ensure_ascii=False).encode("utf-8")
    # print(type(payload))
    # print(payload)

    url_api = url_base_wxc + f"locations/{LOCID}/schedules?orgId={ORG_ID}"
    response = requests.request("POST", url_api, headers=headers,
                             data=payload)


    res_j = response.json()
    print("POST ----------------------------")
    print(response)
    print(json.dumps(res_j, indent=4, ensure_ascii=False))

    # fw = open('holiday.json', 'w', encoding="cp932")
    # hjson_schedule = payload.decode('utf-8')
    # json.dump(hjson_schedule, fw, indent=4)

if __name__ == '__main__':
    main()

