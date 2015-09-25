# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 15:14:16 2015

@author: schiang
"""

import csv
import math    
from datetime import datetime
from sklearn import linear_model
import numpy

#The function calculations the subscription type based on two consecutive transactions
def calculateType(first, second):
    delta = second - first
    if (delta.days == 1):
        return 'daily'
    elif (delta.days <= 31 and delta.days >= 28):
        return 'monthly'
    else:
        return 'yearly'
    
#Returns the duration of the subscription
def calculateDuration(first, third):
    return str((third - first).days) + ' days'

subs = dict()
dateFormat = '%m/%d/%Y'
startYear = 1966
endYear = 2014
years = [0] * (endYear - startYear + 1) 

#Reads the csv file
with open ('subscription_report.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    reader.next()
    for row in reader:
        #Array of years and revenues
        year = int((row[3].split('/'))[2])
        years[year - startYear] += int(row[2])
    
        #Map by subscription ID
        if row[1] in subs:
            temp = subs[row[1]]
            if len(temp) == 3:
                temp[2] = row[3]
            else:
                temp.append(row[3])
        else:
            subs[row[1]] = [row[3]]
            
#Outputs the type and duration of the subscription 
for key, value in subs.iteritems():
    if (len(value) == 1):
        print '{}, {}, {}'.format(key, 'one-off', 'no duration')
    else:
        subType = calculateType(datetime.strptime(value[0], dateFormat), datetime.strptime(value[1], dateFormat))
        subDuration = calculateDuration(datetime.strptime(value[0], dateFormat), datetime.strptime(value[2], dateFormat))
    
        print '{}, {}, {}'.format(key, subType, subDuration)

maxRev = 0
maxYear = 0
minRev = 'Inf'
minYear = 0

#Calculates the max and min revenues
for i in range(1, len(years)):
    if (years[i]-years[i-1] > maxRev):
        maxRev = years[i]-years[i-1]
        maxYear = i + startYear
    if (years[i]-years[i-1] < minRev):
        minRev = years[i]-years[i-1]
        minYear = i + startYear
        
print 'The largest revenue growth of {} was from {} to {}.'.format(maxRev, maxYear-1, maxYear) 
print 'The smallest revenue growth of {} was from {} to {}.'.format(abs(minRev), minYear-1, minYear) 

#Machine Learning
#constructs a matrix of features
X = [[years[0], years[1], years[2], years[3], years[4]],
     [years[1], years[2], years[3], years[4], years[5]]]
y = [years[5], years[6]]

for i in range(7, len(years) - 1):
    temp = [years[i-1], years[i-2], years[i-3], years[i-4], years[i-5]]
    y.append(years[i])
    X = numpy.concatenate((X, [temp]), axis = 0)

#Fits and predicts the data based on previous revenue values
clf = linear_model.LinearRegression()
clf.fit(X, y)

diff = endYear - startYear
test = [years[diff], years[diff-1], years[diff-2], years[diff-3], years[diff-4]]
print round(clf.predict(test), 2)