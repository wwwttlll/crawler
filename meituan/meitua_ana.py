#对爬取数据处理
import json
import pandas as pd
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
    data = pd.DataFrame(data_parse).T
    data.columns=['id', '地址', '评论数量', '平均得分', '平均价格']
    print(data)
    return data
if __name__ == "__main__":
    for page in range(1,11):
        filename = "meituan"+str(page)+".json"
        with open(filename,"r",encoding="utf-8") as fp:
            data = json.load(fp)
        sol = parsePage(data)
        filename = "data.csv"
        if page == 1:
            sol.to_csv(filename,mode='a')
        else :
            sol.to_csv(filename,mode='a',header=None)
        
        