#Searching recursively for files having specified patterns in their name and Moving them to a specified directory

#TO DO :: required functionality::: 
#file names with $ sign not getting moved
import os
patterns=[] #give the list of patterns to be searched for 
all_pat_present=1 # if 1 then fetches only those files which contain all the patterns specified into list
# if 0 then fetches any file that contain atleast one of the specified patterns in the list
main_path="PATH OF DIRECTORY (IN WHICH SEARCH IS TO BE MADE RECURSIVELY)"
source_dir_name=""
dest_dir_name="NAME OF DIRECTORY THAT WOULD BE CREATED ON SPECIFIED PATH AND WOULD STORE THE SEARCH RESULTS"
dest_path=main_path+dest_dir_name+"/"
#here give the names of directories(in which search is not to be made) present in current directory
not_to_be_checked_in_dir=(dest_dir_name) #give in this tuple the directories name in which search is not to be made

os.chdir(main_path)
bn=os.popen("ls").read().split("\n")
if dest_dir_name not in bn:
	os.system("mkdir "+dest_dir_name)


dit={"-":"\-","(":"\(",")":"\)","\\":"\\\\","[":"\[","]":"\]","'":"\'","$":"\$"}

def moveFun(path):		#supply the path of directory from which all  files  have to be fetched and moved
	cn=[]
	pt=main_path+path
	os.chdir(pt)
	mn=os.popen("ls").read().split("\n")
	for i in mn:
		if os.path.isdir(i):
			#files in the following folders should not be moved anywhere
			if i not in not_to_be_checked_in_dir: 
				cn.append(i)
	
		else :

			if all_pat_present==0: # moves file when it's name contains any one of the specified patterns
				for m in patterns:
					if m in i:
						for j in dit:
							if j in i :
								i.replace(j,dit[j])
						print("File Being Moved : ",i)
						try:
							os.system("mv "+'"'+i+'"'+" "+dest_path)
							#mn.remove(i)  <-- CREATES UNEXPECTED MOVING
						except:
						 	print("########### FILE NOT MOVED : EXCEPTION ERROR ############")
						break	#as soon as one of the specified patterns match:: we break out and  any no futher checking for other patterns occur bcoz even one pattern matching confirms that file will be moved so no further checking required  	

			else :  #moves file only when it's name contains all the patterns specified in the list 
				c=0
				for m in patterns:
					if m not in i:
						c=-1
						break
				if c==0 :

					for j in dit:
						if j in i :
							i.replace(j,dit[j])
					print("File Being Moved : ",i)
					try:
						os.system("mv "+'"'+i+'"'+" "+dest_path)
						#mn.remove(i)  <-- CREATES UNEXPECTED MOVING
					except:
					 	print("########### FILE NOT MOVED : EXCEPTION ERROR ############")



	print("Directories Present In Current Directory : ",cn)
		
	if len(cn)==0:
		return
	for i in cn:
		print("Current Directory : ",i)
		if " " in i:
			i.replace(" ","\ ")
		moveFun(path+i+"/")
		
	
moveFun(source_dir_name)


