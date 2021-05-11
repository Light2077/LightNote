api 参考地址: 
https://github.com/SocialSisterYi/bilibili-API-collect


```python
import time
import requests
from tqdm import tqdm

# cookie 如果过期了需要复制自己浏览器上的cookie
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Maxthon/4.3.2.1000 "
                  "Chrome/30.0.1599.101 "
                  "Safari/537.36",
    "Cookie" : "buvid3=25FB1B85-D30D-4A22-8866-A2E817554C89155820infoc; LIVE_BUVID=AUTO9815732278709473; CURRENT_FNVAL=80; rpdid=|(u)~mkRJY)|0J'ul~JkmRJ|u; blackside_state=1; CURRENT_QUALITY=64; PVID=1; _uuid=482C3495-3E26-82FC-B99B-D7ACFCFA6C5879180infoc; bp_video_offset_627350=523406760760723419; sid=6gdh7g7c; fingerprint=8b144f26ce97ed2fe7eadeda9aaffd6a; buvid_fp=25FB1B85-D30D-4A22-8866-A2E817554C89155820infoc; buvid_fp_plain=25FB1B85-D30D-4A22-8866-A2E817554C89155820infoc; SESSDATA=d5e60fe3%2C1630572846%2Cfe608%2A31; bili_jct=ab046d85ddf4ce46a36c2514e619d653; DedeUserID=627350; DedeUserID__ckMd5=1d23519fd67936cc; bp_t_offset_627350=523409049983544515",
    "Referer" : "https://www.bilibili.com"
    }


# 获取视频的cid
def get_cid(bvid):
    resp = requests.get("http://api.bilibili.com/x/web-interface/view", params={"bvid": bvid}, headers=headers)
    cid = resp.json()["data"]["cid"]
    print(f"video BV{bvid} cid: {cid}")
    return cid


# 获取视频流的 url 和 视频大小
def get_video_stream(bvid):
    url = "http://api.bilibili.com/x/player/playurl"
    cid = get_cid(bvid)
    params = {
        "bvid": bvid,
        "cid": cid
    }
    resp = requests.get(url, params=params, headers=headers)
    url = resp.json()["data"]["durl"][0]["url"]
    size = resp.json()["data"]["durl"][0]["size"]

    print(f"video BV{bvid} size: {size / 1024 / 1024:.2f}Mb")
    return url, size


def download_video(bvid):
    stream_url, size = get_video_stream(bvid)
    resp = requests.get(stream_url, headers=headers, stream=True)
    cur = 0
    chunk_size = 100 * 1024
    from tqdm import tqdm
    pbar = tqdm(total=size, initial=0, desc="download", unit="B", unit_scale=True)

    file_name = bvid + ".flv"
    with open(file_name, "wb") as f:
        # 每次写入100kb
        for chunk in resp.iter_content(chunk_size=chunk_size):
            f.write(chunk)
            pbar.update(chunk_size)
            # cur += chunk_size
            # print("%s/%s" % (cur, size))

if __name__ == "__main__":
    download_video("19K411M7L8")
```

