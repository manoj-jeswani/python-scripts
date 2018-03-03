<h1>Pythonic Magic</h1>
<h2>--Scripts written to automate time consuming manual work</h2>
<hr>
<hr>

<h3>Contents</h3>
<b>
 <ol>
<li> Assessment Content Seggregator</li>
 <ul>
 <li> /Raw_Data : Data to be read and seggregated using wildcard searching<br>
</li>
<li> /Seggregated_Data : Output data after execution of seggregator script<br>
</li>
 <li> /Seggregator_scripts :<br> 

  <ol>
  <br>
   <li> seg.py :: Goes deep into directory structure, reads files, makes wildcard searches, seggregates them on basis of<br>
  'Problem title-Tag-Level', 'Test-Cases Tags' , 'Solutions Languages'.<br>

  <h6>Run: python3 seg.py</h6></li>
 <br>
   <li> concurrent_seg.py :: Obtained after reverse engineering of seg.py by using multithreading and thread syncronization in<br> all those tasks in which concurrent processing was possible <br>
  <h6>Run: python3 concurrent_seg.py</h6><br>
</li>
  </ol>
<h5>After execution, /Seggregated_Data directory shall get flooded with organized data and script execution time shall get printed on console.
<br>
<h5>execution_time(concurrent_seg.py) << execution_time(seg.py)<h5>  
</li>
   </ul>
<hr>


<li> automate.py  ::<br>
Implements Linux { grep + mv } , it requires a pattern in input and makes a recursive search (for all the files matching<br> the given pattern) in all the directories starting from the base directory (whose path has to be supplied in input). <br>
It moves all the searched files into a directory (that gets created dynamically in base directory and its name has to be<br> supplied in input). <br>
Moreover,it has options for multi pattern search :: with ALL PATTERNS INCLUDE and ANY ONE PATTERN INCLUDE choices..
              </li><br>     
                   
<li> rename_automate.py ::<br>
It takes in input the Base directory path and renames all the files (present in that directory) in an increasing numeric order..</li>
</ol>
