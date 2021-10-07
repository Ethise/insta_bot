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

    @property
    def is_privat_user(self):
        try:
            self.browser.find_element_by_class_name('_4Kbb_._54f4m')
            print('Приватный аккаунт')
            return True
        except:
            return False

    def get_path_all_post(self, nick):
        sleep(randint(2, 4))

        self.go_to_user(nick)
        if self.is_privat_user:
            self.close_conn()
        else:
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

    @property
    def _is_friend(self):
        try:
            self.browser.find_element_by_class_name('glyphsSpriteFriend_Follow.u-__7')
            return True
        except:
            return False

    def add_new_friend(self, nick):
        sleep(randint(2, 4))

        self.go_to_user(nick)
        if not self._is_friend:
            if self.is_privat_user:
                subscribe = self.browser.find_element_by_class_name('sqdOP.L3NKy.y3zKF')
            else:
                subscribe = self.browser.find_element_by_class_name('_5f5mN.jIbKX._6VtSN.yZn4P')
            subscribe.click()

        sleep(randint(2, 4))

    def _get_33_post_location(self, path_loc):
        self.browser.get(path_loc)
        work_field = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]')
        post_containers = [url.get_attribute('href') for url in work_field.find_elements_by_tag_name('a')]
        return post_containers

    def _get_33_user_location(self, path_loc):
        sleep(randint(2, 4))

        users = []
        url_posts = self._get_33_post_location(path_loc)
        for url_post in url_posts:
            self.browser.get(url_post)
            user = self.browser.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/span/a'
            ).get_attribute('href')
            self.press_like()
            users.append(user)
            sleep(randint(2, 4))
        return users

    @staticmethod
    def _get_nick_from_url(url):
        return url.split('/')[-2]

    def add_new_location_friend(self, path_loc):
        sleep(randint(2, 4))

        users = self._get_33_user_location(path_loc)
        for user in users:
            try:
                self.add_new_friend(self._get_nick_from_url(user))
            except:
                pass
            sleep(randint(2, 4))

    def add_friends_of_friend(self, nick):
        friend = self.go_to_user(nick)

    def close_conn(self):
        sleep(randint(8, 15))
        self.browser.close()
        self.browser.quit()


a = InstaBot(log, pas, comment)
a.sing_in()
a.add_new_location_friend('https://www.instagram.com/explore/locations/212898659/kyiv-ukraine/')
a.close_conn()
