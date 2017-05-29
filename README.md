# python-scripts
Scripts written to automate daily stuff

$$ automate.py  :: Implements Linux { grep + mv } , it requires a pattern in input and makes a recursive search (for all 
                   the files matching the given pattern) in all the directories starting from the base directory (whose 
                   path has to be supplied in input).
                   It moves all the searched files into a directory (that gets created dynamically in base directory and 
                   its name has to be supplied in input).
                   Moreover,it has options for multi pattern search :: with ALL PATTERNS INCLUDE and ANY ONE PATTERN INCLUDE                      choices..
                   
                   
$$ rename_automate.py :: It takes in input the Base directory path and renames all the files (present in that directory) in an
                         increasing numeric order..
