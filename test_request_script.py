import requests

target_url = "http://127.0.0.1:8000/api/v1/get_form/"

test_data_list = [
    "news_tag=sport&news_date=23.06.2023&newspaper_name=prevda&author_email=pravoved@pravda.ru",
    "passenger_name=alexandr&passenger_email=aa-slozhno@email.ru&passenger_birth_date=1990-08-12",
    "goods_name=phone&order_date=2023-08-30",
    "bank_name=investbank&bank_manager_email=ev-zolotova@investbank.ru&bank_manager_phone=+7 999 000 98 73",
    "air_company_name=+7 989 756 98 73&air_company_email=01.12.2013&air_company_phone=788_fax@mail.com",
    "rental_name=superrent&rental_phone=89199834455&rent_date=01.12.2013",
]

for data in test_data_list:
    response = requests.post(url=target_url, data={"req": data})

    print(f"Request Data: {data}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Data: {response.json()} \n")
