Introduction
============

Problem
-------
We will investigate and analyze the attributes affecting the sales of video games and make prediction on future sales.

Dataset
-------
This data-set contains a list of video games with sales greater than 100,000 copies of video games. The features are,
ranking of overall sales,the games name,platform of the games release (i.e. PC,PS4, etc.),year of the game's release,genre of the game,publisher of the game,sales in North America (in millions),sales in Europe (in millions),sales in Japan (in millions),sales in the rest of the world (in millions), and total worldwide sales. We are going to test some machine learning techniques to train our model and compare their accuracy based on the existing data-set.


The features in the data lend themselves to categorical analysis, especially variable conditioning, where we can observe and calculate the effect of one variable conditioned on others. For example, it is easy to ask if a certain genre is popular conditioned on a certain region, and allows us to chain these variables to ask specific questions, and analyze trends like success of different genres on platforms in different regions over time. 

Dataset link
------------
https://www.kaggle.com/gregorut/videogamesales


User Story
----------


As a sales director of video games, I want to know the history of video games sales by genres and regions so that I can make a decision on what types of video games we need to produce and direct the distribution of our products. Furthermore, I want to use the history to identify trends that would help me make market decisions for a future, like not investing in platforms that are not showing a growing trend in certain regions. Given that the sales manager want to find related sales information , when he/she selects feature(s), then our platform produces a visual analysis as well as future predictive modelling for features.
