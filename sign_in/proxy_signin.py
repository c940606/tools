import base64
from PIL import Image
from io import BytesIO
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from msedge.selenium_tools import Edge, EdgeOptions

class crackSlideVerificationCode:

    def __init__(self, drive):
        self.driver = drive


    def get_img(self, ele):
        self.driver.set_script_timeout(120)
        time.sleep(2)
        im_bg_b64 = self.driver.execute_script(
            f'return document.getElementsByClassName("{ele}")[0].toDataURL("image/png");')
        # base64 encoded image
        im_b64 = im_bg_b64.split(',')[-1]
        im_bytes = base64.b64decode(im_b64)
        return Image.open(BytesIO(im_bytes))

    def get_offset_distance(self, cut_img, full_img):
        pix_1 = full_img.load()
        pix_2 = cut_img.load()
        threshold = 60

        for x in range(full_img.size[0]):
            # 垂直方向不同像素的计数
            vert_count = 0
            for y in range(full_img.size[1]):
                p_1 = pix_1[x, y]
                p_2 = pix_2[x, y]
                # 找到像素不同的点
                if abs(p_1[0] - p_2[0]) > threshold and abs(p_1[1] - p_2[1]) > threshold and abs(
                        p_1[2] - p_2[2]) > threshold:
                    vert_count += 1
                    # 如果是一条直线返回横坐标距离，测试下来10个像素结果较好
                    # print(vert_count, x)
                    if vert_count > 10:
                        return x


    def move_to_gap(self, element, offset_x):
        action_chains = webdriver.ActionChains(self.driver)
        # 点击，准备拖拽
        action_chains.click_and_hold(element)
        action_chains.pause(0.3)
        action_chains.move_by_offset(offset_x + 7, 0)
        action_chains.pause(0.8)
        action_chains.move_by_offset(-7, 0)
        action_chains.pause(0.6)
        action_chains.release()
        action_chains.perform()


    def crack(self):
        bg_img = self.get_img("geetest_canvas_bg geetest_absolute")
        full_img = self.get_img("geetest_canvas_fullbg geetest_fade geetest_absolute")
        x_offset = self.get_offset_distance(full_img, bg_img)
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".geetest_slider_button")))
        button = self.driver.find_element_by_css_selector(".geetest_slider_button")
        for x in range(-3, 3):
            self.move_to_gap(button, x_offset + x)
            time.sleep(3)
            if not self.driver.find_element_by_class_name('geetest_fullpage_click_box').is_displayed():
                break

def remind():
    from urllib import request, parse
    import time
    import json

    miao_code = "tzvbHWD"
    text = "你好吗？"

    page = request.urlopen(
        "http://miaotixing.com/trigger?" + parse.urlencode({"id": miao_code, "text": text, "type": "json"}))
    result = page.read()
    jsonObj = json.loads(result)
    if (jsonObj["code"] == 0):
        print("成功")
    else:
        print("失败，错误代码：" + str(jsonObj["code"]) + "，描述：" + jsonObj["msg"])

def main():
    from selenium import webdriver
    options = webdriver.ChromeOptions()
    # options = EdgeOptions()
    # options.use_chromium = True
    # options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"  # 浏览器的位置
    # options.add_argument("--proxy-server=''")
    for opt in ["--headless", "--no-sandbox", "--disable-dev-shm-usage","start-maximized", "--disable-extensions"
                "--disable-browser-side-navigation", "enable-automation", "--disable-infobars",
                "enable-features=NetworkServiceInProcess"]:
        options.add_argument(opt)


    # driver = Edge(options=options, executable_path=r"./msedgedriver.exe")  # 相应的浏览器的驱动位置
    driver = webdriver.Chrome()
    driver.get("https://www.520ssr.top/user")

    driver.find_element_by_id("email").send_keys("762307667@qq.com")
    driver.find_element_by_id("password").send_keys("caiwei940606")

    driver.find_element_by_xpath(r'//*[@id="login_form"]/div[3]/div/div/div[3]').click()
    verf = crackSlideVerificationCode(driver)
    verf.crack()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "login_submit"))).click()
    # driver.find_element_by_id("login_submit").click()
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "checkin"))).click()
    except:
        pass
    finally:
        if WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "已签到"))).is_displayed():
            print("已签到")
        driver.quit()







if __name__ == '__main__':
    # main()

    remind()