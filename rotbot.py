from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time
import praw
import schedule


wait = None
driver = None

def connect():
	global driver, wait
	driver = webdriver.Chrome('chromedriver') 
	driver.get("https://web.whatsapp.com/") 
	wait = WebDriverWait(driver, 600)	

def sendpost(text):
	global driver, wait
	target = '"Anand"'
	x_arg = '//span[contains(@title,' + target + ')]'
	#wait = WebDriverWait(driver, 600)
	group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg))) 
	group_title.click() 
	message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
	for i in text: 
		message.send_keys(i) 
		message.send_keys(Keys.SHIFT,'\n')
	message.send_keys(Keys.ENTER)
	time.sleep(1)


def getpost():
	flag = 0
	try:
		reddit = praw.Reddit(client_id='709OPWc2DWekhQ', client_secret='rEijkVKS_7rW7Cb6Q-7oSs4XOCs', user_agent='ikoojoshi')
		top_posts = reddit.subreddit('todayilearned').new(limit=1)
		text = ""
		flag = 1
		for post in top_posts:
			title = post.title
			text = [title, "", "- RotBot, powered by Python and Reddit"]
	except:
		print("error")
	if flag == 0:
		print("Unable to access Reddit")
		time.sleep(10)
		text = getpost()
	return text

def post():
	text = getpost()
	sendpost(text)
	
def scheduler():
	while True:
		schedule.run_pending()
		time.sleep(1)
			
def main():
	connect()
	schedule.every().day.at("13:54").do(post)
	scheduler()

if __name__ == "__main__":
	main()