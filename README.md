![stars](https://img.shields.io/github/stars/collabnix/bme680-jetson-neo4j)
![forks](https://img.shields.io/github/forks/collabnix/bme680-jetson-neo4j)
![Discord](https://img.shields.io/discord/1020180904129335379)
![issues](https://img.shields.io/github/issues/collabnix/bme680-jetson-neo4j)
![Visitor count](https://shields-io-visitor-counter.herokuapp.com/badge?page=collabnix.bme680-jetson-neo4j)
![Twitter](https://img.shields.io/twitter/follow/collabnix?style=social)



# Storing BME680 Sensor data on Neo4j Graph Database and visualizing it using Docker Extension

<img width="941" alt="image" src="https://user-images.githubusercontent.com/34368930/222442463-c9e4ed08-4554-48d5-96e6-513b2f2d5edd.png">


Graph databases excel at representing complex relationships between data points, which can be useful in sensor data analysis.For example, if you have multiple sensors and want to understand how they are related, a graph database can help you model those relationships and perform queries to find patterns or anomalies in the data. It can also be useful for tracking the history of sensor readings and identifying trends over time.

Here's a project that shows how one can fetch sensor values from BME680, push it to Neo4j Graph database and display it using neo4j Docker Extension.


## Pre-requisite

### Hardware Requirements:

Jetson Nano: 2GB Model ($59)
A 5V 4Amp charger
128GB SD card
BME680 sensors

### Software Requirements:

- Neo4j Cloud Instance
- Neo4j Docker Extension
- Grafana Docker Extension


## Setting up NVIDIA Jetson Nano



- Jetson SD card image from [NVIDIA](https://developer.nvidia.com/embedded/downloads)
- Etcher software installed on your system 
- Preparing Your Jetson Nano for OS Installation 
- Unzip the SD card image downloaded from https://developer.nvidia.com/embedded/downloads. 
- Insert the SD card into your system. 
- Bring up the Etcher tool and select the target SD card to which you want to flash the image.

![image](https://user-images.githubusercontent.com/34368930/222421140-13b8ca21-f1a2-4727-aba6-db29e502f0b6.png)


### Getting Your Sensors Working

Using Grove Hat, you can plugin BME680 sensor to I2C as shown:

![image](https://user-images.githubusercontent.com/34368930/222420031-43909bf3-bf88-460b-a03e-f34f03498ee2.png)


After wiring the sensors, we recommend running I2C detection with i2cdetect to verify that you see the device: in our case it shows 76. Please note that the sensor communicates with a microcontroller using I2C or SPI communication protocols.

```
$ i2cdetect -r -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- 76 --
```


## Bringing up Neo4j Cloud Instance

Visit [this link](https://neo4j.com/cloud/platform/aura-graph-database/) to create a free neo4j hosted graph database


![image](https://user-images.githubusercontent.com/34368930/222420312-f603386a-96c6-4972-b234-39609169360f.png)


## Docker Desktop 


We'll be using [neo4j Docker Extension](https://github.com/collabnix/neo4j-docker-extension) to connect to the remote neo4j Cloud hosted instance.

<img width="1365" alt="image" src="https://user-images.githubusercontent.com/34368930/222422058-452a3464-e5c7-4b42-9943-9ec4f349844b.png">


## Cloning the Repository

```
 git clone https://github.com/collabnix/bme680-jetson-neo4j
 cd bme680-jetson-neo4j
```

## Importing neo4j Python Module

You can install the Neo4j driver for Python using pip:

```
pip install neo4j
```

## A Sample Python Script for Sensors

This creates a new node with the label "SensorReading" and the specified properties. You can then query the database to retrieve sensor data and perform analysis or visualization.




```
from neo4j import GraphDatabase
  
driver = GraphDatabase.driver("neo4j+s://c9fafc6e.databases.neo4j.io", auth=("neo4j", "OgIO99y7E6vxXXXXXXXXXXHrJsTY"))

with driver.session() as session:
    session.run("CREATE (:SensorReading {sensor_id: 'sensor1', timestamp: datetime(), value: 23.4})")
```

## Running the Script

For this demonstration, I shall be using all the sensor values.
This script generates random values for temperature, humidity, pressure, and gas using the random library, and then inserts these values into Neo4j along with a timestamp. You can modify the ranges for the random values by changing the arguments to random.uniform() as needed.

```
python3 sensorloader.py
```

```
Inserted sensor reading - temperature: 26.68, humidity: 41.35, pressure: 1008.6, gas: 3110.63
Inserted sensor reading - temperature: 12.42, humidity: 49.71, pressure: 1149.34, gas: 4815.11
Inserted sensor reading - temperature: 27.73, humidity: 77.2, pressure: 1081.24, gas: 4737.95
Inserted sensor reading - temperature: 19.22, humidity: 50.17, pressure: 958.73, gas: 516.57
```

In this modified script, we import the BME680 class from the bme680 library and create an instance of the class named sensor. We also modify the generate_sensor_data function to read sensor data from the sensor object.

Then, inside the loop, we use the sensor.get_sensor_data() method to read the sensor data and store it in the temperature, humidity, pressure, and gas variables. We round the values to two decimal places using the round function.

We then use the create_sensor_reading function to insert the sensor data into Neo4j, using the same format as before. Finally, we print a message indicating the values of the newly inserted sensor reading.

Note that the get_sensor_data() method may return False if there is an error reading the sensor data, so we add a check for this and print an error message if necessary.


## Fetching co2, no2 gases

- The BME680 sensor measures the concentration of several different gases, including volatile organic compounds (VOCs), carbon monoxide (CO), and nitrogen dioxide (NO2), in addition to measuring temperature, humidity, and pressure.
- To fetch the concentration of these gases from the sensor, you can use the get_sensor_data() method of the BME680 class, which returns a BME680Data object that contains the latest sensor readings. 
- You can then access the gas concentration values from the BME680Data object using the following attributes:
   - gas_resistance: The resistance of the gas sensor in ohms, which is related to the concentration of VOCs in the air.  
   - gas (a list): The concentration of different gases in parts per million (ppm), including CO and NO2.


```
python3 sensorloader_co2.py
Warming up sensor... (takes 4-5 minutes)
Starting CO2 data collection...
Inserted CO2 reading - concentration: 1294686.06
```

Please Note: The CO2 concentration of 1294686.06 ppm (parts per million) that you mentioned is quite high compared to typical indoor CO2 levels. In a well-ventilated indoor environment, the CO2 concentration should be around 400-1000 ppm. CO2 levels above 1000 ppm can cause drowsiness, headaches, and other symptoms, while levels above 5000 ppm can cause serious health effects and even death in extreme cases.

However, the interpretation of CO2 levels depends on the context and the environment in which the measurements were taken. For example, in some industrial settings, such as breweries or greenhouses, CO2 levels may be intentionally high for specific purposes. It is also important to consider other factors that may affect indoor air quality, such as humidity, ventilation, and the presence of other pollutants.




## Installing and Connecting neo4j Docker Extension to hosted neo4j Auro

```shell
git clone https://github.com/collabnix/neo4j-docker-extension
cd neo4j-docker-extension
make install
```

## Connecting to the remote neo4j instance



<img width="1508" alt="image" src="https://user-images.githubusercontent.com/313480/222407314-1c895e4c-8c27-452f-8ff9-02cc0455c0ab.png">


## Using Neo4j Data Source for Grafana

<img width="1364" alt="image" src="https://user-images.githubusercontent.com/34368930/222455775-c724e8c6-2a0b-4edc-8d16-cfb2252a59ee.png">

<img width="1370" alt="image" src="https://user-images.githubusercontent.com/34368930/222463241-8500a4b4-0d75-4cd3-bce2-83250b360da2.png">


Query:

```
MATCH (sr:SensorReading)
WHERE sr.timestamp >= $timeFrom AND sr.timestamp <= $timeTo
RETURN sr.timestamp as time, sr.temperature as temp, sr.humidity as hum, sr.pressure as press, sr.gas as gas_res
ORDER BY sr.timestamp ASC
```

<img width="1510" alt="image" src="https://user-images.githubusercontent.com/34368930/224379370-f8b43358-fb27-408b-aa74-51c6a0caaf4f.png">



## Sample Query

### Pressure

```css
MATCH (n) 
WHERE n.pressure IS NOT NULL
RETURN DISTINCT "node" as entity, n.pressure AS pressure LIMIT 25
UNION ALL 
MATCH ()-[r]-() 
WHERE r.pressure IS NOT NULL
RETURN DISTINCT "relationship" AS entity, r.pressure AS pressure LIMIT 25;
```

<img width="1029" alt="image" src="https://user-images.githubusercontent.com/34368930/222948945-63f7ec7d-9e02-48fd-9f9c-bcf0c3af62df.png">


### Explanation:

This is a Neo4j query written in the Cypher query language.

The query consists of two parts, separated by the "UNION ALL" keyword:

The first part of the query selects all nodes in the graph where the "pressure" property is not null, and returns the value of the "pressure" property for each node. The results are labeled with the string "node" as the entity and the "pressure" value.

The second part of the query selects all relationships in the graph where the "pressure" property is not null, and returns the value of the "pressure" property for each relationship. The results are labeled with the string "relationship" as the entity and the "pressure" value.

Both parts of the query use the "DISTINCT" keyword to ensure that only unique values are returned, and the "LIMIT" keyword to limit the number of results to 25.

Overall, the query returns a list of up to 25 pressure values from either nodes or relationships in the graph, along with an indicator of whether each value came from a node or a relationship.


### Temperature

```css
MATCH (n) 
WHERE n.temperature IS NOT NULL
RETURN DISTINCT "node" as entity, n.temperature AS temperature LIMIT 25
UNION ALL 
MATCH ()-[r]-() 
WHERE r.temperature IS NOT NULL
RETURN DISTINCT "relationship" AS entity, r.temperature AS temperature LIMIT 25;
```

<img width="575" alt="image" src="https://user-images.githubusercontent.com/34368930/222948922-1ba55db7-d40e-4b40-9b2b-ed79eb94fdc2.png">


### Explanation

This is a Neo4j query written in the Cypher query language.

The query is similar to the previous one, but instead of selecting nodes and relationships based on the "pressure" property, it selects nodes and relationships based on the "temperature" property.

The first part of the query selects all nodes in the graph where the "temperature" property is not null, and returns the value of the "temperature" property for each node. The results are labeled with the string "node" as the entity and the "temperature" value.

The second part of the query selects all relationships in the graph where the "temperature" property is not null, and returns the value of the "temperature" property for each relationship. The results are labeled with the string "relationship" as the entity and the "temperature" value.

Both parts of the query use the "DISTINCT" keyword to ensure that only unique values are returned, and the "LIMIT" keyword to limit the number of results to 25.

Overall, the query returns a list of up to 25 temperature values from either nodes or relationships in the graph, along with an indicator of whether each value came from a node or a relationship.


## Humidity

```css
MATCH (n) 
WHERE n.humidity IS NOT NULL
RETURN DISTINCT "node" as entity, n.humidity AS humidity LIMIT 25
UNION ALL 
MATCH ()-[r]-() 
WHERE r.humidity IS NOT NULL
RETURN DISTINCT "relationship" AS entity, r.humidity AS pressure LIMIT 25;
```



## Understanding the Relationship

Sure, here is an example of how you might model a BME680 sensor and its readings in Neo4j:

First, you would create a "Sensor" node to represent your BME680 sensor. This node might have properties like "name" and "manufacturer", as well as any other information you want to store about the sensor.

```css
CREATE (:Sensor {name: 'BME680', manufacturer: 'Bosch'})
```

Next, you would create a "Timestamp" node to represent a particular point in time when a reading was taken. This node might have a "timestamp" property that stores the date and time the reading was taken.

```css
CREATE (:Timestamp {timestamp: datetime()})
```

Then, you would create a "READS" relationship between the Sensor node and the Timestamp node, with properties like "temperature", "pressure", "humidity", etc., representing the values that were read from the sensor at that time. For example, to create a reading where the temperature is 25 degrees Celsius, the pressure is 1000 hPa, and the humidity is 50%, you might use a query like this:

```css
MATCH (s:Sensor {name: 'BME680'}), (t:Timestamp)
CREATE (s)-[:READS {temperature: 37.0, pressure: 1168.83, humidity: 37.23}]->(t)
```

<img width="1505" alt="image" src="https://user-images.githubusercontent.com/34368930/222949941-236cd924-3ac8-4ed8-98a5-9b2a8de795e2.png">


This query creates a "READS" relationship between the Sensor node and the Timestamp node, with properties for temperature, pressure, and humidity set to the values 25, 1000, and 50, respectively.

You can then use Cypher queries to retrieve readings from the database, filter them based on criteria like time range or sensor type, and visualize the data in various ways using tools like Neo4j Bloom or other visualization tools.


## FAQs

### What if I have millions of sensors?

If you have millions of sensors, there are a few considerations to keep in mind:

- Scaling your data pipeline: As the number of sensors increases, you need to ensure that your data pipeline can handle the increased load. You may need to optimize your code or use distributed computing frameworks such as Apache Spark to handle the increased data volume.
- Storing the data: When dealing with large volumes of data, you need to consider the storage mechanism. Neo4j is a graph database that is designed to handle complex relationships between data points, but it may not be the best choice for storing massive amounts of data. You may need to consider using a distributed storage system like Apache Hadoop or Apache Cassandra.
- Querying the data: With millions of sensors, querying the data can become a bottleneck. You may need to use indexing or caching mechanisms to speed up queries.
- Hardware requirements: With an increased number of sensors, you may need to invest in more powerful hardware to handle the increased load. This includes upgrading your Jetson Nano or investing in more powerful servers.

Scaling to millions of sensors requires careful planning and optimization of your data pipeline, storage mechanism, query performance, and hardware infrastructure.


### Scaling Your Data Pipeline

Here are a few examples of how you can scale your data pipeline to handle millions of sensors:

### Using parallel processing

One way to scale your data pipeline is to use parallel processing. This involves splitting up the data processing into smaller chunks that can be processed simultaneously on multiple CPU cores or even across multiple machines. Here's an example using the Python multiprocessing library:

```
from multiprocessing import Pool

def process_sensor_data(sensor_data):
    # process sensor data here
    return processed_data

if __name__ == '__main__':
    with Pool(processes=4) as pool:
        # read in sensor data
        sensor_data = read_sensor_data()
        
        # split the data into chunks
        chunk_size = len(sensor_data) // 4
        data_chunks = [sensor_data[i:i+chunk_size] for i in range(0, len(sensor_data), chunk_size)]
        
        # process the data in parallel
        results = pool.map(process_sensor_data, data_chunks)
        
        # combine the results
        processed_data = combine_results(results)
```

In this example, we use the Pool class from the multiprocessing library to create a pool of worker processes. We then split the sensor data into four chunks and use the map function to process each chunk in parallel. The results are then combined into a single output.

### Using distributed computing frameworks

Another way to scale your data pipeline is to use distributed computing frameworks like Apache Spark. Spark allows you to process large volumes of data across a cluster of machines, which can dramatically increase your processing speed. Here's an example using PySpark:


```
from pyspark import SparkContext

def process_sensor_data(sensor_data):
    # process sensor data here
    return processed_data

if __name__ == '__main__':
    sc = SparkContext(appName='sensor_data_processing')
    
    # read in sensor data as an RDD
    sensor_data = sc.parallelize(read_sensor_data())
    
    # process the data in parallel
    processed_data = sensor_data.map(process_sensor_data)
    
    # collect the results
    results = processed_data.collect()
    
    # combine the results
    combined_results = combine_results(results)
    
    # stop the Spark context
    sc.stop()
```

In this example, we use PySpark to process the sensor data. We read in the data as an RDD (Resilient Distributed Dataset), which allows us to process the data in parallel across a cluster of machines. We use the map function to process each data point and then collect the results and combine them into a single output. Finally, we stop the Spark context.

These are just a few examples of how you can scale your data pipeline to handle millions of sensors. The specific approach you choose will depend on your data processing requirements, available hardware, and other factors.


## Storing the Data

Here are a few ways you can store data for millions of sensors:

### Relational databases

Relational databases are a common choice for storing large volumes of data. They offer a structured way to store and retrieve data, and many tools and libraries are available to work with them. Examples of popular relational databases include PostgreSQL, MySQL, and Microsoft SQL Server.
Here is an example of using PostgreSQL to store sensor data:

```
import psycopg2

conn = psycopg2.connect(
    host="yourhost",
    database="yourdatabase",
    user="yourusername",
    password="yourpassword"
)

cursor = conn.cursor()

# create a table to store sensor data
cursor.execute("CREATE TABLE sensor_data (sensor_id INT, timestamp TIMESTAMP, value FLOAT)")

# insert data into the table
sensor_id = 1
timestamp = '2022-03-15 12:00:00'
value = 25.4
cursor.execute("INSERT INTO sensor_data (sensor_id, timestamp, value) VALUES (%s, %s, %s)", (sensor_id, timestamp, value))

# commit changes and close the connection
conn.commit()
cursor.close()
conn.close()
```

### NoSQL databases

NoSQL databases are designed to handle large volumes of unstructured or semi-structured data. They are often used for big data applications and can scale horizontally to handle massive amounts of data. Examples of popular NoSQL databases include Apache Cassandra, MongoDB, and Amazon DynamoDB.
Here is an example of using MongoDB to store sensor data:

```
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

# create a database and collection to store sensor data
db = client["sensor_data"]
collection = db["data_points"]

# insert data into the collection
data_point = {"sensor_id": 1, "timestamp": "2022-03-15 12:00:00", "value": 25.4}
collection.insert_one(data_point)
```

### Distributed file systems

Distributed file systems are designed to store and manage large volumes of data across multiple machines. They are often used in big data applications and can scale horizontally to handle massive amounts of data. Examples of popular distributed file systems include Apache Hadoop HDFS and Amazon S3.
Here is an example of using Hadoop HDFS to store sensor data:

```
import pyarrow as pa
import pyarrow.parquet as pq
import hdfs

client = hdfs.InsecureClient('http://localhost:9870')

# create a PyArrow table to store sensor data
data_table = pa.Table.from_pydict({"sensor_id": [1], "timestamp": ["2022-03-15 12:00:00"], "value": [25.4]})

# write the table to HDFS as a Parquet file
with client.write('sensor_data.parquet', replication=1) as writer:
    pq.write_table(data_table, writer)
```

## Quesring data for Millions of Sensors

Here are a few examples of how you can query data for millions of sensors:

## Relational databases

To query data from a relational database, you can use SQL. SQL provides a rich set of operations for filtering, grouping, and aggregating data. Examples of SQL operations include SELECT, WHERE, GROUP BY, and JOIN.
Here is an example of querying sensor data from a PostgreSQL database:

```
import psycopg2

conn = psycopg2.connect(
    host="yourhost",
    database="yourdatabase",
    user="yourusername",
    password="yourpassword"
)

cursor = conn.cursor()

# query the maximum value for each sensor
cursor.execute("SELECT sensor_id, MAX(value) FROM sensor_data GROUP BY sensor_id")
rows = cursor.fetchall()
for row in rows:
    print(f"Sensor {row[0]} has a maximum value of {row[1]}")

# close the cursor and connection
cursor.close()
conn.close()
```

### NoSQL databases

To query data from a NoSQL database, you can use the database's native query language. Examples of query languages include Cassandra Query Language (CQL), MongoDB Query Language (MQL), and Amazon DynamoDB Query Language.
Here is an example of querying sensor data from a MongoDB database:

```
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

# get the sensor data collection
collection = client["sensor_data"]["data_points"]

# query the maximum value for each sensor
rows = collection.aggregate([
    {"$group": {"_id": "$sensor_id", "max_value": {"$max": "$value"}}}
])
for row in rows:
    print(f"Sensor {row['_id']} has a maximum value of {row['max_value']}")
```

### Distributed file systems

To query data from a distributed file system, you can use tools like Apache Spark or Apache Hive. These tools provide a SQL-like interface to query data stored in Hadoop HDFS or Amazon S3.
Here is an example of querying sensor data from a Parquet file stored in Hadoop HDFS using PySpark:

```
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SensorDataQuery").getOrCreate()

# read the sensor data Parquet file into a PySpark DataFrame
df = spark.read.parquet("hdfs://localhost:9000/sensor_data.parquet")

# query the maximum value for each sensor
df.groupBy("sensor_id").max("value").show()
```




