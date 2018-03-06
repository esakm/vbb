import reporter
import csv
import time
company_file = open('NASDAQ.csv')
csv_reader = csv.reader(company_file)
company_list = list(csv_reader)
t_list = []
count = 0
report_done = False
for company in company_list:
    if company[5] == 'Technology':
        r = reporter.Reporter(company)
        t_list.append(r)

for i in range(5):
    t_list[i].start()
    time.sleep(3)
counter = len(t_list) - 1
while not report_done:
    if counter == 5:
        report_done = True
        continue
    for thread in t_list:
        if thread.driver_done:
            t_list[counter].start()
            counter -= 1
            break
    time.sleep(7)
