import tls_client
import random
import time



def get_token():
    url = "https://www.eldorado.ru/_ajax/spa/auth/getToken.php"
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '__lhash_=4b3d1bb03f4e3c71ad27864e9d56403f; ab_user=790124380100; ab_segment=79; iRegionSectionId=11324; grs=11324; ABT_test=C; AUTORIZZ=0; AC=1; lv_user_org=0; el_group_user_org=0; bonus_cobrand_showed=0; _gcl_au=1.1.342119173.1726907521; GUID=1jgrtdhjrgdqeluwv4qas9mqtzak8itjifrh; rrpvid=17497917767480; advcake_trackid=9fa5e740-a3ba-8a43-4066-52b0fc5febf4; advcake_session_id=d7107ede-7bc6-d154-bce0-96dfc6567357; _userGUID=0:m1bw5hxl:dcOkqkKvDDBCoxEw31Q~q5WdCXHBH~bT; mindboxDeviceUUID=eab19577-f157-4fbb-a247-4665feb4a612; directCrm-session=%7B%22deviceGuid%22%3A%22eab19577-f157-4fbb-a247-4665feb4a612%22%7D; rcuid=66ee8485870b48bf1832a966; _slid=66ee847eed5376891800534d; tmr_lvid=4307c40a52da9657ac2a0dd958f2296d; tmr_lvidTS=1726907526771; gdeslon.ru.__arc_domain=gdeslon.ru; gdeslon.ru.user_id=a0896c7b-5c34-49f1-9b15-8b6c9ee6f0bd; _ym_uid=1726907528195532277; _ym_d=1726907528; uxs_uid=fe7455d0-77f3-11ef-9749-47a9e76c8552; adid=172690753063206; adrcid=ANs7APRi8FdojQ9Tj5RSfDg; adrcid=ANs7APRi8FdojQ9Tj5RSfDg; _slid_server=66ee847eed5376891800534d; dt=1; PHPSESSID=aegikhu5iovqvj1j4fv0fc6rho; _slid=66f188152eafa9bf450fa1a7; _sljsession=2B8755C8-CBE6-4C1B-95E1-C5813804ADEC; _ga=GA1.1.574806082.1726907521; acs_3=%7B%22hash%22%3A%2240a47f53e220d7da5392%22%2C%22nextSyncTime%22%3A1727191448347%2C%22syncLog%22%3A%7B%22224%22%3A1727105048347%2C%221228%22%3A1727105048347%2C%221230%22%3A1727105048347%7D%7D; acs_3=%7B%22hash%22%3A%2240a47f53e220d7da5392%22%2C%22nextSyncTime%22%3A1727191448347%2C%22syncLog%22%3A%7B%22224%22%3A1727105048347%2C%221228%22%3A1727105048347%2C%221230%22%3A1727105048347%7D%7D; domain_sid=xSGATPa2kUK6QiGwtosa6%3A1727105048349; _ym_isad=2; adrdel=1727154484048; adrdel=1727154484048; _ga_4P3TZK55KZ=deleted; __cap_p_=1,0; __cap_=ecb636fb6c85b0ad1c1dc10d877612994cd8a8f2d4bcd2a5e67a596a3dca2c1e; __hash_=416d81706bcd0581c77467059024d6d4; BITRIX_SM_SALE_UID=32651624315; BITRIX_SM_SALE_UID_CS=c1ca85a6ac8b92682aba60d5c5bc8f9d; _slsession=A8867EE1-53E8-4CF1-ABDB-D36A515AAB82; _sp_ses.f3a5=*; _sp_id.f3a5=d8fd8af6-53b7-4bfd-831e-e6668c34b302.1726907525.7.1727167223.1727156794.c506e514-33c0-43d2-8371-b1009091f7e0.056441cd-efad-46fc-b7ff-d0e3149322d0.6b361471-fad9-4897-bf47-5f9b0ebf6346.1727167222780.2; _slsession=A8867EE1-53E8-4CF1-ABDB-D36A515AAB82; _slfreq=646f4a3ad9b723086101fbec%3A646f4a3ad9b723086101fbf0%3A1727174423; _ym_visorc=w; advcake_track_url=%3D202409234KmR9YGQLBlN5CAyGkU1stdL105EqwjGojW35sPMEinIzIasyHcnsolkFfc0avVRgzDhDH8DKcqjbmJMi%2Bv9BGyhu4ByyYRCU6j44NcpfgVpnJ6b5hzfHU4ouhpU11CAsV%2BaFlqSZUULMbBIyLLnE9OBsYBvcsP23kY%2F7MD3GUOCVFyJYFeCqsY6rqHM%2BMOt2%2BhM7toosK%2FMW9RPny3k0X2%2Bf34HnouaOGXgX4dXqwloLYNYAN8ENEoZaArdni9kTwm8w0qAYHGwgTVO%2Bei5adkX8JUyLary2pxQcscXeISwp1YBCflUGCD5YY3WXpOPSgBhWIqoe8Z%2BlsvEm3y82goYGBokzNKykFPhLHW3FEmkReu%2BeYBDUOnf%2FIGfvmSNYfaPOA66WezEk5Dm5ZlmVtpUBnn1j7dKySIf7sj4acZMrIbX1ibG8oSiOpDkvcihoTgRUrh3YLmLvDC4tEHgK9G4odKrGcQ3Z9Eijy9Aj8ENHHl1xQgAuWsPHf25O4LDq%2Fli3joRWCbjAq5y5XHNA3shwO1PzmEuVo%2Flt5B844Q6WavYtsVlzZ%2Bdv2nNgeFxi0IyaAl58c1cj71sldnyq3QEi2kSKQiJmrlDmjPsWbjkTeiursCJSiB97vlUqsCHR2Nc%2FVR%2Bpl3OBn1BUl%2FJ11uvKEcWsTvy6dBcC3N8i2UJhHnIn3Sjuyg%3D; tmr_detect=0%7C1727167225799; gsscgib-w-eldorado=RX05Ivywqbmm2Vnp4WB3karGNKarkRNS9ux5pzKQTkbzSyAAhuCMFIVD53NauTWA+h3iLB7Swu8lTZ+TZgU7reOenczKKblNvQ8FRZdZ9DaCcSC03V7Ag6wkTKPVIM1+/a6UzS3eEOzcHBz8DWNXXF+ZaQb1/KT8IqZISQG3g0lzd7l2XaNqEy3Q1AXnnH8Igr3iXJCAAI1n+JUEuk+BIAD2oa3o48kfjdTE+d9gkwftp2pNt0tNBKCTwP9ngcwIn+tCWy7c; cfidsgib-w-eldorado=hh0j41puRuwKcn+xg7qN278aaTp825CdIYkU+WmlwyhCrhOUfAMuq5Xl8aO1xxkPlMa0qs4aszDEwFdnwx6X6zPoVH7w8jCFIFveAVYSkvpj+I6v5rYN5+uWCZQFM16aSRkZK7ff/yEyefUqsPF9STT1YmhXLKU11XpVaJ0=; gsscgib-w-eldorado=RX05Ivywqbmm2Vnp4WB3karGNKarkRNS9ux5pzKQTkbzSyAAhuCMFIVD53NauTWA+h3iLB7Swu8lTZ+TZgU7reOenczKKblNvQ8FRZdZ9DaCcSC03V7Ag6wkTKPVIM1+/a6UzS3eEOzcHBz8DWNXXF+ZaQb1/KT8IqZISQG3g0lzd7l2XaNqEy3Q1AXnnH8Igr3iXJCAAI1n+JUEuk+BIAD2oa3o48kfjdTE+d9gkwftp2pNt0tNBKCTwP9ngcwIn+tCWy7c; gsscgib-w-eldorado=RX05Ivywqbmm2Vnp4WB3karGNKarkRNS9ux5pzKQTkbzSyAAhuCMFIVD53NauTWA+h3iLB7Swu8lTZ+TZgU7reOenczKKblNvQ8FRZdZ9DaCcSC03V7Ag6wkTKPVIM1+/a6UzS3eEOzcHBz8DWNXXF+ZaQb1/KT8IqZISQG3g0lzd7l2XaNqEy3Q1AXnnH8Igr3iXJCAAI1n+JUEuk+BIAD2oa3o48kfjdTE+d9gkwftp2pNt0tNBKCTwP9ngcwIn+tCWy7c; _ga_4P3TZK55KZ=GS1.1.1727167222.9.0.1727167269.0.0.0; fgsscgib-w-eldorado=ZIwcb6d12115567151b22242892c92ba77956015; fgsscgib-w-eldorado=ZIwcb6d12115567151b22242892c92ba77956015; AUTORIZZ=0; PHPSESSID=aegikhu5iovqvj1j4fv0fc6rho; bonus_cobrand_showed=0; el_group_user_org=0; grs=11324; iRegionSectionId=11324; lv_user_org=0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }

    session = tls_client.Session(client_identifier="chrome_108")
    response = session.get(url, headers=headers)

    return response.json().get("token")

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
    ]
    return random.choice(user_agents)

def get_reviews(product_id, page_number):
    url = f"https://www.eldorado.ru/esp/prx-reviews/v1/product/{product_id}/reviews"
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {get_token()}',
        'cookie': '__lhash_=4b3d1bb03f4e3c71ad27864e9d56403f; ab_user=790124380100; ab_segment=79; iRegionSectionId=11324; grs=11324; ABT_test=C; AUTORIZZ=0; AC=1; lv_user_org=0; el_group_user_org=0; bonus_cobrand_showed=0; _gcl_au=1.1.342119173.1726907521; GUID=1jgrtdhjrgdqeluwv4qas9mqtzak8itjifrh; rrpvid=17497917767480; advcake_trackid=9fa5e740-a3ba-8a43-4066-52b0fc5febf4; advcake_session_id=d7107ede-7bc6-d154-bce0-96dfc6567357; _userGUID=0:m1bw5hxl:dcOkqkKvDDBCoxEw31Q~q5WdCXHBH~bT; mindboxDeviceUUID=eab19577-f157-4fbb-a247-4665feb4a612; directCrm-session=%7B%22deviceGuid%22%3A%22eab19577-f157-4fbb-a247-4665feb4a612%22%7D; rcuid=66ee8485870b48bf1832a966; _slid=66ee847eed5376891800534d; tmr_lvid=4307c40a52da9657ac2a0dd958f2296d; tmr_lvidTS=1726907526771; gdeslon.ru.__arc_domain=gdeslon.ru; gdeslon.ru.user_id=a0896c7b-5c34-49f1-9b15-8b6c9ee6f0bd; _ym_uid=1726907528195532277; _ym_d=1726907528; uxs_uid=fe7455d0-77f3-11ef-9749-47a9e76c8552; adid=172690753063206; adrcid=ANs7APRi8FdojQ9Tj5RSfDg; adrcid=ANs7APRi8FdojQ9Tj5RSfDg; _slid_server=66ee847eed5376891800534d; dt=1; PHPSESSID=aegikhu5iovqvj1j4fv0fc6rho; _slid=66f188152eafa9bf450fa1a7; _sljsession=2B8755C8-CBE6-4C1B-95E1-C5813804ADEC; _ga=GA1.1.574806082.1726907521; acs_3=%7B%22hash%22%3A%2240a47f53e220d7da5392%22%2C%22nextSyncTime%22%3A1727191448347%2C%22syncLog%22%3A%7B%22224%22%3A1727105048347%2C%221228%22%3A1727105048347%2C%221230%22%3A1727105048347%7D%7D; acs_3=%7B%22hash%22%3A%2240a47f53e220d7da5392%22%2C%22nextSyncTime%22%3A1727191448347%2C%22syncLog%22%3A%7B%22224%22%3A1727105048347%2C%221228%22%3A1727105048347%2C%221230%22%3A1727105048347%7D%7D; domain_sid=xSGATPa2kUK6QiGwtosa6%3A1727105048349; _ym_isad=2; adrdel=1727154484048; adrdel=1727154484048; _ga_4P3TZK55KZ=deleted; __cap_p_=1,0; __cap_=ecb636fb6c85b0ad1c1dc10d877612994cd8a8f2d4bcd2a5e67a596a3dca2c1e; __hash_=416d81706bcd0581c77467059024d6d4; BITRIX_SM_SALE_UID=32651624315; BITRIX_SM_SALE_UID_CS=c1ca85a6ac8b92682aba60d5c5bc8f9d; _slsession=A8867EE1-53E8-4CF1-ABDB-D36A515AAB82; _sp_ses.f3a5=*; _sp_id.f3a5=d8fd8af6-53b7-4bfd-831e-e6668c34b302.1726907525.7.1727167223.1727156794.c506e514-33c0-43d2-8371-b1009091f7e0.056441cd-efad-46fc-b7ff-d0e3149322d0.6b361471-fad9-4897-bf47-5f9b0ebf6346.1727167222780.2; _slsession=A8867EE1-53E8-4CF1-ABDB-D36A515AAB82; _slfreq=646f4a3ad9b723086101fbec%3A646f4a3ad9b723086101fbf0%3A1727174423; _ym_visorc=w; advcake_track_url=%3D202409234KmR9YGQLBlN5CAyGkU1stdL105EqwjGojW35sPMEinIzIasyHcnsolkFfc0avVRgzDhDH8DKcqjbmJMi%2Bv9BGyhu4ByyYRCU6j44NcpfgVpnJ6b5hzfHU4ouhpU11CAsV%2BaFlqSZUULMbBIyLLnE9OBsYBvcsP23kY%2F7MD3GUOCVFyJYFeCqsY6rqHM%2BMOt2%2BhM7toosK%2FMW9RPny3k0X2%2Bf34HnouaOGXgX4dXqwloLYNYAN8ENEoZaArdni9kTwm8w0qAYHGwgTVO%2Bei5adkX8JUyLary2pxQcscXeISwp1YBCflUGCD5YY3WXpOPSgBhWIqoe8Z%2BlsvEm3y82goYGBokzNKykFPhLHW3FEmkReu%2BeYBDUOnf%2FIGfvmSNYfaPOA66WezEk5Dm5ZlmVtpUBnn1j7dKySIf7sj4acZMrIbX1ibG8oSiOpDkvcihoTgRUrh3YLmLvDC4tEHgK9G4odKrGcQ3Z9Eijy9Aj8ENHHl1xQgAuWsPHf25O4LDq%2Fli3joRWCbjAq5y5XHNA3shwO1PzmEuVo%2Flt5B844Q6WavYtsVlzZ%2Bdv2nNgeFxi0IyaAl58c1cj71sldnyq3QEi2kSKQiJmrlDmjPsWbjkTeiursCJSiB97vlUqsCHR2Nc%2FVR%2Bpl3OBn1BUl%2FJ11uvKEcWsTvy6dBcC3N8i2UJhHnIn3Sjuyg%3D; tmr_detect=0%7C1727167225799; gsscgib-w-eldorado=RX05Ivywqbmm2Vnp4WB3karGNKarkRNS9ux5pzKQTkbzSyAAhuCMFIVD53NauTWA+h3iLB7Swu8lTZ+TZgU7reOenczKKblNvQ8FRZdZ9DaCcSC03V7Ag6wkTKPVIM1+/a6UzS3eEOzcHBz8DWNXXF+ZaQb1/KT8IqZISQG3g0lzd7l2XaNqEy3Q1AXnnH8Igr3iXJCAAI1n+JUEuk+BIAD2oa3o48kfjdTE+d9gkwftp2pNt0tNBKCTwP9ngcwIn+tCWy7c; cfidsgib-w-eldorado=hh0j41puRuwKcn+xg7qN278aaTp825CdIYkU+WmlwyhCrhOUfAMuq5Xl8aO1xxkPlMa0qs4aszDEwFdnwx6X6zPoVH7w8jCFIFveAVYSkvpj+I6v5rYN5+uWCZQFM16aSRkZK7ff/yEyefUqsPF9STT1YmhXLKU11XpVaJ0=; gsscgib-w-eldorado=RX05Ivywqbmm2Vnp4WB3karGNKarkRNS9ux5pzKQTkbzSyAAhuCMFIVD53NauTWA+h3iLB7Swu8lTZ+TZgU7reOenczKKblNvQ8FRZdZ9DaCcSC03V7Ag6wkTKPVIM1+/a6UzS3eEOzcHBz8DWNXXF+ZaQb1/KT8IqZISQG3g0lzd7l2XaNqEy3Q1AXnnH8Igr3iXJCAAI1n+JUEuk+BIAD2oa3o48kfjdTE+d9gkwftp2pNt0tNBKCTwP9ngcwIn+tCWy7c; gsscgib-w-eldorado=RX05Ivywqbmm2Vnp4WB3karGNKarkRNS9ux5pzKQTkbzSyAAhuCMFIVD53NauTWA+h3iLB7Swu8lTZ+TZgU7reOenczKKblNvQ8FRZdZ9DaCcSC03V7Ag6wkTKPVIM1+/a6UzS3eEOzcHBz8DWNXXF+ZaQb1/KT8IqZISQG3g0lzd7l2XaNqEy3Q1AXnnH8Igr3iXJCAAI1n+JUEuk+BIAD2oa3o48kfjdTE+d9gkwftp2pNt0tNBKCTwP9ngcwIn+tCWy7c; _ga_4P3TZK55KZ=GS1.1.1727167222.9.0.1727167269.0.0.0; fgsscgib-w-eldorado=ZIwcb6d12115567151b22242892c92ba77956015; fgsscgib-w-eldorado=ZIwcb6d12115567151b22242892c92ba77956015; AUTORIZZ=0; PHPSESSID=aegikhu5iovqvj1j4fv0fc6rho; bonus_cobrand_showed=0; el_group_user_org=0; grs=11324; iRegionSectionId=11324; lv_user_org=0',
        'priority': 'u=1, i',
        'referer': 'https://www.eldorado.ru/cat/detail/kofemashina-delonghi-etam-29-510-sb/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'x-gib-fgsscgib-w-eldorado': '6saCf8772b76090c188e253df8c7f73f6487d38e',
        'x-gib-gsscgib-w-eldorado': 'u9mowPsyxhMseiPemRIbwBJnLKzRE3QumgRlf5lLv0Pt6POtbizNduFgcLxNAS5en80/E7ntFTCECr/VpqoZBo/bSEjiAmdbJqARrYFLkN+n4GlvUApzFoR9go/93GDzecfiTI0X5l398+WT4+fAxcCoM1uJEWRamc9JIOoWyIVCUeU1PNZ36VXgxIiVhnbY1G9Zt2+PWBZHL8tolGO8TNjD8O+yiJ+Y5ZldM7IM3URIzPerHAzI4U8AjJZR8Tpif6Yujcnvw+PGjqbabne0FN7Og8PqnJ9N0nRUHy86TfdH',
        'x-source-frontend': 'SPA'
        }
    
    params = {
        'pageNumber': page_number
    }
    
    try:
        client = tls_client.Session(
            client_identifier="chrome_108"
        )
        response = client.get(url, headers=headers, params=params)
        print(response.status_code)
        return response.json()
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        return None

def get_all_reviews(product_id):
    current_page = 1
    while True:
        reviews = get_reviews(product_id, current_page)
        
        if reviews:
            total_reviews = reviews.get("totalReviewsCount", 0)
            total_pages = (total_reviews // 10) + (1 if total_reviews % 10 > 0 else 0)
            
            for review in reviews.get("reviews", []):
                parsed_review = parse_reviews(review)
                print(parsed_review)
            
            if current_page >= total_pages:
                break
            
            current_page += 1
            time.sleep(random.uniform(1, 3))
        else:
            print(f"Failed to fetch reviews for page {current_page}")
            break

def parse_reviews(review):
    return {
        "author": review.get("author", {}).get("name", "Unknown"),
        "date_published": review.get("datetime", "Unknown"),
        "message": review.get("message", "No message"),
        "rating": review.get("rating", 0)
    }


def main():
    product_id = '71472011'
    get_all_reviews(product_id)
    
if __name__ == "__main__":
    main()