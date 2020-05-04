import random
import re
import time
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
import constant


def curr_time():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time

class Bot:
    PATH = "chromedriver.exe"
    driver = webdriver.Chrome(PATH)

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def login(self):
        self.driver.get(self.url)
        NameXpath = self.driver.find_element_by_xpath(
            '//*[@id="content"]/div[1]/div[1]/form/table/tbody/tr[1]/td[2]/input')
        NameXpath.click()
        NameXpath.send_keys(self.username)
        PasswordXpath = self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[1]/form/table/tbody/tr[2]/td[2]/input")
        PasswordXpath.click()
        PasswordXpath.send_keys(self.password)
        self.driver.find_element_by_xpath("//*[@id='s1']/div/div[2]").click()
        print("login time: " + curr_time())
        self.driver.implicitly_wait(10)  # seconds

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        if soup.find('a', text=re.compile('continue')) != None:
            self.driver.find_element_by_partial_link_text('continue').click()
            self.driver.implicitly_wait(10)  # seconds

    def switch_to_main_city(self):
        while 'dorf2' not in self.driver.current_url:
            self.driver.find_element_by_id('n2').click()
            self.driver.implicitly_wait(10)

    def switch_to_resource(self):
        while 'dorf1' not in self.driver.current_url:
            self.driver.find_element_by_id('n1').click()
            self.driver.implicitly_wait(10)

    def close_browser(self):
        self.driver.quit()
        print('quit time: ' + curr_time())

    def warehouse(self):
        return int(self.driver.find_element_by_id('stockBarWarehouse').text.replace(',', ''))

    def granary(self):
        return int(self.driver.find_element_by_id('stockBarGranary').text.replace(',', ''))

    def lumber(self):
        return int(self.driver.find_element_by_id('l1').text.replace(',', ''))

    def clay(self):
        return int(self.driver.find_element_by_id('l2').text.replace(',', ''))

    def iron(self):
        return int(self.driver.find_element_by_id('l3').text.replace(',', ''))

    def wood(self):
        return int(self.driver.find_element_by_id('l4').text.replace(',', ''))

    def get_building_resource(self):
        self.driver.implicitly_wait(10)
        self.switch_to_resource()
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        area = soup.find_all('area')
        area.pop()
        list = []
        for i in area:
            list.append(int(i['alt'][-3:-1]))
        return list


    def enuf_resources(self):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        a = soup.find('div', class_='button-content', text='Exchange resources')
        if a == None:
            return True
        else:
            return False

    def busy(self):
        if self.clay() < 1000 or self.wood() < 1000 or self.iron() < 1000 or self.lumber() < 1000:
            return True
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        a = soup.find('div', class_='finishNow')
        if a == None:
            return False
        else:
            return True


    def get_building_main_city(self):
        if 'dorf2' not in self.driver.current_url:
            self.switch_to_main_city()
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        build_spot = soup.find_all('div', class_=re.compile('buildingSlot'))
        list = []
        for i in build_spot:
            lvl = soup.find('div', class_=re.compile(i['class'][1])).find('div', class_='labelLayer')
            if lvl is None:
                lvl = 0
            else:
                lvl = int(lvl.text)
            list.append((i['class'][2], lvl, int(i['class'][1][1:])))  # building type     lvl      spot
        return list


    def hero_adventure(self):  # run this code evey 5 min
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        hero_hp = soup.find('div', class_='bar')
        heroStatus = soup.find('div', class_='heroStatusMessage').text.strip()
        num_adventure = soup.find('button', class_='layoutButton adventureWhite green')
        if num_adventure.find('div', class_='speechBubbleContent') == None:
            return
        if int(hero_hp['style'][-4:-1].replace(' ', '').replace(':', '').replace('h', '')) < 10:
            return
        if heroStatus == 'on the way':
            return
        btn_hero = self.driver.find_element_by_css_selector('button.heroImageButton').click()
        self.driver.implicitly_wait(10)  # seconds
        self.driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[3]').click()
        self.driver.implicitly_wait(10)  # seconds
        self.driver.find_element_by_link_text('To the adventure.').click()
        self.driver.implicitly_wait(10)  # seconds
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        if soup.find('div', class_='heroStatusMessage header error') != None:
            return
        self.driver.find_element_by_xpath('//*[@id="start"]/div').click()
        self.driver.implicitly_wait(10)  # seconds
        self.driver.find_element_by_xpath('//*[@id="ok"]/div').click()
        self.driver.implicitly_wait(10)  # seconds
        print("hero adventure time: " + curr_time())
        sleep(random.randint(10, 20))

        #how many cities you have and return a number
    def count_city(self):
        i = 0
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        city_list = soup('a', href=re.compile('newdid'))
        for item in city_list:
            i = i + 1
        return i

    def current_city(self):
        i = 0
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        current_city_name = self.get_current_city_name()
        current_city = soup.find('div', class_='name', text=current_city_name)
        city_list = soup.find('div', id='sidebarBoxVillagelist').find_all('div', class_='name')
        for item in city_list:
            i = i + 1
            if item == current_city:
                return i


    def switch_to_next_city(self):
        if self.count_city() == 1:
            return
        curr = self.current_city()
        if curr == self.count_city():
            curr = 0
        print('move from  {}'.format(self.driver.find_element_by_id('villageNameField').text), end="")
        self.driver.find_element_by_xpath(
            '//*[@id="sidebarBoxVillagelist"]/div[2]/div[2]/ul/li[{}]/a/div'.format(curr + 1)).click()
        print(' to {}'.format(self.driver.find_element_by_id('villageNameField').text) + '   time: ' + curr_time())

    def get_capital(self):
        self.driver.find_element_by_class_name('profile').click()
        self.driver.implicitly_wait(10)  # seconds
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        capital = soup.find('span', text='(Capital)').parent
        return str(capital.a.string)

    def get_current_city_name(self):
        return self.driver.find_element_by_id('villageNameField').text

    def find_build_spot(self, build):  # get what to build and return int(the place to build,return>19)
        build_list = self.get_building_main_city()
        if build == constant.Rally_Point:
            return constant.Rally_Point_slot
        if build == constant.Main_Building:
            return constant.Main_Building_slot
        for i in build_list:
            if i[0] == build:
                return i[2]

    def build_task_main_city(self, to_build, lvl):  # gXX   # num
        self.switch_to_main_city()
        if self.busy():
            return True
        build_list = self.get_building_main_city()
        for i in build_list:
            if i[0] == to_build and lvl == i[1]:
                return True

        for i in build_list:
            if i[0] == to_build:
                if int(i[1]) < lvl:
                    # self.driver.find_element_by_xpath(
                    #    '//*[@id="village_map"]/div[{}]'.format(self.find_build_spot(to_build) - 18)).click()
                    self.driver.get(self.url + '/build.php?id={}&fastUP=0'.format(i[2]))
                    self.driver.implicitly_wait(10)  # seconds
                    soup = BeautifulSoup(self.driver.page_source, "html.parser")
                    a = soup.find('span', class_='none', text=re.compile('max level'))
                    if a != None:
                        return True
                    soup = BeautifulSoup(self.driver.page_source, "html.parser")
                    print('Upgrade {} to level {}   time:'.format(soup.find('h1', class_='titleInHeader').text,
                                                                  ##################################################
                                                                  int(i[1]) + 1) + curr_time())
                    self.driver.find_element_by_class_name('upgradeButtonsContainer').find_element_by_class_name(
                        'button-content').click()
                    return False
                else:
                    return True

        for i in build_list:
            if i[1] == 0:  # this is free space
                self.driver.get(self.url + '/build.php?id={}&fastUP=0'.format(i[2]))

                if to_build == constant.Granary or to_build == constant.Warehouse or to_build == constant.Marketplace or to_build == constant.Residence:
                    pass
                if to_build == constant.Barracks or to_build == constant.Palisade or to_build == constant.Rally_Point:
                    self.driver.find_element_by_xpath('//*[@id="build"]/div[1]/div[2]').click()

                if to_build == constant.Sawmill or to_build == constant.Brickyard or to_build == constant.Iron_Foundry or to_build == constant.Grain_Mill or to_build == constant.Bakery:
                    self.driver.find_element_by_xpath('//*[@id="build"]/div[1]/div[3]').click()

                print('new building, build : {} time: '.format(constant.from_gxx_to_name(to_build)) + curr_time())
                self.driver.find_element_by_id('contract_buildin{}'.format(to_build)).find_element_by_class_name(
                    'button-content').click()
                return False


    def train_troop(self, wood, clay, iron, lumber):
        if self.wood() < wood or self.clay() < clay or self.iron() < iron or self.lumber() < lumber:
            return True
        self.switch_to_main_city()
        build_list = self.get_building_main_city()
        for i in build_list:
            if i[0] == constant.Barracks and i[1] == 15:  # the lvl is higher then 15
                self.driver.get(self.url + '/build.php?id={}&fastUP=0'.format(i[2]))
                Phalanx = self.driver.find_element_by_xpath('//*[@id="build"]/form/div/div/div[2]/a').click()
                self.driver.find_element_by_xpath('//*[@id="s1"]/div/div[2]').click()
                return True
        return True


    def build_task_resorurce_all_to_lvl(self, max_lvl):
        self.switch_to_resource()
        build_list = self.get_building_resource()
        if self.busy():
            return True
        if min(build_list) < max_lvl:
            i = build_list.index(min(build_list))
            self.driver.find_element_by_xpath(
                '/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/map/area[{}]'.format(i + 1)).click()
            if not self.enuf_resources():
                self.driver.back()
                return
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            a = soup.find('span', class_='none', text=re.compile('max level'))
            if a != None:
                return True
            else:
                lvl = self.driver.find_element_by_xpath('//*[@id="content"]/h1/span').text
                lvl = int((lvl[-2:]).replace(':', '').replace(' ', '')) + 1
                print('Upgrade {} to level {}   time:'.format(
                    self.driver.find_element_by_xpath('//*[@id="content"]/h1').text, lvl) + curr_time())
                self.driver.find_element_by_xpath("//*[contains(text(),'Upgrade to level')]").click()
                return False
        else:
            return True


        #get wait timer and return a number the number of sec to wait
    def wait_timer_time(self):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        a = soup.find('div', class_='boxes buildingList')
        if a is None:
            return 0
        a = a.find('span', class_='timer')
        if a is None:
            return 0
        a = int(a['value'])
        if a > 0:
            return a
        else:
            return 0

