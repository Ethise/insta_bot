from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from config import log, pas
from random import randint
from comments_dictionary import comment


class InstaBot:

    base_url = 'https://www.instagram.com'

    @staticmethod
    def conn_webdriver(path):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('window-size=1200,1000')
            return webdriver.Chrome(path, chrome_options=options)
        except:
            print('Не удалось подключится к драйверу')

    def __init__(self, login, password, comments, path=r'google\chromedriver'):
        self.login = login
        self.password = password
        self.browser = self.conn_webdriver(path)
        self.comments = comments
        self.base_comments = self.comments['default']

    def sing_in(self):
        try:
            self.browser.get(self.base_url)
            sleep(randint(3, 7))

            login = self.browser.find_element_by_name('username')
            login.clear()
            login.send_keys(log)

            sleep(randint(2, 4))

            password = self.browser.find_element_by_name('password')
            password.clear()
            password.send_keys(self.password)

            sleep(randint(2, 4))

            password.send_keys(Keys.ENTER)

            sleep(randint(2, 4))
        except:
            self.close_conn()

    def go_to_user(self, nick):
        try:
            url = self.base_url + '/' + nick
            return self.browser.get(url)
        except:
            print('Такого пользователя нет')
            self.close_conn()

    def _get_number_posts(self):
        res = self.browser.find_elements_by_class_name('g47SY ')
        return int(res[0].text.replace(' ', ''))

    def get_path_all_post(self, nick):
        sleep(randint(2, 4))

        self.go_to_user(nick)
        try:
            self.browser.find_element_by_class_name('_4Kbb_._54f4m')
            print('Приватный аккаунт')
            self.close_conn()
        except:
            num = self._get_number_posts()
            loops = num // 12 + 1
            all_urls = set()

            for i in range(loops):
                sleep(randint(2, 4))
                all_posts = self.browser.find_element_by_class_name('_2z6nI')
                urls = [url.get_attribute('href') for url in all_posts.find_elements_by_tag_name('a')]
                all_urls.update(urls)
                self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')

            sleep(randint(2, 4))

            return all_urls

    def press_like(self):
        like = self.browser.find_element_by_class_name('fr66n')
        like = like.find_element_by_class_name('_8-yf5 ')
        if like.get_attribute('color') == '#262626':
            like.click()
        sleep(randint(2, 4))

    def write_comment(self):
        com = self.browser.find_element_by_class_name('Ypffh')
        com.click()
        c = self.base_comments[randint(0, len(self.base_comments) - 1)]
        sleep(randint(1, 2))
        try:
            com.send_keys(c)
        except:
            com = self.browser.find_element_by_class_name('Ypffh.focus-visible')
            com.send_keys(c)
        sleep(randint(2, 4))

        com.send_keys(Keys.ENTER)

    def event_all_posts(self, nick, switch='all'):
        all_urls = self.get_path_all_post(nick)

        count = 1
        count_all = 1
        all_num_posts = len(all_urls)

        for post in all_urls:
            if count >= 50:
                sleep(3600)
                count = 1
            self.browser.get(post)
            sleep(randint(1, 3))
            if switch == 'like' or switch == 'all':
                self.press_like()
            if switch == 'comment' or switch == 'all':
                self.write_comment()
            sleep(randint(2, 4))

            print(f'{count_all} / {all_num_posts}')
            count += 1
            count_all += 1

    def close_conn(self):
        sleep(randint(8, 15))
        self.browser.close()
        self.browser.quit()


a = InstaBot(log, pas, comment)
a.sing_in()
a.event_all_posts('xenoner1506')
a.close_conn()
