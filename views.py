from django.shortcuts import render,redirect

from django.http import HttpResponse
from jouIF.models import Professor,Journal,Impactfactor,Scholar
from .forms import PostForm

#from song2 import findJournal


def index(request):
	return HttpResponse("Hello, world. You're at the polls index.")
	
def DisplayBase(request):
	#print(request.method)
	
	if request.method=="POST":
		form = PostForm(request.POST)
		
		#print('form.is_valid()',form.is_valid())
		
		if form.is_valid():
			pname=form.cleaned_data['pName']
			sname=str(form.cleaned_data['sName'])
			
			chkbox1=request.POST.get("chkbox1",'')
			chkbox2=request.POST.get("chkbox2",'')
			
			#print('professor name : ',pname)
			#print('scholar name : ',sname)

			#print('checkbox1 :',len(request.POST.get("chkbox1",'')), request.POST.get("chkbox1",'')=='')
			#print('checkbox2 :',len(request.POST.get("chkbox2",'')), request.POST.get("chkbox2",'')=='')
			
			searchFlag=4 # 0 :교수 이름 검색 결과 없음, 1: 논문 이름 검색 결과 없음, 2: 교수 이름 검색 결과 완료, 3: 논문 이름 검색 완료
			searchWord={'pName':pname,'sName':sname}
			resultSet=[]
			if (chkbox1=='' and chkbox2=='on') or (sname==''): # mean second form click -> search only with professor name
				check=Professor.objects.filter(professor_name=pname).count()
				if check!=0:
					searchFlag=2
					pr_result = Professor.objects.filter(professor_name=pname)[0]
					
					pid=pr_result.professor_id #교수id
					#교수 이름으로 검색
					scho_list = Scholar.objects.filter(professor_id=pid)
					
					for scho in scho_list:
						jouRes=Journal.objects.filter(scholar=scho.scholar_id)[0]
						ifRES=Impactfactor.objects.filter(journal=jouRes.journal_id)[0]
						#result_temp = "scholar {0}; journal {1}; Impactfactor: {2}; \n".format(str(scho.scholar_name),str(jouRes.journal_name),str(ifRES.impactfactor_value))
						result_temp ={'sname':scho.scholar_name,'jname':jouRes.journal_name,'year':jouRes.year,'if':str(ifRES.impactfactor_value)}
						resultSet.append(result_temp)
				else :
					resultSet.append([])
					searchFlag=0
					
			elif(chkbox1=='on' and chkbox2=='') or (pname==''): 
				check=Scholar.objects.filter(scholar_name=sname).count()
				if check!=0:
					searchFlag=3
					sid=Scholar.objects.filter(scholar_name=sname)[0]
					jouRes=Journal.objects.filter(scholar=sid.scholar_id)[0]
					ifRES=Impactfactor.objects.filter(journal=jouRes.journal_id)[0]
					#result_temp = "scholar {0}; journal {1}; Impactfactor: {2}; \n".format(str(scho.scholar_name),str(jouRes.journal_name),str(ifRES.impactfactor_value))
					result_temp ={'sname':sname,'jname':jouRes.journal_name,'year':jouRes.year,'if':str(ifRES.impactfactor_value)}
					resultSet.append(result_temp)
					
				else :
					rsDict=findJournal(sname)
					result_temp ={'sname':rsDict['find'],'jname':rsDict['jname'],'year':rsDict['jyear'],'if':rsDict['impactfactor']}
					resultSet.append(result_temp)
					searchFlag=1
				
			else :
				resultSet.append([])
			#searchResult={'sr':searchFlag}
			return render(request, 'jouIF/searchTest.html', {'searchResult':searchFlag,'searchWord':searchWord, 'resultSet': resultSet })
	else :
		form = PostForm()
		return render(request, 'jouIF/base.html',{'form':form})

def findJournal(input_str):
	from urllib.parse import urlencode, quote_plus
	import requests
	from urllib.parse import urlparse
	from bs4 import BeautifulSoup
	from selenium import webdriver
	from selenium.webdriver.common.keys import Keys
	import time
	import re
	import sqlite3
	
	lines=[input_str]
	
	t=0

	for line in lines:
		scholar=line
		jyear=1
		jname='a'
		sssoup='find'
		impactfactor='0'
		t=t+1
		if(t%3==0):
			time.sleep(0.1)
			
		# riss  
		try:
		
			options=webdriver.ChromeOptions()
			options.add_argument('headless')
			options.add_argument('window-size=1920x1080')
			options.add_argument("--disable-gpu")
			options.add_argument("--no-sandbox")

			driver=webdriver.Chrome('/Users/song/Downloads/chromedriver',chrome_options=options)
			driver.implicitly_wait(1)
			url2='http://www.riss.kr/index.do'
			driver.get(url2)   

			driver.find_element_by_xpath('//*[@id="normal"]/fieldset/div[2]/p/label[3]').click()        
			driver.find_element_by_xpath('//*[@id="basicQuery"]').click()
			for s in scholar:
				driver.find_element_by_xpath('//*[@id="basicQuery"]').send_keys(s)
				time.sleep(0.1)
				
			try:
				driver.find_element_by_xpath('//*[@id="normal"]/fieldset/div[1]/input[2]').click()
			except:
				pass

			if(t%5==0):
				time.sleep(0.1)
			
			time.sleep(0.1)
			source_r=driver.page_source
			soup_r=BeautifulSoup(source_r,'html.parser')

			soups_r=soup_r.find("p",class_="txt")
			soups_r2=soups_r.find("a")
			soups_r9=soups_r2.text
			soups_r3=soups_r2.get("href")
			urlr='http://www.riss.kr'+soups_r3
			
			#jyear 찾기
			soups_r4=driver.find_element_by_xpath('//*[@id="level4_mainContent"]/form/div[3]/div[2]/div/div[2]/ul/li/div[1]/span[2]')
			soups_r5=soups_r4.text
			soups_r10=soups_r5.split(',')
			soups_r11=soups_r10[-1]
			soups_r6=int(re.findall('\d+',soups_r11)[0])
			
			driver.quit()
			
			options=webdriver.ChromeOptions()
			options.add_argument('headless')
			options.add_argument('window-size=1920x1080')
			options.add_argument("--disable-gpu")
			options.add_argument("--no-sandbox")
			
			driver=webdriver.Chrome('/Users/song/Downloads/chromedriver',chrome_options=options)        
			driver.implicitly_wait(1)
			driver.get(urlr)

			#jname 찾기
			soups_r7=driver.find_element_by_xpath('//*[@id="level4_mainContent"]/div/div[3]/ul/li[3]/p/a')
			soups_r8=soups_r7.text
			
			if jname=='a':
				jname=soups_r8
				sssoup=soups_r9
				#print("jname=",jname)
				
			if jyear==1:
				jyear=soups_r6
				#print("jyear=",jyear)
			driver.quit()
		except:
			pass
		
		

		#google scholar
		if jname=='a' and jyear==1:
			try:
				
				options=webdriver.ChromeOptions()
				options.add_argument('headless')
				options.add_argument('window-size=1920x1080')
				options.add_argument("--disable-gpu")
				options.add_argument("--no-sandbox")
				
				driver=webdriver.Chrome('/Users/song/Downloads/chromedriver',chrome_options=options)
				driver.implicitly_wait(1)

				url='https://scholar.google.co.kr/'
				driver.get(url)

				if(t%3==0):
					time.sleep(0.5)
				
				#검색창에 입력
				for s in scholar:
					driver.find_element_by_xpath('//*[@id="gs_hdr_tsi"]').send_keys(s)
					time.sleep(0.1)

				driver.implicitly_wait(0.5)
				
				#검색버튼 누르기
				driver.find_element_by_xpath('//*[@id="gs_hdr_tsb"]').click()
				
				source=driver.page_source
				soup=BeautifulSoup(source,'html.parser')
				ssoup=soup.find("h3",class_="gs_rt").find("a")

				sssoup=ssoup.text


				if(len(scholar)>len(sssoup)):
					l=len(scholar)-len(sssoup)
				else:
					l=len(sssoup)-len(scholar)

				#scholar jname, jyear 찾기

				soups=soup.find("div",class_="gs_a")
				soups2=soups.text.split("-")
				soups3=soups2[1]
				soups4=soups3.split(",")

				if len(soups4)==2:
					if (len(soups4[1].strip())<5) and (l<10):
						jname=soups4[0].strip('…').strip()
						jyear=soups4[1].strip()
						#print("jname=",jname)
						#print("jyear=",jyear)
					else:
						jname=soups4[0].strip('…').strip()+' '+soups4[1].strip()

				soups5=soup.find("a",class_="gs_or_nvi")
				soups6=soups5.get("href")
				urls=soups6
				driver.quit()
			except:
				pass
			
			
		
		#scholar2
			try:
				options=webdriver.ChromeOptions()
				options.add_argument('headless')
				options.add_argument('window-size=1920x1080')
				options.add_argument("--disable-gpu")
				options.add_argument("--no-sandbox")
				
				driver=webdriver.Chrome('/Users/song/Downloads/chromedriver',chrome_options=options)
				driver.implicitly_wait(0.5)
				
				if(t%8==0):
					time.sleep(0.5)
				driver.get(urls)
				
				jname2=driver.find_element_by_xpath('/html/body/div[2]/font[2]/span/div/nobr')
				jname2=jname2.text
				if len(jname2)>len(jname):
					jname=jname2
					#print("jname=",jname)
					#print("jyear=",jyear)
				driver.quit()
			except:
				pass

			#driver.quit()
	   
		#JCR
		
		options=webdriver.ChromeOptions()
		options.add_argument('headless')
		options.add_argument('window-size=1920x1080')
		options.add_argument("--disable-gpu")
		options.add_argument("--no-sandbox")
			
		driver=webdriver.Chrome('/Users/song/Downloads/chromedriver',chrome_options=options)
		driver.implicitly_wait(0.5)

		url3='https://error.incites.thomsonreuters.com/error/Error?DestApp=IC2JCR&Error=IPValid&Params=IPStatus%3DIPValid%26DestApp%3DIC2JCR&RouterURL=https%3A%2F%2Flogin.incites.thomsonreuters.com%2F&Domain=.thomsonreuters.com&Src=IP&Alias=IC2'
		driver.get(url3)

				
		driver.find_element_by_xpath('//*[@id="username"]').send_keys('soaka94@sju.ac.kr')
		driver.find_element_by_xpath('//*[@id="password"]').send_keys('@ailab123456789')
		driver.find_element_by_xpath('/html/body/div/div[1]/div[3]/div[1]/div/div/div/form/button').click()
		time.sleep(3)
				
		#select journal 선택
		driver.find_element_by_xpath('//*[@id="ext-gen1018"]/div[1]/div[2]/div[4]/div[4]/a[1]/button').click()
		driver.find_element_by_xpath('//*[@id="skip-to-content"]/div/div[2]/div[1]/div[1]/div[4]/i').click()
				
		#journal명 입력
		for j in jname:
			driver.find_element_by_xpath('//*[@id="journalSearch-inputEl"]').send_keys(j)
			time.sleep(0.1)
				
		time.sleep(2)
		driver.find_element_by_xpath('//*[@id="journalSearch-inputEl"]').send_keys(Keys.ENTER)
				
		#select yeat 선택
		driver.find_element_by_xpath('//*[@id="ext-gen1097"]').click()
				
		#년도 리스트 받아오기
		source_new=driver.page_source
		soup_new=BeautifulSoup(source_new,'html.parser')
		soups_new=soup_new.find_all("li",class_='x-boundlist-item')

		s_list=[]

		for s in soups_new:
			s_list.append(s.text)
					
		jyear=str(jyear)
				
		#리스트에서 일치하는 년도 찾아서 선택하기
		for i in s_list:
			if i==jyear:
				jyear=int(jyear)
				jy=2018-jyear
				jy=str(jy)
				#xpath가 바뀔 수도 있어서
				try:
					driver.find_element_by_xpath('//*[@id="boundlist-1171-listEl"]/ul/li[' +jy+ ']').click()
				except:
					pass
				try:
					driver.find_element_by_xpath('//*[@id="boundlist-1169-listEl"]/ul/li[' +jy+ ']').click()
				except:
					pass
				driver.find_element_by_xpath('//*[@id="skip-to-content"]/div/div[2]/div[1]/div[9]/div[3]/a[2]').click()
				
		time.sleep(0.5)        
		source_j=driver.page_source
		soup_j=BeautifulSoup(source_j,'html.parser')
		soups_j=soup_j.find_all("div",class_='x-grid-cell-inner')
				
		jname=jname.upper()

		j_list=[]
				
		for j in soups_j:
			j_list.append(j.text)

		try:
			if jname==j_list[2]:
				impactfactor=j_list[6]
			else:
				impactfactor='0'
		except:
			pass
		
		#driver.quit()
		
		#web of science
		if impactfactor=='0':
			try:
				
				options=webdriver.ChromeOptions()
				#options.add_argument('headless')
				options.add_argument('window-size=1920x1080')
				options.add_argument("--disable-gpu")
				options.add_argument("--no-sandbox")
				
				driver=webdriver.Chrome('/Users/song/Downloads/chromedriver',chrome_options=options)
				driver.implicitly_wait(0.5)
				
				url4='http://apps.webofknowledge.com/WOS_GeneralSearch_input.do?product=WOS&search_mode=GeneralSearch&SID=E2sQzu6vkqLlwp8pcR3&preferencesSaved='
				driver.get(url4)

				time.sleep(0.5)
				
				driver.find_element_by_xpath('//*[@id="clearIcon1"]').click()
				
				time.sleep(0.5)
				
				for w in scholar:
					driver.find_element_by_xpath('//*[@id="value(input1)"]').send_keys(w)
					time.sleep(0.1)

				try:
					driver.find_element_by_xpath('//*[@id="searchCell1"]/span[1]/button').click()
				except:
					pass
					
				time.sleep(0.5)
				
				driver.find_element_by_xpath('//*[@id="show_journal_overlay_link_1"]/a/span/value').click()
				time.sleep(0.5)
				source_w=driver.page_source
				soup_w=BeautifulSoup(source_w,'html.parser')
				
				soups_w3=soup_w.find("table",class_='Impact_Factor_table').find("tr")
				soups_w3=soups_w3.text.strip()
				soups_w3=soups_w3.split()[-1]
				soups_w4=soup_w.find_all("span",class_='hitHilite')
				
				check1=0
				check2=0
				
				for a in soups_w4:
					check1+=1
					
				scholar=scholar.split()
				
				for b in scholar:
					check2+=1
				
				if check1>=check2*0.7:
					impactfactor=soups_w3
				
			except:
				pass
			
		driver.quit()

		rs={
		'find':sssoup,
		'scholar':scholar,
		'jname':jname,
		'jyear':jyear,
		'impactfactor':impactfactor
		}
		print(rs)
		return rs
		
def DisplayProfessor(request, professorId):
    
    #pname = request.GET.get('pName')
    #jname = request.GET.get('jName')
    
    result = Professor.objects.filter(professor_id=professorId)[0]
    #bookInfo = "PID: {0}; PNAME: {1}; PHOMEPAGE: {2}; DNAME: {3}".format(result.professor_id,result.title,result.memo['content'])
    pInfo = "PID: {0}; PNAME: {1}; PHOMEPAGE: {2}; DNAME: {3}".format(result.professor_id,result.professor_name,result.professor_homepage,result.depart_name)
    return render(request, 'jouIF/mypage.html',
                  { 'welcome_text': pInfo })