# Movie-Recomendator-pending
The aim of this project is to build a Movie Recommenator system based on clustering. 

The idea is: 
1. given an user search its n closests users.
2. Pic the movie which hasnt been seen by the new user and has the highest mean reviews of the other closests users

## DATA

First of all we need data from different users. I used the dataset available in kaggle called ['The Movie Dataset'](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset). As a [Filmaffinity](https://www.filmaffinity.com/es/main.html) user I wanted to retrieve my own reviews 
from this platform so I made a web scrapping code to obtain the reviews from any user. 

I later tried to randomly scrap users reviews to make my own Filmaffinity Reviews DB but I´m unable since each user is defined by a 7 digit number and it is almost imposible to randomly pic a number wich matches an user.


