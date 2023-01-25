from crontab import CronTab

my_cron = CronTab(user='batyr')
job = my_cron.new(command='python3 /home/batyr/projects/SSR/cdnvpn-tools/client_list_generator.py')
job.minute.every(1)
my_cron.write()