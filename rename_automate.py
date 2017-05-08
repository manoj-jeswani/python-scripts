import os
main_path="/media/mj/F6A400C5A4008A77/spt/"
source_dir_name=""
os.chdir(main_path+source_dir_name)
bn=os.popen("ls").read().split("\n")
k=1
for i in bn:
	print(i)
	try:

		os.rename(i,str(k)+".jpg")
		print("SUCCESSFULLY RENAMED")
	except:
		print("Rename unsuccessful")
	k=k+1