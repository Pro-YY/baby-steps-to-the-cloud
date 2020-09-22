# -*- coding: utf-8 -*-
from scrapyspider.items import MicroInfoItem

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

import scrapy


class MicrosoftSpider(scrapy.Spider):
    name = 'microsoft'
    allowed_domains = ['https://www.levels.fyi']
    start_urls = [
                  'https://www.levels.fyi/comp.html?track=Software%20Engineer&search=Microsoft',
                ]
    custom_settings = {
        'ITEM_PIPELINES': {'scrapyspider.pipelines.InsertMicroInfoDBPipeline': 400},
    }
    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1920)

    def parse(self, response, **kwargs):
        self.driver.get(response.url)
        for i in range(213):
            wait = WebDriverWait(self.driver, 5)
            wait.until(
                lambda driver: driver.find_element_by_xpath('//*[@id="compTable"]/tbody/tr[1]'))  # 等待内容加载完成

            tr_list = self.driver.find_elements_by_xpath('//*[@id="compTable"]/tbody/tr')  # 每一行信息
            for tr in tr_list:
                item = MicroInfoItem()
                try:
                    company = tr.find_element_by_css_selector('td:nth-child(2) span:nth-child(1) a').text
                except:
                    company = tr.find_element_by_css_selector('td:nth-child(2) span:nth-child(1)').text
                location_date = tr.find_element_by_css_selector('td:nth-child(2) span.dateDetails').text
                level_name = tr.find_element_by_css_selector('td:nth-child(3) span:nth-child(1)').text
                try:
                    tag = tr.find_element_by_css_selector('td:nth-child(3) > span.dateDetails > a').text
                except:
                    tag = tr.find_element_by_css_selector('td:nth-child(3) > span.dateDetails').text
                total_compensation = tr.find_element_by_css_selector('td:nth-child(5) span:nth-child(1)').text
                try:
                    base_stock_bonus = tr.find_element_by_css_selector('td:nth-child(5) span.dateDetails').text
                except:
                    base_stock_bonus = '0K|0K|0K'

                tr.click()
                years_at_company = self.driver.find_element_by_css_selector('#compTable > tbody > tr.detail-view > td > div > div > div:nth-child(3) > div > p:nth-child(2) > span').text
                years_of_experience = self.driver.find_element_by_css_selector('#compTable > tbody > tr.detail-view > td > div > div > div:nth-child(4) > div > p:nth-child(2) > span').text
                tr.click()

                item['company'] = company
                item['location'] = location_date.split("|")[0]
                item['company_date'] = location_date.split("|")[1]
                item['level_name'] = level_name
                item['tag'] = tag
                item['total_compensation'] = total_compensation
                item['base'] = base_stock_bonus.split("|")[0]
                item['stock'] = base_stock_bonus.split("|")[1]
                item['bonus'] = base_stock_bonus.split("|")[2]
                item['years_at_company'] = years_at_company
                item['years_of_experience'] = years_of_experience
                yield item

            wait = WebDriverWait(self.driver, 1)
            wait.until(lambda driver: driver.find_element_by_css_selector('li.page-item.page-next'))  # 等待内容加载完成
            next_page = self.driver.find_element_by_css_selector('li.page-item.page-next a')
            next_page.click()  # 模拟点击下一页














