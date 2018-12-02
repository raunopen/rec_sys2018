#TIETS43 RECOMMENDER SYSTEMS 2018 group work
#Aki Lempola & Rauno Pennanen
import pandas as pd
import csv
from scipy.stats import pearsonr

MIN_SAMPLE_SIZE = 10
dataset=pd.read_csv('dataset.csv',index_col=0)
# rows = users, (row = userId -1 )
# cols = movies (col = movieId -1 )
data = dataset.values
movie_ids = dataset.columns

movie_names = {}
with open('movies.csv', 'r') as rfile:
    reader = csv.reader(rfile)
    lineCount = 0
    for row in reader:
        if lineCount == 0:
            lineCount += 1
        else:
            key = int(row[0])
            value = row[1]
            movie_names[key] = value
            lineCount += 1

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
            size = MIN_SAMPLE_SIZE # min sample size for pearson correlation
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

def predict(user, simUsers):
    movies = set()
    # set of movies rated by sim users
    for user_id, pearson in simUsers:
        movies = movies.union( movies_rated_by(user_id) )
    # remove movies allready rated by the user
    movies = movies.difference( movies_rated_by(user) )
    
    user_mean = user_mean_rating[user]
    predicted = {}
    for movie in movies:
        r = 0.0 # predicted movie rating
        p_sum = 0.0
        for user_id, pearson in simUsers:
            mean = user_mean_rating[ user_id ]
            rating = data[user_id][movie]
            if rating >= 0:
                r += (rating - mean) * pearson
            p_sum += pearson
        
        predicted[movie] = user_mean + (r / p_sum )
    result = sorted(predicted.items(), key=lambda x: x[1], reverse=True)
    for i, r in result[:5]:
        m_id = int(movie_ids[i])
        print(movie_names[m_id], r)
        # TODO return list of movie ids, instead of printing

# mean ratings for the users 
user_mean_rating = []
for i, row in enumerate(data):
    movies = movies_rated_by(i)
    n = len(movies)
    summ = float( sum( get_ratings(i, movies) ))
    user_mean_rating.append( summ / n )

#user = 224 # test user id
#simUsers = pearson_similarity(user, rated_same_movies(user), 20)
#predict(user, simUsers)

# user interface
user_list=[]
for i in dataset.index:
    user_list.append(i)
print("-= SUPER MOVIE RECOMMENDER v1.0 =-")
print("Give a valid user ID to get movie recommendations for that user.")
print("Write 'exit' when you wish to exit the program.\n")
while True:
    user=input("Give user ID (or write 'exit' to quit): ")
    try:
        if user=='exit':
            print('\nExiting program...')
            break
        user=int(user)
        if user in user_list:
            print('The top 5 movie recommendations for user {}:\n'.format(user))
            simUsers = pearson_similarity(user, rated_same_movies(user), 20)
            predict(user, simUsers)
            print()
        else:
            print("\nERROR - User not found.\nPlease try again.\n")
    except (ValueError, NameError):
        print("\nERROR - User not found.\nPlease try again.\n")
