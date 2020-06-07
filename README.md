# Amazon Recommender System Application
This is a Recommender System application for Amazon customers.
 
 
[![Documentation](https://img.shields.io/badge/docs-passing-NeonGreen.svg)](https://sites.google.com/a/eng.ucsd.edu/capstone-2020-amazondata/)
[![Demo](https://img.shields.io/badge/status-staging-Red.svg)](https://sites.google.com/a/eng.ucsd.edu/capstone-2020-amazondata/)
[![GitHub stars](https://img.shields.io/github/stars/j4baek/dse260-CapStone-Amazon.svg)](https://github.com/j4baek/dse260-CapStone-Amazon/stargazers)
[![UCSD](https://img.shields.io/badge/Data_Science-UCSD-Blue.svg)](https://sites.google.com/a/eng.ucsd.edu/capstone-2020-amazondata/)
[![MIT license](https://img.shields.io/badge/License-MIT-Yellow.svg)](https://lbesson.mit-license.org/)
 
 
 
## Overview
A personalized ‘shop-by-style’ experience using DeepLearning on Amazon.
 
 
<!-- ![](docs/images/chat.gif) -->
 
## Table of Contents
 
- [Amazon Recommender System Application](#amazon-recommender-system-application)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Architecture](#architecture)
  - [Models](#models)
  - [GraphDB](#graphdb)


## Architecture
![Architecture](./img/AmazonDataPipeline.png)
 

## Models
The following models that have been trained and stored under the individual directories.
- Keras-DeepRecommender-Shoes
- Image_based_recommender
- word2vec_model.zip


## GraphDB
The Neo4j graph databse is used to store the results of the models and provide recomendations in real time. Example code for deploymnet and queries can be found under `GraphDB` directory.

