// The script contains examples of quries used for amazon
// neo4j graph db.

// Load Review Scores Pedictions
LOAD CSV WITH HEADERS FROM 'file:///Shoes_for_100_users_per_100_products_prediction_Ver3.csv' AS row
MERGE (i:Item {
    id: toString(row.item_id), 
    asin: toString(row.asin), 
    url: toString(row.url), 
    title: toString(row.product_title)
})
MERGE (u:User {
    id: toString(row.user_id)
})
MERGE (u)-[x:PURCHASED {
    rating: toInteger(row.score), 
    rating_prediction: toInteger(row.predicted_score)
}]->(i)


// Load IMAGE Similarity
LOAD CSV WITH HEADERS FROM "file:///RESULT_image_recommended_product_50k_for_100JH_ver3_all.csv" AS row
MERGE (item1:Item {asin: row.given_product, given_product_img_url: row.given_product_img_url})
MERGE (item2:Item {asin: row.recommended_product, recommended_product_img_url: row.recommended_product_img_url})
MERGE (item1)-[x:IMG_SIM {similarity: toInteger(row.similarity_score)}]->(item2)

// check valid data 
LOAD CSV WITH HEADERS FROM "file:///img_50k_100.csv" AS row
MATCH (item1: Item {asin: row.given_product}), (item2: Item {asin: row.recommended_product})
WHERE item1.url <> row.given_product_img_url OR item2.url <> row.recommended_product_img_url
RETURN item1, item2, row 

// Calculate error 
MATCH (u:User)-[r:PURCHASED]->(i:Item)
WHERE r.rating-r.rating_prediction < 1
with r.rating-r.rating_prediction as error 
RETURN u,p,i, error LIMIT 25

// check missing img
MATCH (item1:Item)
WHERE item1.url is null
RETURN item1

// query second degree items for similar users
MATCH (u:User)-[:PURCHASED]->(item1:Item)
WHERE u.url IS NULL
NOT EXISTS(u.url)
RETURN u, item1

// count items purchased by user
MATCH (u1:User)-[x:PURCHASED]->(i:Item)
RETURN u1.id as user, count(i) as total_items_purchased
ORDER by total_items_purchased DESC;

// count users that bought item 
MATCH (u1:User)-[x:PURCHASED]->(i:Item)
RETURN i.id as item, count(u1) as total_users_bought
ORDER by total_users_bought DESC;

// match user id
MATCH (u:User {id: '68499'})-[p:PURCHASED]->(i:Item)
RETURN u, p, i

// match item id
MATCH (u:User)-[p:PURCHASED]->(i:Item {id: '3776'})
RETURN u, p, i

// match users who also bought items the user bought
MATCH (u:User {id: '68499'})-[:PURCHASED]->(i:Item)<-[:PURCHASED]-(u2:User)
RETURN u, i, u2 

// query second degree items for similar users
MATCH (u:User {id: '68499'})-[:PURCHASED]->(item1:Item)<-[:PURCHASED]-(u2:User)-[:PURCHASED]->(item2:Item)<-[:PURCHASED]-(u3:User)
WHERE u <> u3 AND NOT (u)-[:PURCHASED]->(:Item)<-[:PURCHASED]-(u3)
RETURN u, item1, u2, item2, u3

// return items both users rated
MATCH  (u1:User {id:"68499"})-[p1:PURCHASED]->(i:Item)<-[p2:PURCHASED]-(u2:User {id:"30209"})
RETURN i.id AS item, p1.rating AS `U1 Rating`, p2.rating AS `U2 Rating`

// query second degree items for similar users
MATCH (u:User {id: '68499'})-[:PURCHASED]->(item1:Item)<-[:PURCHASED]-(u2:User)-[:PURCHASED]->(item2:Item)<-[:PURCHASED]-(u3:User),
(u)-[s:SIMILARITY]-(u2)
WHERE u <> u3 AND NOT (u)-[:PURCHASED]->(:Item)<-[:PURCHASED]-(u3)
WITH item1, s.similarity AS userSim
ORDER BY userSim DESC
LIMIT 5
RETURN item1.id AS Neighbor, userSim AS Similarity

// create cos similarity
MATCH (u1:User)-[x:PURCHASED]->(i:Item)<-[y:PURCHASED]-(u2:User)
WITH  SUM(x.rating * y.rating) AS xyDotProduct,
      SQRT(REDUCE(xDot = 0.0, a IN COLLECT(x.rating) | xDot + a^2)) AS xLength,
      SQRT(REDUCE(yDot = 0.0, b IN COLLECT(y.rating) | yDot + b^2)) AS yLength,
      u1, u2
MERGE (u1)-[s:SIMILARITY]-(u2)
SET   s.similarity = xyDotProduct / (xLength * yLength)

// Eval sim score
MATCH  (u1:User {id: '68499'})-[s:SIMILARITY]-(u2:User {id: '30209'})
RETURN s.similarity AS `Cosine Similarity`

// User similarity model 
MATCH (u1:User)-[x:PURCHASED]->(i:Item)<-[y:PURCHASED]-(u2:User),
      (u1)-[:SIMILARITY]-(u2)
RETURN u1, u2, i LIMIT 3;

// Get Nearest Neighbors
MATCH (u1:User)-[x:PURCHASED]->(i:Item), (u1)-[s:SIMILARITY]-(u2:User {id:'5733'})
WITH u2, s.similarity AS sim
ORDER BY sim DESC
LIMIT 5
RETURN u1.id AS Neighbor, sim AS Similarity

// Most similar users using Cosine similarity
MATCH (u1:User {id: "68499"})-[x:PURCHASED]->(i1:Item)<-[y:PURCHASED]-(u2:User)
WITH COUNT(i1) AS numberitems, SUM(x.rating * y.rating) AS xyDotProduct,
SQRT(REDUCE(xDot = 0.0, a IN COLLECT(x.rating) | xDot + a^2)) AS xLength,
SQRT(REDUCE(yDot = 0.0, b IN COLLECT(y.rating) | yDot + b^2)) AS yLength,
u1, u2 
RETURN u1.id, u2.id, xyDotProduct / (xLength * yLength) AS sim
ORDER BY sim DESC
LIMIT 10;

// make recomendations to user
MATCH (u1:User)-[x:PURCHASED]->(i:Item), (u1)-[s:SIMILARITY]-(u2:User {id:"68499"})
WHERE NOT((u2)-[:PURCHASED]->(i))
WITH i, s.similarity AS similarity, x.rating AS rating
ORDER BY i.title, similarity DESC
WITH i.title AS item, COLLECT(rating)[0..3] AS ratings
WITH item, REDUCE(s = 0, i IN ratings | s + i)*1.0 / LENGTH(ratings) AS reco
ORDER BY reco DESC
RETURN item AS Item, reco AS Recommendation

// Neo4j sim use cosine algorithm 
MATCH (p1:User {id: '68499'})-[x:PURCHASED]->(Item)<-[x2:PURCHASED]-(p2:User)
WHERE p2 <> p1
WITH p1, p2, collect(x.rating) AS p1Ratings, collect(x2.rating) AS p2Ratings
WHERE size(p1Ratings) > 10
RETURN p1.name AS from,
       p2.name AS to,
       algo.similarity.cosine(p1Ratings, p2Ratings) AS similarity
ORDER BY similarity DESC
