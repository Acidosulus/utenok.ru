import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
from my_library import *
import colorama
from colorama import Fore, Back, Style
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser
from bs4 import BeautifulSoup as BS
from lxml import html
import requests
from click import echo, style
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import uuid

class WD:
	def init(self):
		#self.site_url = 'https://utenok.ru/'
		self.site_url = 'http://saas_87809_pfthxiqmxg_utenock.u.on-advantshop.net/'
		config = configparser.ConfigParser()


		
	def __init__(self):
		self.init()
		if False:
			chrome_options = webdriver.ChromeOptions()
			chrome_prefs = {}
			chrome_options.experimental_options["prefs"] = chrome_prefs
			chrome_options.add_argument('--disable-gpu')
			chrome_options.add_argument("--disable-notifications")
			#chrome_options.add_argument('--headless')
			self.driver = webdriver.Chrome(options=chrome_options)
			self.driver.maximize_window()

	def __del__(self):
		try:
			self.driver.quit()
		except: pass

	def Get_HTML(self, curl):
		if False:
			if os.path.isfile('response.html'):
					echo(style('Загружен локальный файл: ', fg='bright_red') + style('response.html', fg='red'))
					self.page_source = file_to_str('response.html')
			else:
				r = requests.get(curl)
				self.page_source = r.text
				str_to_file('response.html', self.page_source)
		else:
			#r = requests.get(curl, headers={'User-Agent': UserAgent().chrome})
			r = requests.get(curl)
			self.page_source = r.text
			echo(style(text='Downloaded: ', fg='cyan')+style(text=len(self.page_source), fg='green'))
			#str_to_file(file_path="response.html", st = r.text)
			#self.driver.get(curl)
			#self.page_source = self.driver.page_source
			#return self.page_source
		return self.page_source

	def Get_List_Of_Links_On_Goods_From_Catalog(self, pc_link:str) -> list:
		echo(style('Список товаров каталога: ', fg='bright_yellow') + style(pc_link, fg='bright_white'))
		ll_catalog_items = []
		ll_catalog_pages_list = self.Get_List_of_Catalog_Pages(pc_link)
		for catalog_page in ll_catalog_pages_list:
			echo(style('Список товаров каталога: ', fg='bright_yellow') + style(pc_link, fg='bright_white') + '    ' + style('Страница: ', fg='bright_cyan') +style(catalog_page, fg='bright_green'))
			self.Get_HTML(catalog_page)
			soup = BS(self.page_source, features='html5lib')
			elements = soup.find_all('a',{'class':'products-view-name-link'})
			for ln_counter, element in enumerate(elements):
				print(f"{ln_counter}  {element['href']}")
				append_if_not_exists(element['href'], ll_catalog_items)
		print(len(ll_catalog_items))
		return ll_catalog_items

	
	def Get_List_of_Catalog_Pages(self, pc_href:str) -> list:
		ll = []
		lc_result = pc_href
		while len(lc_result)>0:
			echo(style('Список страниц каталога:', fg='bright_yellow') + '  ' + style(lc_result, fg='bright_cyan'))
			append_if_not_exists(lc_result, ll)
			lc_result = self.Get_link_on_the_next_catalog_page(lc_result)
		return ll
		

	def Get_link_on_the_next_catalog_page(self, lc_link:str) -> str:
		self.Get_HTML(lc_link)
		soup = BS(self.page_source, features='html5lib')
		"""
		if page source contented text 'pagenumberer-next' it have the next page, in other cases it's the last catalog page
		"""
		if self.page_source.count('pagenumberer-next')==0: # page without link on the next page
			return ''
		else: # the page have link on next page
			soup = BS(self.page_source, features='html5lib')
			link = soup.find('a',{'class':'pagenumberer-next'})
			lc_next_link = (self.site_url if len(link['href'])>0 else '') + link['href']
			return lc_next_link
		
	

		
	def Write_To_File(self, cfilename):
		file = open(cfilename, "w", encoding='utf-8')
		file.write(self.page_source)
		file.close()


def Login():
	return WD()

if False:
	colorama.init()
	wd = Login()
	print(wd.Get_List_Of_Links_On_Goods_From_Catalog('https://utenok.ru/categories/dzhemperi-dlya-devochek'))
