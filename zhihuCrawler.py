from selenium import webdriver
import time
import urllib.request
from bs4 import BeautifulSoup
import html.parser
import os


def expand_times(driver,times):
	for i in range(int(times)):
		#scroll to the bottom of the page
		driver.execute_script("window.scrollTo(0,document.body.scrollHeight);") 
		time.sleep(3) #wait for the page to be loaded
		try:
			driver.find_element_by_css_selector('button.QuestionMainAction').click()
			print('page'+str(i))
			time.sleep(1)
		except:
			break


def main(url,expandTime,folder):
	driver = webdriver.Chrome() #open the web browser
	
	#get url you want to scrap
	driver.get(url)

	expand_times(driver,expandTime)
	
	result_rawPage = driver.page_source
	result_soupObj = BeautifulSoup(result_rawPage, 'html.parser')
	result_bf = result_soupObj.prettify() #structurize the raw html page
	
	with open("./output/rawPage/raw_result.txt",'w') as f:
		f.write(result_bf)
	print("Store raw html data successfully!")
	
	with open('./output/rawPage/noscript_metadata.txt','w') as f:
		noscript_nodes = result_soupObj.find_all('noscript')
		noscript_inner_all = ""
		for noscript in noscript_nodes:
			noscript_inner = noscript.get_text()
			noscript_inner_all += noscript_inner + "\n"
		noscript_all = html.parser.unescape(noscript_inner_all)
		f.write(noscript_all)
		
	print("Successfully store noscript meta data!")

	img_soup = BeautifulSoup(noscript_all,'html.parser')
	img_nodes = img_soup.find_all('img')

	folderPath = "./output/images/"+folder
	if not os.path.exists(folder):
		os.makedirs(folderPath)

	with open('./output/rawPage/img_metadata.txt','w') as f:
		count = 0
		for img in img_nodes:
			if img.get('src') is not None:
				imgUrl = img.get('src')
				oneLine = str(count)+"\t"+imgUrl+"\n"
				f.write(oneLine)
				urllib.request.urlretrieve(imgUrl, folderPath+"/"+str(count)+".jpg")
				count += 1
	print("ImgUrl stored and pictures successfully stored!")


if __name__ == '__main__':
	urlToScrape = input("Enter the url you want to scrape on Zhihu -->")
	numberToExpand = input("Enter the number of pages you want to expand -->")
	folderToStore = input("Enter the folder name for images to store -->")
	main(urlToScrape,numberToExpand,folderToStore)