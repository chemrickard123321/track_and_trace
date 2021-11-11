import pandas as pd

from pep8_processing import order_by_date, people_with_infectious_contacts, group_by_day_contact, time_dist_converter
from pep8_risk_calculations import risk_per_contact, daily_risk
from pep8_notifications import notifications


dataset = pd.read_pickle('testData')
dataset = order_by_date(dataset)
dataset, infectiousPeople = people_with_infectious_contacts(dataset)
dataset = group_by_day_contact(dataset)
dataset = risk_per_contact(dataset)
dataset = daily_risk(dataset)
dataset = notifications(dataset)
print(dataset)





# dataset = pd.read_csv('/home/chem/Documents/dataset.csv') actual data
