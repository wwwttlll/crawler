import json
import requests
if __name__ == "__main__":
    post_url = "https://fanyi.baidu.com/sug"
    word = input("input a word:")
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54"}
    data = {"kw" : word}
    response = requests.post(url = post_url,data = data, headers=headers)
    dic = response.json()
    mean = dic['data']
    fileName = word + '.txt'
    f = open(fileName,"w",encoding="utf-8")
    for i in mean:
        for key, value in i.items():
            if(key == 'k'):
                print("word:",value,file=f)
            else :
                print("含义: " + str(value),file=f)
    f.close()

