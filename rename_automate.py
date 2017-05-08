import os
main_path="PATH OF DIRECTORY CONTAINING FILES TO BE RENAMED"
source_dir_name=""
os.chdir(main_path+source_dir_name)
bn=os.popen("ls").read().split("\n")
k=1 #name would start from 1 
for i in bn:
	print(i)
	try:

		os.rename(i,str(k)+".jpg") #extension here can be changed according to the type of files being renamed
		print("SUCCESSFULLY RENAMED")
	except:
		print("Rename unsuccessful")
	k=k+1
