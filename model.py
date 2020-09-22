import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
def get_title_from_index(index):
    	return df[df.index == index]["title"].values[0]

def get_index_from_title(title):

  if title not in df['title'].unique():
    return -1
  else:
    return df[df.title == title]["index"].values[0]

## Read CSV File
df = pd.read_csv("movie_dataset.csv")
#print df.columns
## Select Features

features = ['keywords','cast','genres','director']
## Creating a column in DF which combines all selected features
for feature in features:
	df[feature] = df[feature].fillna('')

def combine_features(row):
	try:
		return row['keywords'] +" "+row['cast']+" "+row["genres"]+" "+row["director"]
	except:
		print("Error:",row)

df["combined_features"] = df.apply(combine_features,axis=1)

#print "Combined Features:", df["combined_features"].head()

## Creating count matrix from this new combined column
cv = CountVectorizer()

count_matrix = cv.fit_transform(df["combined_features"])

##Computing the Cosine Similarity based on the count_matrix
cosine_sim = cosine_similarity(count_matrix) 
movie_user_likes = input("Enter a movie name :")


## Getting index of this movie from its title
movie_index = get_index_from_title(movie_user_likes)
if movie_index == -1:
  print("Sorry movie is not in our database")
else:

  similar_movies =  list(enumerate(cosine_sim[movie_index]))

  ##Get a list of similar movies in descending order of similarity score
  sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]

  ##Print titles of first 50 movies

  i=0
  print("Top 5 similar movies to "+movie_user_likes+" are:\n")
  for element in sorted_similar_movies:
      print(get_title_from_index(element[0]))
      i=i+1
      if i>5:
          break
