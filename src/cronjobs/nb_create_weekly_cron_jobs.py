#kevin fink
#kevin@shorecode.org
#Sept 25 2023
#nutrition_bot/cronjobs/nb_create_weekly_cron_jobs.py

import crontab

# user=True indicates that the current users crontab will be used
cron_diary = crontab.CronTab(user=True)
check_if_cron_exists = cron_diary.find_command('nb_cron_send_weekly_diary_report.py')
try:
    # this will raise an exception if there is no cron job with teh command: nb_cron_send_weekly_diary_report.py
    # if the cron job exists, the except statement will not execute so a duplicate job will not be created
    check_if_cron_exists.__next__()
except StopIteration:        
    job = cron_diary.new(command='nb_cron_send_weekly_diary_report.py')
    # dow.on(6) = day of week(saturday)
    job.dow.on(6)
    # 1pm = 13
    job.hour.on(13)
    cron_diary.write()

# user=True indicates that the current users crontab will be used
cron_dietplan = crontab.CronTab(user=True)
check_if_cron_plan_exists = cron_diary.find_command('nb_cron_send_weekly_plan_report.py')
try:
    # this will raise an exception if there is no cron job with teh command: nb_cron_send_weekly_diary_report.py
    # if the cron job exists, the except statement will not execute so a duplicate job will not be created    
    check_if_cron_plan_exists.__next__()    
except StopIteration:        
    job = cron_dietplan.new(command='nb_cron_send_weekly_plan_report.py')
    # dow.on(0) = day of week(sunday)
    job.dow.on(0)
    # 1pm = 13
    job.hour.on(13)
    cron_dietplan.write()
    
datavizdir = '/home/kevin/Coding/Learning/Projects/nutrition_bot/nutrition_bot/dataviz/'
crondatavizdir = '/home/kevin/Coding/Learning/Projects/nutrition_bot/nutrition_bot/cronjobs/dataviz/'
cron_viz_files = crontab.CronTab(user=True)
cron_cronviz_files = crontab.CronTab(user=True)
check_if_cron_files_exists = cron_viz_files.find_command(f'rm {datavizdir}*')
check_if_cronviz_files_exists = cron_cronviz_files.find_command(f'rm {crondatavizdir}*')

try:
    # this will raise an exception if there is no cron job with teh command: nb_cron_send_weekly_diary_report.py
    # if the cron job exists, the except statement will not execute so a duplicate job will not be created    
    check_if_cron_files_exists.__next__()    
except StopIteration:        
    job = cron_viz_files.new(command=f'rm {datavizdir}*')
    # 4am = 4
    job.hour.on(4)
    cron_viz_files.write()

try:
    # this will raise an exception if there is no cron job with teh command: nb_cron_send_weekly_diary_report.py
    # if the cron job exists, the except statement will not execute so a duplicate job will not be created    
    check_if_cronviz_files_exists.__next__()    
except StopIteration:        
    job = cron_cronviz_files.new(command=f'rm {crondatavizdir}*')
    # 4am = 4
    job.hour.on(4)
    cron_cronviz_files.write()