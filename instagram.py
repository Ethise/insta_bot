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
        num = self._get_number_posts()
        loops = num // 12
        if loops == 0:
            loops = 1
        all_urls = set()

        for i in range(loops):
            sleep(randint(2, 4))
            all_posts = self.browser.find_element_by_class_name('_2z6nI')
            urls = [url.get_attribute('href') for url in all_posts.find_elements_by_tag_name('a')]
            all_urls.update(urls)
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')

        sleep(randint(2, 4))

        return all_urls

    def like_all_posts(self, nick):
        all_urls = self.get_path_all_post(nick)
        count = 1
        count_all = 1
        all_num_posts = len(all_urls)

        for post in all_urls:
            if count >= 40:
                sleep(180)
                count = 1
            self.browser.get(post)
            sleep(randint(1, 3))
            like = self.browser.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button'
            )
            if like.get_attribute('aria-label') == 'Нравится':
                like.click()
            sleep(randint(2, 4))

            print(f'{count_all} / {all_num_posts}')
            count += 1
            count_all += 1

    def all_posts_comments(self, nick):
        all_urls = self.get_path_all_post(nick)
        count = 1
        count_all = 1
        all_num_posts = len(all_urls)

        for post in all_urls:
            if count >= 40:
                sleep(180)
                count = 1
            self.browser.get(post)
            sleep(randint(1, 3))
            comment = self.browser.find_element_by_class_name('Ypffh')
            comment.click()
            c = self.base_comments[randint(0, len(self.base_comments) - 1)]
            sleep(randint(1, 2))
            try:
                comment.send_keys(c)
            except:
                comment = self.browser.find_element_by_class_name('Ypffh.focus-visible')
                comment.send_keys(c)
            sleep(randint(2, 4))

            comment.send_keys(Keys.ENTER)

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
a.like_all_posts('xenoner1506')
a.close_conn()
