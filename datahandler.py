#TIETS43 RECOMMENDER SYSTEMS 2018 group work
#Aki Lempola & Rauno Pennanen
#a python script that processes movielens data files into a pandas dataframe

import csv, pandas as pd

#read the data files
links=csv.reader(open('links.csv'))
movies=csv.reader(open('movies.csv'))
ratings=csv.reader(open('ratings.csv'))
tags=csv.reader(open('tags.csv'))

#add movieIDs to a list
movielist=[]
for row in movies:
  try:
    movielist.append(int(row[0]))
  except ValueError:
    pass

#make a list of dictionaries with the ratings out of the data
#userID=row[0],movieID=row[1],rating=row[2]

dlist=[]
d={}
user=1
for row in ratings:
  try:
    if int(row[0])==user:
      d[int(row[1])]=float(row[2])
    else:
      dlist.append(d)
      d={}
      d[int(row[1])]=float(row[2])
      user+=1
  except ValueError:
    pass
dlist.append(d)

#add a -1 to signify a missing value into a list of dictionaries
endres=[]
d={}
for i in range(0,len(dlist)):
  for movie in movielist:
    if dlist[i].get(movie):
      d[movie]=dlist[i].get(movie)
    else:
      d[movie]=-1    
  endres.append(d)
  d={}

#create a pandas dataframe from the so far processed data
#that looks like this
#
#       movie1 movie2 movie3 movie4...  
#user1  rating 3      -1     1     ...
#user2  5      4      2      -1    ...
#user3  3      -1     3      3     ...
#.      .      .      .      .
#.      .      .      .      .
#.      .      .      .      .

df=pd.DataFrame(endres)
df.index+=1

df.to_csv('dataset.csv')