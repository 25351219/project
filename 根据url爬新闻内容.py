from selenium import webdriver
from time import sleep
from lxml import etree
from selenium.webdriver.common.keys import Keys

bro = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
#进入微博页面

def solveClickProblem(element):
    bro.execute_script('arguments[0].scrollIntoView(true)', element)
    bro.execute_script('scrollBy(0,-250)')

def scroll():
    for k in range(0, 4):
        bro.execute_script('scrollBy(0,10000)')
        sleep(1.618)

def storeContent(url):
    count1 = count2 = count3 = count4 = 0  # 用于统计新闻个数
    count4 = 910
    #传进来的是列表
    for site in url:
        site = site.strip()#去除网址左右两边多余空格
        try:
            bro.get(site)
            sleep(4)
            check = len(bro.find_elements_by_xpath('//div[@class="list_ul"]/div'))
            mistakeNum = 0
            while check < 2:
                print('解决评论不出现问题')
                mistakeNum = mistakeNum + 1
                button = bro.find_element_by_xpath('//li[@class=" curr"]/a/span/span/span')
                solveClickProblem(button)
                button.click()
                sleep(2.5)
                check = len(bro.find_elements_by_xpath('//div[@class="list_ul"]/div'))
                if mistakeNum > 8:
                    print("错误次数太多，你还让我怎么爬？草。")
                    break
            scroll()
            timeText = bro.find_element_by_xpath('//div[@class="WB_detail"]/div[2]/a').text
            timeText = timeText.split(' ')[0]
            year = int(timeText.split('-')[0])
            month = int(timeText.split('-')[1])
            date = int(timeText.split('-')[2])
            commentNum = bro.find_element_by_xpath('//li[@class=" curr"]/a/span/span/span').text
            print('正在爬取' + str(year) + '年' + str(month) + '月' + str(date) + '日的新闻内容')
            flag = 0
            if (year == 2019) or (month == 1 and date <= 22):
                name = '2019.12.8 ~ 2020.1.22新闻及其评论'
                count1 = count1 + 1
                flag = 0
            if (month == 1 and date >= 23) or (month == 2 and date <= 7 ):
                name = '2020.1.23 ~ 2020.2.7新闻及其评论'
                count2 = count2 + 1
                flag = 1
            if (month == 2 and date >=8) and (month == 2 and date <= 13):
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
                fp.write("**评论量***" + commentNum)#记录评论量
        except:
            print('网址错误')
            pass


if __name__ == '__main__':
    with open('../seleniun爬虫/sorce.txt', "r", encoding='utf-8') as fo:
        urlSource = fo.read()
        urlList = urlSource.split("   ")
        storeContent(urlList)