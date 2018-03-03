import os
import string
import random
import re
from collections import defaultdict
import shutil
import threading
import time

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pdict=dict([('Easy',[]),('Medium',[]),('Difficult',[])])
tcdict=defaultdict(lambda :[])
soldict=defaultdict(lambda :[])


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


def do_for_each_prob_dir(prob_path,l1,pool,taken_pid,cr_name):
	global pdict
	for x in os.listdir(prob_path):
		y=os.path.join(prob_path,x)
		with open(y) as f:
			res=extract_prob_info(f)
			l1.acquire()
			pdict[res['Level']].append({'creator':cr_name,'ptitle':res['Title'],'pid':get_pid(pool,3,taken_pid),'tag':res['Tag'],'path':y})
			l1.release()


def do_for_each_tc_dir(tc_path,l2,cr_name):
	global tcdict
	for x in os.listdir(tc_path):
		y=os.path.join(tc_path,x)
		with open(y) as f:
			res=extract_tc_info(f)
			l2.acquire()
			tcdict[(res['Problem Title'],cr_name)].append({'fname':x,'tag':res['Tag'],'path':y})
			l2.release()




def do_for_each_sol_dir(sol_path,l3,cr_name):
	global soldict
	for x in os.listdir(sol_path):
		y=os.path.join(sol_path,x)
		with open(y) as f:
			res=extract_sol_info(f)
			l3.acquire()
			soldict[(res['Problem Title'],cr_name)].append({'fname':x,'ext':get_ext(x),'path':y})
			l3.release()



def do_for_each_creator(cr_name,in_path,pool,taken_pid,l1,l2,l3):
	prob_path=os.path.join(in_path,cr_name+"/Problems/")
	sol_path=os.path.join(in_path,cr_name+"/Solutions/")
	tc_path=os.path.join(in_path,cr_name+"/Testcases/")
	
	p=threading.Thread(target=do_for_each_prob_dir,args=(prob_path,l1,pool,taken_pid,cr_name),name="t_{0}_prob".format(cr_name))
	p.start()

	tc=threading.Thread(target=do_for_each_tc_dir,args=(tc_path,l2,cr_name),name="t_{0}_tc".format(cr_name))
	tc.start()

	sol=threading.Thread(target=do_for_each_sol_dir,args=(sol_path,l3,cr_name),name="t_{0}_sol".format(cr_name))
	sol.start()

	p.join()
	tc.join()
	sol.join()
	




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
	
	thread_list=[]
	l1=threading.Lock()
	l2=threading.Lock()
	l3=threading.Lock()

	for cr_name in os.listdir(in_path):
		t=threading.Thread(target=do_for_each_creator,args=(cr_name,in_path,pool,taken_pid,l1,l2,l3),name="t_{}".format(cr_name))
		t.start()
		thread_list.append(t)

	list(map(lambda x:x.join(),thread_list))
	'''
		map applies the given fxn to each element of list,
		but its workflow is same as that of queryset i.e 
		like queryset it only returns the map object but
		does not execute the actual thing(query),
		so to get the query performed like in queryset
		we can apply any of the functions like repr(), list(), etc.
		on qset , similarly we have to apply any of these on the map object,
		so to make it do the actual work
	''' 	
	


def beautify(name):
	return name.replace(" ","_")

def get_pdir_name(pobj):
	return '__'.join([beautify(pobj['creator']),beautify(pobj['ptitle']),beautify(pobj['pid'])])


def write_for_each_tcdir(tclist,yt):
	for tcobj in tclist:
		ytt=os.path.join(yt,tcobj['tag'])
		ytf=os.path.join(ytt,tcobj['fname'])

		if not os.path.exists(ytt):
			os.mkdir(ytt)
		shutil.copyfile(tcobj['path'],ytf)


def write_for_each_soldir(slist,ys):
	for sobj in slist:
		yst=os.path.join(ys,sobj['ext']+" solutions")
		ysf=os.path.join(yst,sobj['fname'])

		if not os.path.exists(yst):
			os.mkdir(yst)
		shutil.copyfile(sobj['path'],ysf)






def write_for_each_probdir(y,pobj,pdir_name,key):
	global tcdict,soldict

	yp=os.path.join(y,pdir_name)
	yt=os.path.join(yp,"Testcases")
	ys=os.path.join(yp,"Solutions")
	yf=os.path.join(yp,pobj['ptitle'])
	
	os.mkdir(yp)
	os.mkdir(yt)
	os.mkdir(ys)
	shutil.copyfile(pobj['path'],yf)

	slist=soldict[(pobj['ptitle'],pobj['creator'])]
	st=threading.Thread(target=write_for_each_soldir,args=(slist,ys),name="t_{0}_{1}_sol".format(key,pdir_name))
	st.start()
	
	tclist=tcdict[(pobj['ptitle'],pobj['creator'])]
	tct=threading.Thread(target=write_for_each_tcdir,args=(tclist,yt),name="t_{0}_{1}_tc".format(key,pdir_name))
	tct.start()
	
	st.join()
	tct.join()



def write_for_each_level(out_path,key):
	global pdict
	y=os.path.join(out_path,key)
	if not os.path.exists(y):
		os.mkdir(y)

	thread_list=[]
	
	for pobj in pdict[key]:
		pdir_name=get_pdir_name(pobj)
		t=threading.Thread(target=write_for_each_probdir,args=(y,pobj,pdir_name,key),name="t_{0}_{1}".format(key,pdir_name))
		t.start()
		thread_list.append(t)

	list(map(lambda x:x.join(),thread_list))





def write_seggregated():
	out_path=os.path.join(BASE_DIR,"Seggregated_Data/")

	thread_list=[]
	for key in pdict:
		t=threading.Thread(target=write_for_each_level,args=(out_path,key),name="t_{}".format(key))
		t.start()
		thread_list.append(t)

	list(map(lambda x:x.join(),thread_list))





def main():
	get_data_dict()
	write_seggregated()


if __name__=="__main__":
	stime=time.time()
	main()
	print(time.time()-stime)