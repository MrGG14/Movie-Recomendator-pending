# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 01:49:44 2022

@author: Nico
"""

import pandas as pd
import re
import os
from sklearn.preprocessing import MultiLabelBinarizer


#%%
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%%
# links_small_df = pd.read_csv('links_small.csv')

ratings_small_df = pd.read_csv('ratings_small.csv')
movies_metadata_df = pd.read_csv('movies_metadata.csv')
keywords_df = pd.read_csv('keywords.csv')

#%%

#delete unncecessary columns
movies_metadata_df.drop(columns=['adult', 'belongs_to_collection', 'homepage','imdb_id', 'overview','poster_path','tagline','status','original_title','video', 'popularity','revenue','spoken_languages'],inplace=True) #se podria quitar 'title' en vez de 'original_title', depende del idioma del usuario

#mergin dfs
movies_metadata_df.rename(columns={'id': 'movieId'},inplace=True)
movies_metadata_df['movieId'] = movies_metadata_df['movieId'].astype('string', copy=False)


ratings_small_df.drop(columns=['timestamp'],inplace=True)
ratings_small_df['movieId'] = ratings_small_df['movieId'].astype('string', copy=False)
ratings_small_df['userId'] = ratings_small_df['userId'].astype('string', copy=False)

full_df = pd.merge(ratings_small_df,movies_metadata_df, on='movieId')
full_df['budget'] = full_df['budget'].astype('int', copy=False)
full_df['original_language'] = full_df['original_language'].astype('string', copy=False)
full_df['release_date'] = pd.to_datetime(full_df['release_date'])
#dropping genre labels, keeping just its id
# for i in range(len(full_df['genres'])):
#     genres = full_df['genres'][i]
#     numbers = re.findall(r'\d+', genres)
#     ids = ','.join([n for n in numbers])
#     full_df.loc[i,'genres']='[' + ids + ']'

def extract_ids(x):
    numbers = re.findall(r'\d+',x)
    ids = ','.join([n for n in numbers])
    return  list(ids.split(',')) 

def extract_countryId(x):
    numbers = re.findall(r"(iso_.*?)'",x)
    ids = ','.join([n for n in numbers])
    return  list(ids.split(',')) 

full_df['genres'] = full_df['genres'].apply(extract_ids)
full_df['production_companies'] = full_df['production_companies'].apply(extract_ids)
full_df['production_countries'] = full_df['production_countries'].apply(extract_countryId)
full_df['release_date'] = pd.to_datetime(full_df['release_date'])
full_df['title'] = full_df['title'].astype('string')

#create users_df
users_df  = full_df.groupby(by=['userId']).mean()

users_df['n_movies']  = full_df.groupby('userId')['rating'].count()
users_df['std_rating']  = full_df.groupby('userId')['rating'].std()
users_df['min_rating']  = full_df.groupby('userId')['rating'].min()
users_df['max_rating']  = full_df.groupby('userId')['rating'].max()
users_df['total_mins']  = full_df.groupby('userId')['runtime'].sum()
users_df['rated_movs']  = full_df.groupby('userId').apply(lambda full_df: dict(zip(full_df['movieId'], full_df['rating'])))
users_df['genres_movs']  = full_df.groupby('userId').apply(lambda full_df: dict(zip(full_df['movieId'], full_df['genres'])))
users_df = users_df.drop(columns=['runtime', 'vote_average', 'vote_count'])
users_df.rename(columns={'rating': 'avg_rating'}, inplace=1)

print(full_df.info())
print(users_df.info())

mlb = MultiLabelBinarizer()
s = users_df['rated_movs']
seen_movs = pd.DataFrame(mlb.fit_transform(s),columns=mlb.classes_, index=s.index)
users_df = pd.merge(users_df,seen_movs, on='userId')

''' 
COSAS DE PRUEBASs[1]
s


# def genre_count(x):
    
# users_df['genres_count'] = full_df.groupby(by=['userId'], axis=0)['genres'].apply(dict)
# full_df.groupby(by=['userId'], axis=0)['genres'].apply(list)
# list(full_df['genres'][0].split(','))
# dummies = full_df['genres'].str.get_dummies()
# dummies.head()        

# mlb = MultiLabelBinarizer()
# s=full_df['genres']
# pd.DataFrame(mlb.fit_transform(s),columns=mlb.classes_, index=s.index)

#%%
# print(movies_metadata_df.info())
# print(ratings_small_df['rating'])
# print(full_df.info())
# print(full_df['vote_average'])
# print(len(ratings_small_df.duplicated()==False))
# print(movies_metadata_df.info())
# a = full_df['genres'].tolist()
# print(full_df.loc[0]['rating'])
# #%%
# # full_df[0:100].to_excel('ooutput.xlsx')
# full_df['genres'].dtype
# df = pd.DataFrame(
#     {'groups':
#         [['12','3','5'],
#         ['c'],
#         ['b','c','e'],
#         ['a','c'],
#         ['b','e']]
#     }, columns=['groups'])
# df
# x = df['groups']
# x
# d=s.tolist()
# s
# mlb.fit([s])
# mlb.classes_
# pd.DataFrame(mlb.fit_transform(s),columns=mlb.classes_, index=s.index)

'''
