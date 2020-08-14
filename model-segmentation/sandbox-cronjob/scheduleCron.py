/*=============================================================================
|   Source code: scheduleCron.py
|   Author:  Alejandro Martinez
|   Assignment:  Cron Jobs
|   Due Date:  [12/13/2020]
|
|  Language:  Python 3
|  Compile/Run:
|
|   Running Files:
|	Before running the file python3 scheduleCron.py, make sure you have
|	installed the following dependencies:
|		- pip install python-crontab
|
|	Note: The description will explain what crontap performs but these
|		two commands will be important when using crontab
|			- crontab -l : Allows you to see all your crontab jobs
|			- contrab -e : Allows you to edit your crontab jobs
|
|--------------------------------------------------------------------------------
|	
|
|  Description: 
|               The purpose of this code is be able to call a program multiple
|               times without specifically running that program.
|               For this purpose we are going to be using the cron library from
|               python that allows us to schedule calls to a program.
|      
|               Our program will have 3 files. These files are: scheduleCron.py,
|               hello.py, hello2.py. To make everything easier have the files
|               in the same directory.
|               
|               After installing the cron library, when the file scheduleCron.py 
|               is run, it will call files hello.py and 30 seconds after it will
|               call files hello2.py. The output of these files will be piped to
|               file test.txt. I decided to call two files (hello.py and hello2.py)
|               for testing purposes (Making sure that the files are running 
|               every 30 seconds). For the purpose of our project, that file name
|               should be the same.
|
|        Input:  No input
|
|	    Output:  Check the test.txt file to see the output
|
|      Sources:
|   
|           Main Sources: 
|           https://pypi.org/project/python-crontab/#description
|           https://code.tutsplus.com/tutorials/managing-cron-jobs-using-python--cms-28231
|           These were the main sources and thatt helped me the most to create 
|           create the project
|
|           Scheduler of Cron:
|           https://crontab.guru/#1_*_*_*_*
|           This is a website that allows to make schedules
|
|           Crypto Tutorial with Cron: 
|           https://www.youtube.com/watch?v=kL5rmcxwgSs
|           https://www.youtube.com/watch?v=LRC4gWRblL8
|           Tutorial using cryto API
|
|           Tutorial to make cron run in seconds:
|           https://www.youtube.com/watch?v=OX1KALe3dcE
|           https://stackoverflow.com/questions/9619362/running-a-cron-every-30-seconds#:~:text=Cron%20job%20cannot%20be%20used,while%20loop%20as%20shown%20below.
|
|           
|
|.  Explanation of Code:
|
|       - Make sure that the user will be the user where the 
|           program will be running
|       my_cron = CronTab(user = 'alejandromartinez')
|       
|       - The Cron Job has to be established as follows:
|          [environment  File  >> Output File]
|           Note: Output file not necessary.
|           Environment: In my case is /usr/local/opt/python@3.8/libexec/bin/python
|           (1)Location of file to be runned: /Users/alejandromartinez/hello.py
|           (2)Location of file 2 to be runned: /Users/alejandromartinez/hello2.py
|           Output: test.txt
|       my_cron.new(command = '/usr/local/opt/python@3.8/libexec/bin/python /Users/alejandromartinez/hello.py >> test.txt')
|       my_cron.new(command = 'sleep 30; /usr/local/opt/python@3.8/libexec/bin/python /Users/alejandromartinez/hello2.py >> test.txt')
|
|       - my_cron.write() is necesary to make sure the cron job is placed.
|
|   Known Bugs:  Not know Bugs in this program
|
|  *=====================================================================
|  */

from crontab import CronTab

#create the object of the crontab
my_cron = CronTab(user = 'alejandromartinez')

my_cron.new(command = '/usr/local/opt/python@3.8/libexec/bin/python /Users/alejandromartinez/cron/cronJob/hello.py >> test.txt')
my_cron.new(command = 'sleep 30; /usr/local/opt/python@3.8/libexec/bin/python /Users/alejandromartinez/cron/cronJob/hello2.py >> test.txt')

#job.minute.every(1)
print('Running Task')

my_cron.write()




