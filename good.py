from queue import Empty
from my_library import *
from driver import *
import colorama
from colorama import Fore, Back, Style
from urllib.parse import quote
from bs4 import BeautifulSoup as BS
from click import echo, style

def poiskpers(url):
	geourl = '{0}'.format(quote(url))
	return geourl

class Good:
	def __init__(self, ol:WD, pc_good_link, pc_price:str):
		pc_good_link = pc_good_link.replace(r'amp;', '')
		self.pictures = []
		self.sizes = []
		self.prices = []
		self.color = ''
		self.colors = []
		self.article = ''
		self.name = ''
		self.description= ''
		self.price = 0
		self.brand = ''
		echo(style('Товар: ', fg='bright_yellow') + style(pc_good_link, fg='bright_white') + style('  Прайс:', fg='bright_cyan') + style(pc_price, fg='bright_green'))

		ol.Get_HTML(pc_good_link)
		soup = BS(ol.page_source, features='html5lib')


		

		self.article = soup.find('div',{'class':'details-param-value inplace-offset'}).text
		self.name = soup.find('h1').text.strip()
		self.description = soup.find('div',{'class':'tabs-content'}).text
		if 'Скачать каталоги' in self.description:
			self.description = sx('|' + self.description, '|', 'Скачать каталоги')

		self.description = self.description + ' ' + soup.find('div', {'class':'details-tabs-properties'}).text
		self.description = prepare_str(self.description)

		pictures = soup.find_all('div',{'class':'details-carousel-item-vertical'})
		for picture in pictures:
			lc = sx(  str(picture).replace(' ',''),  "'originalPath':'", "'")
			append_if_not_exists(lc, self.pictures)
		
		
		self.price = soup.find('div', {'class':'price-number'}).text.strip()
		#str_to_file('price.txt', self.price)

		lc_source = (ol.page_source).replace(chr(13),'').replace(chr(9),' ').replace(chr(10),'').replace(chr(12),'')
		#str_to_file('source.html', lc_source )
		lc = sx( lc_source, f'<div class="price-current cs-t-1"><div class="price-number">  {self.price}</div> <div class="price-currency"> руб.</div></div>                    </div>                </div>            </div>', '<div class="products-view-block cs-br-1 js-products-view-block"')
		if len(lc)==0:
			lc = sx( lc_source, f'<div class="price-current cs-t-1"><div class="price-number"> {self.price}</div> <div class="price-currency"> руб.</div></div>                    </div>                </div>            </div>', '<div class="products-view-block cs-br-1 js-products-view-block"')
		for i in range(lc.count('<div class="block-size-product">')):
			lc_size = sx( lc, '<div class="block-size-product">', '</div>', i+1)
			append_if_not_exists(lc_size, self.sizes)

		self.color = sx(lc_source, '&quot;ColorName&quot;:&quot;','&')
		
		self.price = self.price.replace(' ','')
		return

		print()
		lc = replace_decorators(sx( ol.page_source, 'data-sizes="::[', ']"' ))
		str_to_file('json.json', lc)
		print()
		return
		sizes =soup.find_all('div', {'class':'sizes-viewer-block'})
		print(len(sizes))
		for size in sizes:
			if not 'sizes-viewer-item-disabled' in str(size):
				print(size.text)
		
		return
		#for i in range(ol.page_source.count('<option value="')):
		#	lc_size = sx(ol.page_source, '<option value="', '"', i+1)
		#	if len(lc_size)>0:
		#		append_if_not_exists(lc_size, self.sizes)

		
		sizes = soup.find('select',{'id':'pa_rost'})
		if sizes!=None:
			sizes=sizes.find_all('option')
			for size in sizes:
				lc_size = size.text
				if lc_size!='Выбрать опцию':
					append_if_not_exists(lc_size, self.sizes)
		else:
			self.sizes=['*']

		colors = soup.find('select',{'id':'pa_color'})
		if colors!=None:
			colors = colors.find_all('option')
			for color in colors:
				lc_color = color.text
				if lc_color!='Выбрать опцию':
					append_if_not_exists(lc_color, self.colors)

		self.description = soup.find('div',{'class':'woocommerce-Tabs-panel woocommerce-Tabs-panel--description panel entry-content wc-tab'}).text.strip()

		if not '–' in self.price:
			for size in self.sizes:
				self.prices.append(self.price)
		else:
			print()
			print()
			self.sizes=[]
			lc_description_source = self.description.replace('\nРасцветки в ассортименте','').replace(' — ','-').replace(' по ','-').replace('руб\n','руб.\n')
			if 'Расцветки:' in lc_description_source:
				lc_description_source = lc_description_source[0:lc_description_source.find('Расцветки:')]
			if 'Цвет:' in lc_description_source:
				lc_description_source = lc_description_source[0:lc_description_source.find('Цвет:')]
			print(f'Источник размеров:{lc_description_source}')
			print()
			lc = sx(lc_description_source+'|', 'Размеры:','|')
			lc = lc.replace('Размеры:','').strip()
			ll_source = lc.split('\n')
			print(f'll_source:{ll_source}')
			print()
			
			for lc in ll_source:
				print()
				print()
				print()
				print(f'lc:{lc}')
				ll_r_str = ''.join(reversed(lc))
				lc_price = ''.join(reversed(sx(ll_r_str, '.бур ', '-')))
				lc = lc.replace(f'-{lc_price} руб.','')
				print(f'lc: {lc}    => price: {lc_price}')
				for size in lc.split(','):
					if len(size)>0 and len(lc_price)>0:
						self.sizes.append(size)
						self.prices.append(lc_price)
			if len(self.sizes)==0:
				self.sizes=['*']
			print()
			print()


