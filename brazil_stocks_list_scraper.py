import pandas as pd
import requests
import base64
import json
from time import sleep
import yfinance as yf

url_base = "https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/GetInitialCompanies/"

page_size = 120
total_pages = 26

stocks_df_brazil = pd.DataFrame()

def try_ticker(ticker):
    try:
        stock = yf.Ticker(ticker + '.SA')
    except:
        stock = None
    return stock

for page_num in range(1, total_pages + 1):
    payload = {"language": "pt-br", "pageNumber": page_num, "pageSize": page_size}
    payload_b64 = base64.b64encode(json.dumps(payload).encode()).decode()
    url = url_base + payload_b64

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
        "priority": "u=1, i",
        "referer": "https://sistemaswebb3-listados.b3.com.br/",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "x-dtpc": "24$351147032_225h3vOEGAPLQCSRVFCARKRUABTHNTPMGTPHAW-0e0"
    }

    cookies = {
        "__cf_bm": "P9Ib2JBE7yB2juKG00wi1SCtMGEm1.QIzxq8mPh0hc8-1752352639-1.0.1.1-gQ5nmdy9zf8MAJf.oWHzwRkyBYP.LF1kP37kpe6f1qVa.8Qf.BH9dMNIWw1JYFOYWlQt6iPVkYLOQuWc_02Hg3OkVeCac3Zp3Vu3E5XdgIY",
        "_clck": "1g2sprd%7C2%7Cfxj%7C0%7C2019",
        "_clsk": "xv8k9p%7C1752351715031%7C5%7C1%7Ca.clarity.ms%2Fcollect",
        "_ga": "GA1.1.1380317717.1752350047",
        "_ga_CNJN5WQC5G": "GS2.1.s1752350065$o1$g1$t1752352638$j59$l0$h0",
        "_ga_FTT9L7SR7B": "GS2.1.s1752350047$o1$g1$t1752350061$j46$l0$h0",
        "_ga_SS7FXRTPP3": "GS2.1.s1752350064$o1$g0$t1752350078$j46$l0$h0",
        "_gid": "GA1.3.1859662565.1752350064",
        "dtCookie": "v_4_srv_24_sn_36C25207E70331A4BA6202C9145ACC1C_perc_100000_ol_0_mul_1_app-3Afd69ce40c52bd20e_1_rcs-3Acss_0",
        "dtPC": "24$352637728_626h-vOEGAPLQCSRVFCARKRUABTHNTPMGTPHAW-0e0",
        "dtSa": "-",
        "OptanonAlertBoxClosed": "2025-07-12T19:54:25.425Z",
        "OptanonConsent": "isGpcEnabled=0&datestamp=Sat+Jul+12+2025+16%3A54%3A25+GMT-0300+(Brasilia+Standard+Time)&version=6.21.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0003%3A1%2CC0001%3A1%2CC0004%3A1%2CC0002%3A1&AwaitingReconsent=false",
        "rxVisitor": "17523500448333UGNOEA7VSKBK1PKJFRFOTFEFEEHPC7F",
        "rxvt": "1752354439073|1752350044836",
        "TS0171d45d": "011d592ce101e5230a0879c53112a470f005bc6d6233f45fdafac54bfd2ad937c0737590184bba96454ac7e8a016e3244c02462879",
        "TS01f22489": "011d592ce16bef97350520d988107b8dd75a214583b4fd843fc9b5b54b3780de5684f5cf2c5ac203bebfd7a342a258324b9e33a253",
        "F051234a800": "!/2U4ba5AmSNIjnrJV6atKwfHCrEHsIZxulykQ1LvhR9CvMl28fwMIKC4CtIOFSYCKY5sPEq1T82tnho=",
        "TS01871345": "016e3b076fbd6a32268e27b3aa484f74f105c048091988e3974137ae2bd592330694373c7f23f04cda74fec45e2832276d3258d4b6",
    }

    response = requests.get(url, headers=headers, cookies=cookies)

    if response.status_code != 200:
        tries = 0
        while (tries < 2):
            response = requests.get(url, headers=headers, cookies=cookies)
            if response.status_code == 200:
                break
            tries += 1

    data = response.json()

    page_df = pd.DataFrame(data['results'])

    stocks_df_brazil = pd.concat([stocks_df_brazil, page_df], ignore_index=True)

    sleep(2)

stocks_df_brazil = stocks_df_brazil[(stocks_df_brazil['market'] == 'NM') |
                                    (stocks_df_brazil['market'] == 'N1') |
                                    (stocks_df_brazil['market'] == 'N2') |
                                    (stocks_df_brazil['market'] == 'MA') |
                                    (stocks_df_brazil['market'] == 'M2')]

stocks_df_brazil['ticker'] = stocks_df_brazil['issuingCompany']
stocks_df_brazil = stocks_df_brazil['ticker']

brazil_stocks_list = []

for i in range(len(stocks_df_brazil)):

    ticker = stocks_df_brazil.iloc[i] + '3'
    stock = try_ticker(ticker)

    if stock == None:
        ticker = stocks_df_brazil.iloc[i] + '4'
        stock = try_ticker(ticker)

        if stock == None:
            ticker = stocks_df_brazil.iloc[i] + '5'
            stock = try_ticker(ticker)

            if stock == None:
                ticker = stocks_df_brazil.iloc[i] + '11'
                stock = try_ticker(ticker)

                if stock == None:
                    continue

    brazil_stocks_list.append(ticker)

brazil_stocks_list = pd.DataFrame(brazil_stocks_list, columns=['ticker'])
brazil_stocks_list.to_csv('stocks list/brazil_stocks_list.csv', index=False, sep=';')