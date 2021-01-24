from selenium import webdriver
from time import sleep
from lxml import etree
from selenium.webdriver.common.keys import Keys

bro = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
#进入微博页面
bro.get('https://weibo.com/cctvxinwen?is_all=1')
sleep(15)

#登录
def login():
    ul = bro.find_element_by_class_name("gn_login_list")
    ul.find_element_by_xpath('./li[3]').click()
    sleep(3)
    userName_tag = bro.find_element_by_name('username')
    passWord_tag = bro.find_element_by_name('password')
    userName_tag.send_keys('13052871252')
    passWord_tag.send_keys('wenkai413')
    sleep(10)
    loginButton = bro.find_element_by_xpath('//div[@class="B_login form_login_register"]/div[6]')
    loginButton.click()#登入成功
    sleep(25)

def findTime(year, month):
    if year == 2020:
        yearButton = bro.find_elements_by_xpath('//li[@class="none"]')[1]
        solveClickProblem(yearButton)
        yearButton.click()
        sleep(5)
        monthButton = bro.find_elements_by_xpath('//div[@class="WB_timeline"]/ul/li[3]/ul')[12 - month]
        solveClickProblem(monthButton)
        monthButton.click()
    else:
        yearButton = bro.find_elements_by_xpath('//li[@class="none"]')[2]
        solveClickProblem(yearButton)
        yearButton.click()
        sleep(5)
        monthButton = bro.find_elements_by_xpath('//div[@class="WB_timeline"]/ul/li[3]/ul')[12 - month]
        solveClickProblem(monthButton)
        monthButton.click()

def scroll():
    for k in range(0, 4):
        bro.execute_script('scrollBy(0,10000)')
        sleep(7)

def solveClickProblem(element):
    bro.execute_script('arguments[0].scrollIntoView(true)', element)
    bro.execute_script('scrollBy(0,-100)')


def getComment(i,count):
    sleep(3)
    #加载出本页面所有的微博
    commentButton = bro.find_elements_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div')[i]
    text = commentButton.find_element_by_xpath('.//div[@class="WB_detail"]/div[4]').text
    #爬取跟新冠有关的微博
    if realNews(text):
        tmp = commentButton.find_element_by_xpath('.//ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]')
        comment = tmp.find_element_by_xpath('./li[3]')
        # 把要点击的放到能点到的地方没有障碍物
        solveClickProblem(comment)
        # 点击
        comment.click()
        sleep(3)
        newsPage = bro.find_elements_by_class_name('list_box')[count]
        flag = 0
        mistake = 0
        while flag == 0:
            try:
                newsPage = bro.find_elements_by_class_name('list_box')[count]
                a = newsPage.find_element_by_xpath('./div/a')
                url1 = a.get_attribute('href')
                with open('./' + 'sorce' + '.txt', 'a+', encoding='utf-8') as fp:
                    fp.write(url1 + '   ')
                print(url1)
                flag = 1
            except:
                print("评论错误修正")
                comment.click()
                sleep(3)
                comment.click()
                sleep(4)
                flag = 0
                mistake = mistake + 1
                if mistake > 5:
                    print("错误次数太多，跳过")
                    flag = 1
        return 1
    return 0

def realNews(text):
    lst = ['新冠', '肺炎', '疫情', '病例', '核酸', '隔离', '新型冠状']
    res = 0
    for item in lst:
        if item in text:
            res = 1
            break
    return res

def getNextPage():
    flag = 0
    while flag == 0:
        try:
            sleep(3)
            next = bro.find_elements_by_xpath('//div[@class="W_pages"]/a')
            length = len(next)
            solveClickProblem(next[length - 1])
            next[length - 1].click()
            sleep(6)
            flag = 1
        except:
            print("翻页错误修正")
            bro.refresh()
            sleep(10)
            scroll()
            flag = 0

def calculatePages():
    return len(bro.find_elements_by_xpath('//div[@class="WB_cardwrap S_bg2"]/div/span/div/ul/li'))


def storeContent(url):
    count1 = count2 = count3 = count4 = 0  # 用于统计新闻个数
    #传进来的是列表
    for site in url:
        bro.get(site)
        sleep(5)
        scroll()
        timeText = bro.find_element_by_xpath('//div[@class="WB_detail"]/div[2]/a').text
        timeText = timeText.split(' ')[0]
        year = int(timeText.split('-')[0])
        month = int(timeText.split('-')[1])
        date = int(timeText.split('-')[2])
        flag = 0
        if (year == 2019) or (month == 1 and date <= 22):
            name = '2019.12.8 ~ 2020.1.22新闻及其评论'
            count1 = count1 + 1
            flag = 0
        if (month == 1 and date >= 23) or (month == 2 and date <= 7):
            name = '2020.1.23 ~ 2020.2.7新闻及其评论'
            count2 = count2 + 1
            flag = 1
        if (month == 2 and date >=8) or (month == 2 and date <= 13):
            name = '2020.2.8 ~ 2020.2.13新闻及其评论'
            count3 = count3 + 1
            flag = 2
        if(month == 2 and date >= 14) or (month >= 3):
            name = '2020.2.14 ~ 2020.6.30新闻及其评论'
            count4 = count4 + 1
            flag = 3
        with open('./' + name + '.txt' , 'a+', encoding='utf-8') as fp:
            if flag == 0:
                fp.write('******' + str(count1) + " ")
            if flag == 1:
                fp.write('******' + str(count2) + " ")
            if flag == 2:
                fp.write('******' + str(count3) + " ")
            if flag == 3:
                fp.write('******' + str(count4) + " ")
            fp.write('**时间**' + timeText)
            newsText = bro.find_element_by_xpath('//div[@class="WB_detail"]/div[4]').text
            commentList = bro.find_elements_by_xpath('//div[@class="list_box"]/div/div')
            k = 1 #用于评论的计数
            fp.write(newsText + "**评论区**")
            for item in commentList:
                commentText = str(item.find_element_by_xpath('./div[2]/div[1]').text)
                commentText = commentText.split("：")[1]
                if commentText != "":
                    fp.write("*评论*" + str(k) + ": " + commentText + " ")
                    k = k + 1
            fp.write('\n' + '\n')

def adjust(pageNum, pageSize):
    next = bro.find_elements_by_xpath('//div[@class="W_pages"]/span/div/ul/li')
    next[pageSize - pageNum].click()
    return pageNum

if __name__ == '__main__':
    login()
    for year in range(2020, 2018, -1):
        for month in range(1, 0, -1):
            findTime(year=year, month=month)
            scroll()
            pageSize = calculatePages()#计算某月新闻个数
            p = 1
            if month == 1:
                bro.get("https://weibo.com/cctvxinwen?is_all=1&stat_date=202001&page=29#1611323936863")
                sleep(8)
                p = 11
            for page in range(p, pageSize + 1):
                print('正在爬取' + str(year) + '年' + str(month) + '月的微博')
                # 第一页已经加载完了全部微博，所以不用滚动
                if page > 1:
                    scroll()
                #计算一页的微博总数
                NewsSize = len(bro.find_elements_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div')) - 2
                #最后一页多了一个div标签
                if page == pageSize:
                    NewsSize = NewsSize - 1
                #爬取该页所有微博
                count = 0
                for i in range(1, NewsSize + 1):
                    if getComment(i, count):
                        count = count + 1
                if page < pageSize:
                    getNextPage() #最后一页不用翻
