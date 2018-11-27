#TIETS43 RECOMMENDER SYSTEMS 2018 group work
#Aki Lempola & Rauno Pennanen
import pandas as pd
from scipy.stats import pearsonr


dataset=pd.read_csv('dataset.csv',index_col=0)
# rows = users, (row = userId -1 )
# cols = movies (col = movieId -1 )
data = dataset.values
user = 0


# returns set of cols rated by the user
def movies_rated_by(user):
    #movies ratet by user
    mIds = set()
    for i, r in enumerate(data[user], 0):
        if r >= 0 : mIds.add(i)
    return mIds

# retuns array of tuples: (userId, {movieIds}):
# where userId is the user that rated atleast 1 same movie as user.
# set {movieIds}: contais col numbers to movies rated by both.
def rated_same_movies(user):
    movies = movies_rated_by(user)
    users = []
    for i, u in enumerate(data, 0):
        if i != user :
            mIds = movies_rated_by(i)
            mIds = movies.intersection(mIds)
            size = 25 # min sample size for pearson correlation
            if len( mIds ) > size : users.append( (i,mIds) )
    return users

# param ids: set of movie ids
#      user: user id 
# return rating array correspondin to the ids
def get_ratings(user, ids):
    ratings = []
    for i in ids:
        ratings.append(data[user][i])
    return ratings
        

# param user: user id
#      users: set of userIds
#          n: return top n similar usersIds:
def pearson_similarity(user, users, n):
    result = {}
    for u, mids in rated_same_movies(user):
        x = get_ratings( user, mids)
        y = get_ratings( u, mids)
        result[u] = pearsonr(x,y)[0]
        '''
        if u == 368:
            print( 0, x )
            print( u, y )
            
            print('pearson correlation: ',pearsonr(x,y)[0])
            print('-------------------------------')
        '''
    result = sorted(result.items(), key=lambda x: x[1], reverse=True)
    return result[:n]


# TODO recommend movies from simUsers

# TODO User interace

user = 0 # test user id
simUsers = pearson_similarity(user, rated_same_movies(user), 20)
for user, correlation in simUsers:
    print(user, correlation)