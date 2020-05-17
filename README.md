# Amazon Recommender System Application
This is a Recommender System application for Amazon customers.
 
 
[![Documentation](https://img.shields.io/badge/docs-passing-NeonGreen.svg)](https://sites.google.com/a/eng.ucsd.edu/capstone-2020-amazondata/)
[![Demo](https://img.shields.io/badge/status-dev-Red.svg)](https://sites.google.com/a/eng.ucsd.edu/capstone-2020-amazondata/)
[![tests](https://img.shields.io/badge/testing-fail-red.svg)](https://github.com/facebook/jest)
[![GitHub stars](https://img.shields.io/github/stars/j4baek/dse260-CapStone-Amazon.svg)](https://github.com/j4baek/dse260-CapStone-Amazon/stargazers)
[![UCSD](https://img.shields.io/badge/Data_Science-UCSD-Blue.svg)](https://sites.google.com/a/eng.ucsd.edu/capstone-2020-amazondata/)
[![MIT license](https://img.shields.io/badge/License-MIT-Yellow.svg)](https://lbesson.mit-license.org/)
 
 
 
## Overview
A personalized ‘shop-by-style’ experience using PyTorch on Amazon SageMaker and Amazon Neptune
 
 
<!-- ![](docs/images/chat.gif) -->
 
## Table of Contents
 
- [Amazon Recommender System Application](#amazon-recommender-system-application)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Architecture](#architecture)
  - [Components](#components)
  - [Models](#models)
  - [Usage](#usage)
    - [Installation](#installation)
    - [Serverless ETl](#serverless-etl)
 
 
## Architecture
![Architecture](./img/AmazonDataPipeline.png)
 
## Components
The following components refer to modules located in the `src` dir.
 
|  | Module | Description |
| ---- | ------ | -------- |
| 0 | Set up | Prepares local and cloud env. |
| 1 | Data Loader | Loads batch data set to amazon s3. |
| 2 | Data Processor | Prepared product data for modeling. <br>- Indexer <br> - Transformer|
| 3 | EDA |  |
| 4 | Product Similarity Model | <dl><dt>**Utilities:**</dt> <ul><li>Modeler</li><li>Inputer</li><li>Outputer</li><li>Predictor</li></ul></dl> |
| 5 | Data Trainer | |
| 6 | Optimizer |  |
| 7 | Model Deployer |  |
| 8 |  Recommender API | Programmatic access to the system |
| 9 | Recommender Web Site | User interface to the recommender system. |
 

## Models
The following models that have been trained and stored under the `src/models/` directory. Model versions and benchmarks are evaluated using MSE for rating predictions and include execution times. Three progressive datasets are used to measure the scalability as the model progress to productiion. Models can be evaluated locally using the 100k dataset. All other evaluations are executed in an aws cloud envoinrment. The `src/cf/` directory containes scripts used for automated deployments. 



**Dataset:** Amazon_Clothing_Shoes_and_Jewelry_100k

| Method                             | Accuracy            | Time                 | 
| ---------------------------------- | ------------------- | ------------------   | 
| Baseline                           | 1.1630374059367858  | 0.004736900329589844 |
| Weighted Ratings Heuristic         | 1.40054874327075    | 1.8000781536102295  | 
| Product KNN                        | 1.2433453027128647  | 5.375831842422485   | 
| User KNN                           | 1.4744309982698536  | 84.04179906845093  |


```
cosine_sim(𝑢,𝑣)=∑𝑖∈𝐼𝑢𝑣𝑟𝑢𝑖⋅𝑟𝑣𝑖∑𝑖∈𝐼𝑢𝑣𝑟2𝑢𝑖‾‾‾‾‾‾‾√⋅∑𝑖∈𝐼𝑢𝑣𝑟2𝑣𝑖‾‾‾‾‾‾‾√
or

cosine_sim(𝑖,𝑗)=∑𝑢∈𝑈𝑖𝑗𝑟𝑢𝑖⋅𝑟𝑢𝑗∑𝑢∈𝑈𝑖𝑗𝑟2𝑢𝑖‾‾‾‾‾‾‾√⋅∑𝑢∈𝑈𝑖𝑗𝑟2𝑢𝑗‾‾‾‾‾‾‾√
```

**Dataset:** Amazon_Clothing_Shoes_and_Jewelry_1M

| Method                             | Accuracy            | Time                 | 
| ---------------------------------- | ------------------- | ------------------   | 
| Baseline                           |                     |                      |
| Weighted Ratings Heuristic         |                     |                      | 
| Product KNN                        |                     |                      | 
| User KNN                           |                     |                      |


**Dataset:** Amazon_Clothing_Shoes_and_Jewelry

| Method                             | Accuracy            | Time                 | 
| ---------------------------------- | ------------------- | ------------------   | 
| Baseline                           |                     |                      |
| Weighted Ratings Heuristic         |                     |                      | 
| Product KNN                        |                     |                      | 
| User KNN                           |                     |                      |

 
## Usage
  
### Installation
- Install spark
- requirments.txt
- aws cli (optional)
- Neo4J DB
 

### Serverless ETl
Crawler output for raw metadata.
![ETL2](./img/RawMetaDataCralwerOutput.png)
 
Transforming raw data for analysis.
![ETL](./img/MetaDataTransform.png)
 
