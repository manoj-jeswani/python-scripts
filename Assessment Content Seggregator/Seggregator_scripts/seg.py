import os
import string
import random
import re
from collections import defaultdict
import shutil
import time

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_pid(pool="",size=5,taken=set()):
	res=""
	res=''.join([random.choice(pool) for _ in range(size)])
	if res in taken:
		res= get_pid(pool,size,taken)
	taken.add(res)
	return res


def extract_prob_info(f):
	res={}
	for line in f:
		tobj=re.search(r'^Title( *):(.*)$',line,re.M|re.I)
		if tobj is not None:
			res['Title']=tobj.group(2).strip().title()
		lobj=re.search(r'^Level( *):(.*)$',line,re.M|re.I)
		if lobj is not None:
			res['Level']=lobj.group(2).strip().capitalize()
		tagobj=re.search(r'^Tag( *):(.*)$',line,re.M|re.I)
		if tagobj is not None:
			res['Tag']=tagobj.group(2).strip().capitalize()
	return res


def extract_tc_info(f):
	res={}
	for line in f:
		tobj=re.search(r'^(.*)Title( *):(.*)$',line,re.M|re.I)
		if tobj is not None:
			res['Title']=tobj.groups()[-1].strip().title()
		lobj=re.search(r'^(.*)Level( *):(.*)$',line,re.M|re.I)
		if lobj is not None:
			res['Level']=lobj.groups()[-1].strip().capitalize()
		tagobj=re.search(r'^(.*)Tag( *):(.*)$',line,re.M|re.I)
		if tagobj is not None:
			res['Tag']=tagobj.groups()[-1].strip().capitalize()
	return res


def extract_tc_info(f):
	res={}
	for line in f:
		tobj=re.search(r'^(.*)Problem Title( *):(.*)$',line,re.M|re.I)
		if tobj is not None:
			res['Problem Title']=tobj.groups()[-1].strip().title()
		tagobj=re.search(r'^(.*)Tag( *):(.*)$',line,re.M|re.I)
		if tagobj is not None:
			res['Tag']=tagobj.groups()[-1].strip().capitalize()
	return res

def extract_sol_info(f):
	res={}
	for line in f:
		tobj=re.search(r'^(.*)Problem Title( *):(.*)$',line,re.M|re.I)
		if tobj is not None:
			res['Problem Title']=tobj.groups()[-1].strip().title()
	return res


def get_ext(name):
	tobj=re.search(r'^(.*)\.(.*)$',name,re.M|re.I)
	return tobj.groups()[-1]


def get_data_dict():
	
	'''
	hops into dirs, reads files and extracts information necessary to categorize them in the desired manner
	extracted info is stored in dictionaries -->
	 pdict: contains info of all problems
	 tcdict: contains info of all testcases
	 soldict: contains info of all solutions
	'''

	in_path=BASE_DIR+"/Raw_Data/"
	pool=string.ascii_lowercase + string.ascii_uppercase + string.digits
	taken_pid=set()

	pdict=dict([('Easy',[]),('Medium',[]),('Difficult',[])])
	tcdict=defaultdict(lambda :[])
	soldict=defaultdict(lambda :[])
	
	for cr_name in os.listdir(in_path):
		prob_path=os.path.join(in_path,cr_name+"/Problems/")
		sol_path=os.path.join(in_path,cr_name+"/Solutions/")
		tc_path=os.path.join(in_path,cr_name+"/Testcases/")

		for x in os.listdir(prob_path):
			y=os.path.join(prob_path,x)
			with open(y) as f:
				res=extract_prob_info(f)
				pdict[res['Level']].append({'creator':cr_name,'ptitle':res['Title'],'pid':get_pid(pool,3,taken_pid),'tag':res['Tag'],'path':y})
			

		for x in os.listdir(tc_path):
			y=os.path.join(tc_path,x)
			with open(y) as f:
				res=extract_tc_info(f)
				tcdict[(res['Problem Title'],cr_name)].append({'fname':x,'tag':res['Tag'],'path':y})

		for x in os.listdir(sol_path):
			y=os.path.join(sol_path,x)
			with open(y) as f:
				res=extract_sol_info(f)
				soldict[(res['Problem Title'],cr_name)].append({'fname':x,'ext':get_ext(x),'path':y})
			


	return (pdict,tcdict,soldict)


def beautify(name):
	return name.replace(" ","_")

def get_pdir_name(pobj):
	return '__'.join([beautify(pobj['creator']),beautify(pobj['ptitle']),beautify(pobj['pid'])])


def main():
	pdict,tcdict,soldict=get_data_dict()
	out_path=BASE_DIR+"/Seggregated_Data/"

	for key in pdict:
		y=os.path.join(out_path,key)
		if not os.path.exists(y):
			os.mkdir(y)
		
		for pobj in pdict[key]:
			yp=os.path.join(y,get_pdir_name(pobj))
			yt=os.path.join(yp,"Testcases")
			ys=os.path.join(yp,"Solutions")
			yf=os.path.join(yp,pobj['ptitle'])
			
			os.mkdir(yp)
			os.mkdir(yt)
			os.mkdir(ys)
			shutil.copyfile(pobj['path'],yf)
			slist=soldict[(pobj['ptitle'],pobj['creator'])]
			
			for sobj in slist:
				yst=os.path.join(ys,sobj['ext']+" solutions")
				ysf=os.path.join(yst,sobj['fname'])

				if not os.path.exists(yst):
					os.mkdir(yst)
				shutil.copyfile(sobj['path'],ysf)

					
			tclist=tcdict[(pobj['ptitle'],pobj['creator'])]
			
			for tcobj in tclist:
				ytt=os.path.join(yt,tcobj['tag'])
				ytf=os.path.join(ytt,tcobj['fname'])

				if not os.path.exists(ytt):
					os.mkdir(ytt)
				shutil.copyfile(tcobj['path'],ytf)

					






if __name__=="__main__":
	stime=time.time()
	main()
	print(time.time()-stime)	