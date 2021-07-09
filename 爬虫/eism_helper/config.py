

# selenium 相关
# driver path
# driver_path = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

driver_path = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
chrome_user_data_path = r"C:\Users\ztn\AppData\Local\Google\Chrome\User Data"

server_name = "primera"
# 主url
url = "https://%s.e-sim.org/" % server_name

username = "Light L"
password = "569853885"
user_id = "426056"
# requests header

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.77 Safari/537.36",
}