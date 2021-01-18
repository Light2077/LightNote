import requests
import os
url ='https://files.yande.re/sample/e55d59ed56233b93e67192082385cc00/yande.re%20549458%20sample%20ass%20bikini%20fate_extella_link%20fate_grand_order%20nekoshoko%20saber_extra%20swimsuits%20thong%20topless.jpg'
root = 'D://pics//'
path = root + url.split('/')[-1]
try:
    if not os.path.exists(root):
        os.mkdir(root)
    if not os.path.exists(path):
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
            f.close()
            print('文件保存成功')
    else:
        print('文件已存在')
except:
    print('爬取失败')


