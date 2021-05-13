import requests
from lxml import etree
from multiprocessing.dummy import Pool

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/90.0.4430.93 Safari/537.36"
}

url = "https://www.pearvideo.com/category_5"


def get_html(url):
    resp = requests.get(url, headers=headers)
    return resp.text


def parse(html):
    tree = etree.HTML(html)
    video_idxs = tree.xpath("//span[@class='fav']/@data-id")
    video_msgs = []
    for idx in video_idxs:
        video_url = get_video_url(idx)
        msg = {
            "url": video_url,
            "name": idx + ".mp4",
        }
        video_msgs.append(msg)
        # download_video(video_url, idx)
    return video_msgs
    # 使用线程池下载视频
    # pool = Pool(4)
    # pool.map(download_content, video_msgs)


def get_video_url(idx):
    detail_url = "https://www.pearvideo.com/videoStatus.jsp?"
    video_url = "https://www.pearvideo.com/video_" + idx
    video_headers = headers.copy()
    video_headers["Referer"] = video_url

    params = {
        "contId": idx,
    }
    detail = requests.get(detail_url, headers=video_headers, params=params).json()
    src_url = detail["videoInfo"]["videos"]["srcUrl"]
    src_url = src_url.replace(detail["systemTime"], "cont-" + idx)

    return src_url


# 下载视频使用
def download_content(msg):
    content = requests.get(msg["url"], headers=headers).content
    with open(msg["name"], "wb") as f:
        f.write(content)


if __name__ == '__main__':
    html = get_html(url)
    msgs = parse(html)
    # pool = Pool(4)
    # pool.map(download_content, msgs[:4])