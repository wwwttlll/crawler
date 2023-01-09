#店铺数据爬取
import requests 
from pyquery import PyQuery
import time
import random
import json
import base64
import pandas as pd
import os
import zlib
def downCitynamesfile(citynamesfilepath):
    #cityname映射表
    url = 'https://www.meituan.com/changecity/'
    doc = PyQuery(requests.get(url).text)
    cities_dict = dict()
    [cities_dict.update({city.text(): city.attr('href').replace('.', '/').split('/')[2]}) for city in doc('.cities a').items()]
    with open(citynamesfilepath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(cities_dict, indent=2, ensure_ascii=False))

def getToken():
    #_token
    token = "eJxVjl9vqjAYxr9Lb0dsoZSiybkAYTqkelQU2bILFBSYdNoiKifnu69L3MWSN3n+vL+L5x8QLxkY6Aj1EdJAmwswAHoP9SyggUaqj0WRYZiGadK+pYHd784mpga2Yu2BwRtRf6qb79/FQuU3nWBLsy3VPKxuvWuGqe6beVEIKJrmJAcQyqJX52VzSXlv91lD5WVRQjUBKLSOFKr046HpQ5ufzNRmxcrywJXLg+uxWukzd+jPi9y+D0mCkAeToOyY8O9sdu07024THeP6sLrN640c05FnzO3FrdyEqA2fICcOtxPsTkRAizHx9pwjvw+xDtu/t8l8UrvjaDbd+x6jMbs7WSVm8c7pymYxTO2EnwscY7agvL2IMBiyah1QXhve6jLC29KeZnHqh7vghIyPrjA6kjGZ1T7ZJ76gDg5PPCnX4kAt2EYRFOk27c5u7DEkk2Mzkp86Hl0zkj1Xzet5mYvK5UhM4nh5FlGI8XWZO3/A/y9eFo0L"
    token_decode = base64.b64decode(token)
    token_string = zlib.decompress(token_decode)
    string = str(token_string,"utf-8")
    sign = eval(string)
    print(sign)
    sign['ts'] = int(time.time()*1000)
    sign['cts'] = int(time.time()*1000 + 10000)
    info = str(sign).encode()
    token = base64.b64encode(zlib.compress(info)).decode()
    print(token)
    return token

def getRandomUA():
    #RANDOM USER-AGENT
    df = pd.read_csv("ua.log",sep='\t')
    user_agent = df["UA"].iloc[random.randint(0,1000)]
    return user_agent

def parsePage(data_page):
    data_parse = dict()
    infos = data_page.get('data')
    if infos is None:
        return None
    else:
        infos = infos.get('poiInfos')
        for info in infos:
        # 店名: id 地址, 评论数量, 平均得分, 平均价格
            data_parse[info.get('title')] = [info.get('poiId'),info.get('address'), info.get('allCommentNum'), info.get('avgScore'), info.get('avgPrice')]
    return data_parse

def MTSpider(cityname = "上海", maxpages=10):
    data_pages = {}
    citynamesfilepath = 'cityname.json'
    with open(citynamesfilepath, encoding='utf-8') as f:
        cities = eval(f.read())
    base_url = 'https://{}.meituan.com/meishi/api/poi/getPoiList?'.format(cities[cityname])
    #userId=1882429344&uuid=c3f6ad4e651c4b868a5f.1668315595.1.0.0

    for page in range(1, maxpages+1):
        print('[INFO]: Getting the data of page<%s>...' % page)
        data_page = None
        while data_page is None:
            url = base_url
            # headers = {
            #     'Accept': 'application/json',
            #     'Accept-Encoding': 'gzip, deflate, br',
            #     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            #     'User-Agent': getRandomUA(),
            #     'Connection': 'keep-alive',
            #     'Host': 'sh.meituan.com',
            #     'Referer': 'https://sh.meituan.com/meishi/',
            #     'Cookie':'_lxsdk_cuid=1845238e25cc8-0ac9f157cb4d8f-26021e51-144000-1845238e25dc8; WEBDFPID=4394328z553x5u82z4386299xu08z8x0815475x793497958yy7y61w4-1983188029880-1667828029340GEKMGOGfd79fef3d01d5e9aadc18ccd4d0c95074013; _hc.v=ee29cbcb-07d2-e70b-fae4-3de835a202f4.1667828030; _ga_95GX0SH5GM=GS1.1.1667835376.2.1.1667836239.0.0.0; ci=10; rvct=10,73; _ga=GA1.1.1756334387.1667826775; _ga_LYVVHCWVNG=GS1.1.1668320475.3.0.1668320475.0.0.0; mtcdn=K; uuid=82b488d482934d7797fc.1670148410.1.0.0; _lx_utm=utm_source=bing&utm_medium=organic; __mta=87380647.1667827020184.1669612140744.1670148412482.26; client-id=21d2d270-ed08-49a8-b397-f92fe162f942; userTicket=sxoWwZKxiDHqvoUKzzChzVfDfmsUQUWiFcPrlBse; _yoda_verify_resp=jE9HNPxp77i+D/zrtAjKqq9GxABaZMXbZz8CpEyur6Xn5H8E5J8Wbwu15MXDPps6jf2efKuVkHRVd5cW8grCp7urht+3RyalfWy2OuyJJr1q6vYYkPTMM/wKbfLahbSP9w+K5aG3/tFBWTw1MFS69sphjkKA/ddCnKlj2DhAA+PT595058BzUSrRTCaBZYCKT/is/wz3AhxApx7KU3e8OcM8uCD2Krv0j17Oquq/GqSdf8JLRQXjs9EMZtlsThmwm/GwM+uMQUasNycQQ0DYsubsG0a/gnKrSSNbgCW1ayIfv9NW8aDusGm/iX+bI+hl6KITJx5HPcOwoahbZaa2ctCzPvvyUCYC4qCVTTdNnKR8XEHtkpUJ2oaY4pMzldJ5; _yoda_verify_rid=163203710b029002; u=3323916979; n=LIBERATION8936; lt=AgHRI1hAyEvL1PxRrcBhHXGd_VHm-TN4A7tby4tPggjoJ2XeH7Vblmsr643uXRjRGd41VIi-RcabXQAAAABaFQAA5rul1qFltsc5BOZw073kWbWiC8-j8ls_LhhUfM7lBFmGKJaPlCgUujk36uvNTFLT; mt_c_token=AgHRI1hAyEvL1PxRrcBhHXGd_VHm-TN4A7tby4tPggjoJ2XeH7Vblmsr643uXRjRGd41VIi-RcabXQAAAABaFQAA5rul1qFltsc5BOZw073kWbWiC8-j8ls_LhhUfM7lBFmGKJaPlCgUujk36uvNTFLT; token=AgHRI1hAyEvL1PxRrcBhHXGd_VHm-TN4A7tby4tPggjoJ2XeH7Vblmsr643uXRjRGd41VIi-RcabXQAAAABaFQAA5rul1qFltsc5BOZw073kWbWiC8-j8ls_LhhUfM7lBFmGKJaPlCgUujk36uvNTFLT; token2=AgHRI1hAyEvL1PxRrcBhHXGd_VHm-TN4A7tby4tPggjoJ2XeH7Vblmsr643uXRjRGd41VIi-RcabXQAAAABaFQAA5rul1qFltsc5BOZw073kWbWiC8-j8ls_LhhUfM7lBFmGKJaPlCgUujk36uvNTFLT; unc=LIBERATION8936; _lxsdk=1845238e25cc8-0ac9f157cb4d8f-26021e51-144000-1845238e25dc8; firstTime=1670149019766; _lxsdk_s=184dc9a5021-313-0ab-0be||26'}
            # token = getToken()
            # params = {
            #     "cityName": "上海",
            #     "cateId": '0',
            #     'areaId':'0',
            #     'sort': '',
            #     'dinnerCountAttrId': '',
            #     'page': page,
            #     'userId': '3323916979',
            #     'uuid': '82b488d482934d7797fc.1670148410.1.0.0',
            #     'platform': '1',
            #     'partner': '126',
            #     'originUrl': 'https://sh.meituan.com/meishi/',
            #     'riskLevel': '1',
            #     'optimusCode': '10',
            #     '_token' : token
            #     } 
            # res = requests.get(url, headers=headers,timeout=(30,50),params=params)

            cookies = {
                '_lxsdk_cuid': '1845238e25cc8-0ac9f157cb4d8f-26021e51-144000-1845238e25dc8',
                'WEBDFPID': '4394328z553x5u82z4386299xu08z8x0815475x793497958yy7y61w4-1983188029880-1667828029340GEKMGOGfd79fef3d01d5e9aadc18ccd4d0c95074013',
                '_hc.v': 'ee29cbcb-07d2-e70b-fae4-3de835a202f4.1667828030',
                '_ga_95GX0SH5GM': 'GS1.1.1667835376.2.1.1667836239.0.0.0',
                'ci': '10',
                'rvct': '10%2C73',
                '_ga': 'GA1.1.1756334387.1667826775',
                '_ga_LYVVHCWVNG': 'GS1.1.1668320475.3.0.1668320475.0.0.0',
                'client-id': '21d2d270-ed08-49a8-b397-f92fe162f942',
                'uuid': '2bd4b52c57b5478fb767.1670224191.1.0.0',
                '_lx_utm': 'utm_source%3Dbing%26utm_medium%3Dorganic',
                '__mta': '87380647.1667827020184.1670148412482.1670224194758.27',
                'mtcdn': 'K',
                'userTicket': 'NUEUmKwhMKXAuWqqrjdcncettvDpSXKMVgOpRjiC',
                '_yoda_verify_resp': 'leoPZ5ZqayiD8VHGJrv%2FH%2FcNZWTp7Nv2gEa%2Beb2t0qhfBjhhtvpz1t22mhzIWp1jJYuKkxCLAWAiy%2BQd7MV%2FoT4UTEipghomDLV1ALpkIAmsaay8B1ssW7mwiH6R2hs9o6BWiCPRirheKwokv1zdGsu2jo0YpWLNAUv2t%2F5FyFAystb5BF8%2FVZlwgtIQdbvKLyA56xFaqtayPoK6GQhcVkZeBCCF1M0hj3FOBa8tiCURGFLjd1kCA35yHUbdZXWBSDpeBRm1zsH9aC1g52AjQshNq3tvs7jJTlRBZEf2lcrPYYsmlziy3yNk5YMHBMpMZAfKZORhxWwdt4qkzZYMFhimC9zEpGM3ZwJ8vhj022IhOht1NKz3iIOa%2BeV7%2BQiy',
                '_yoda_verify_rid': '1633248e0c80f04b',
                'u': '3323916979',
                'n': 'LIBERATION8936',
                'lt': 'AgGfIyxDIUO9tmJkHm4DjA80MUCfDmOB8fF_znEVWCLlXeOT3CBk9pzcnp3ciZsAIpEjSek_vN_I_gAAAABaFQAAXk_zVpynUT3zGGEhtiixCUcAUEfRJpfGRuGPIv3c3HyrxUhrumSi96QyBTyCL7b7',
                'mt_c_token': 'AgGfIyxDIUO9tmJkHm4DjA80MUCfDmOB8fF_znEVWCLlXeOT3CBk9pzcnp3ciZsAIpEjSek_vN_I_gAAAABaFQAAXk_zVpynUT3zGGEhtiixCUcAUEfRJpfGRuGPIv3c3HyrxUhrumSi96QyBTyCL7b7',
                'token': 'AgGfIyxDIUO9tmJkHm4DjA80MUCfDmOB8fF_znEVWCLlXeOT3CBk9pzcnp3ciZsAIpEjSek_vN_I_gAAAABaFQAAXk_zVpynUT3zGGEhtiixCUcAUEfRJpfGRuGPIv3c3HyrxUhrumSi96QyBTyCL7b7',
                'token2': 'AgGfIyxDIUO9tmJkHm4DjA80MUCfDmOB8fF_znEVWCLlXeOT3CBk9pzcnp3ciZsAIpEjSek_vN_I_gAAAABaFQAAXk_zVpynUT3zGGEhtiixCUcAUEfRJpfGRuGPIv3c3HyrxUhrumSi96QyBTyCL7b7',
                'firstTime': '1670224236868',
                'unc': 'LIBERATION8936',
                '_lxsdk_s': '184e11ea5c4-525-957-f86%7C%7C18',
            }

            headers = {
                'Accept': 'application/json',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Connection': 'keep-alive',
                # 'Cookie': '_lxsdk_cuid=1845238e25cc8-0ac9f157cb4d8f-26021e51-144000-1845238e25dc8; WEBDFPID=4394328z553x5u82z4386299xu08z8x0815475x793497958yy7y61w4-1983188029880-1667828029340GEKMGOGfd79fef3d01d5e9aadc18ccd4d0c95074013; _hc.v=ee29cbcb-07d2-e70b-fae4-3de835a202f4.1667828030; _ga_95GX0SH5GM=GS1.1.1667835376.2.1.1667836239.0.0.0; ci=10; rvct=10%2C73; _ga=GA1.1.1756334387.1667826775; _ga_LYVVHCWVNG=GS1.1.1668320475.3.0.1668320475.0.0.0; client-id=21d2d270-ed08-49a8-b397-f92fe162f942; uuid=2bd4b52c57b5478fb767.1670224191.1.0.0; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; __mta=87380647.1667827020184.1670148412482.1670224194758.27; mtcdn=K; userTicket=NUEUmKwhMKXAuWqqrjdcncettvDpSXKMVgOpRjiC; _yoda_verify_resp=leoPZ5ZqayiD8VHGJrv%2FH%2FcNZWTp7Nv2gEa%2Beb2t0qhfBjhhtvpz1t22mhzIWp1jJYuKkxCLAWAiy%2BQd7MV%2FoT4UTEipghomDLV1ALpkIAmsaay8B1ssW7mwiH6R2hs9o6BWiCPRirheKwokv1zdGsu2jo0YpWLNAUv2t%2F5FyFAystb5BF8%2FVZlwgtIQdbvKLyA56xFaqtayPoK6GQhcVkZeBCCF1M0hj3FOBa8tiCURGFLjd1kCA35yHUbdZXWBSDpeBRm1zsH9aC1g52AjQshNq3tvs7jJTlRBZEf2lcrPYYsmlziy3yNk5YMHBMpMZAfKZORhxWwdt4qkzZYMFhimC9zEpGM3ZwJ8vhj022IhOht1NKz3iIOa%2BeV7%2BQiy; _yoda_verify_rid=1633248e0c80f04b; u=3323916979; n=LIBERATION8936; lt=AgGfIyxDIUO9tmJkHm4DjA80MUCfDmOB8fF_znEVWCLlXeOT3CBk9pzcnp3ciZsAIpEjSek_vN_I_gAAAABaFQAAXk_zVpynUT3zGGEhtiixCUcAUEfRJpfGRuGPIv3c3HyrxUhrumSi96QyBTyCL7b7; mt_c_token=AgGfIyxDIUO9tmJkHm4DjA80MUCfDmOB8fF_znEVWCLlXeOT3CBk9pzcnp3ciZsAIpEjSek_vN_I_gAAAABaFQAAXk_zVpynUT3zGGEhtiixCUcAUEfRJpfGRuGPIv3c3HyrxUhrumSi96QyBTyCL7b7; token=AgGfIyxDIUO9tmJkHm4DjA80MUCfDmOB8fF_znEVWCLlXeOT3CBk9pzcnp3ciZsAIpEjSek_vN_I_gAAAABaFQAAXk_zVpynUT3zGGEhtiixCUcAUEfRJpfGRuGPIv3c3HyrxUhrumSi96QyBTyCL7b7; token2=AgGfIyxDIUO9tmJkHm4DjA80MUCfDmOB8fF_znEVWCLlXeOT3CBk9pzcnp3ciZsAIpEjSek_vN_I_gAAAABaFQAAXk_zVpynUT3zGGEhtiixCUcAUEfRJpfGRuGPIv3c3HyrxUhrumSi96QyBTyCL7b7; firstTime=1670224236868; unc=LIBERATION8936; _lxsdk_s=184e11ea5c4-525-957-f86%7C%7C18',
                'Referer': 'https://sh.meituan.com/meishi/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }

            params = {
                'cityName': '上海',
                'cateId': '0',
                'areaId': '0',
                'sort': '',
                'dinnerCountAttrId': '',
                'page': '1',
                'userId': '3323916979',
                'uuid': '2bd4b52c57b5478fb767.1670224191.1.0.0',
                'platform': '1',
                'partner': '126',
                'originUrl': 'https://sh.meituan.com/meishi/',
                'riskLevel': '1',
                'optimusCode': '10',
                '_token': getToken(),
            }

            res = requests.get('https://sh.meituan.com/meishi/api/poi/getPoiList', params=params, cookies=cookies, headers=headers)

            print(res.text)
            data_page = parsePage(json.loads(res.text))
            filename = "meituan"+ str(page) + ".json"
            with open(filename,"w",encoding = "utf-8") as fp:
                fp.write(str(res.text))
            filename = "soldata"+ str(page) + ".json"
            with open(filename,"w",encoding = "utf-8") as fp:
                fp.write(str(data_page))
            time.sleep(random.randint(20, 30))
if __name__ == "__main__":
    citynamepath = "cityname.json"
    downCitynamesfile(citynamepath)
    MTSpider()