# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 01:49:44 2022

@author: Nico
"""

import pandas as pd
import re
import os


#%%
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%%
# links_small_df = pd.read_csv('links_small.csv')
root = '../datasets/'
ratings_small_df = pd.read_csv(root+'ratings_small.csv')
movies_metadata_df = pd.read_csv(root+'movies_metadata.csv')
keywords_df = pd.read_csv(root+'keywords.csv')

#%%
movies_metadata_df.drop(columns=['adult', 'belongs_to_collection', 'homepage','imdb_id', 'overview','poster_path','tagline','status','original_title','video', 'popularity','revenue','spoken_languages'],inplace=True) #se podria quitar 'title' en vez de 'original_title', depende del idioma del usuario
movies_metadata_df.rename(columns={'id': 'movieId'},inplace=True)
# pd.to_datetime(movies_metadata_df['release_date'])
movies_metadata_df['budget'] = movies_metadata_df['budget'].astype('int64', copy=False)
movies_metadata_df['movieId'] = movies_metadata_df['movieId'].astype('string', copy=False)

# to_float = ['popularity']

# hay q ver que hacer con 'genre'
# genres = full_df['genres'].tolist()



# to_str = ['genres','original_language','production_companies','spoken_languages','title']
# con1.loc[:,'available'] = con1.loc[:,'available'].map({'t': 1, 'f': 0})


ratings_small_df.drop(columns=['timestamp'],inplace=True)
ratings_small_df['movieId'] = movies_metadata_df['movieId'].astype('string', copy=False)

full_df = pd.merge(ratings_small_df,movies_metadata_df, on='movieId')


for i in range(len(full_df['genres'])):
    genres = full_df['genres'][i]
    numbers = re.findall(r'\d+', genres)
    ids = ','.join([n for n in numbers])
    full_df.loc[i,'genres']=ids
        

#%%
print(movies_metadata_df.info())
print(ratings_small_df.info())
print(full_df.info())
print(full_df['genres'])
print(len(ratings_small_df.duplicated()==False))
print(movies_metadata_df.info())
a = full_df['genres'].tolist()
print(full_df.loc[0]['rating'])
#%%
full_df[0:100].to_excel('ooutput.xlsx')

