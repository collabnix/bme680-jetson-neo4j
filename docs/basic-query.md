

## Adding data

Suppose we want to insert some data about people and cities into our social network database. Here's an example Cypher query that inserts two Person nodes and one City node into the database, and creates a LIVES_IN relationship between the people and the city:

```
CREATE (john:Person {name: 'John Smith', age: 30})
CREATE (jane:Person {name: 'Jane Doe', age: 25})
CREATE (newyork:City {name: 'New York'})
CREATE (john)-[:LIVES_IN]->(newyork)
CREATE (jane)-[:LIVES_IN]->(newyork)
```

## Running Queries


Cypher query that retrieves the name and age of all people who live in a given city:


```
MATCH (person:Person)-[:LIVES_IN]->(city:City {name: 'New York'})
RETURN person.name, person.age
```



<img width="782" alt="image" src="https://user-images.githubusercontent.com/34368930/224358718-c58bf9e9-f681-4dfa-a920-f73bba53b630.png">


