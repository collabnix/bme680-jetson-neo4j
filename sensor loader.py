from neo4j import GraphDatabase
import time
import random

# Set up the Neo4j driver
uri = "neo4j+s://c9fafc6e.databases.neo4j.io"
driver = GraphDatabase.driver(uri, auth=("neo4j", "OgXXXXJsTY"))

# Define a function to generate random sensor data
def generate_sensor_data():
    temperature = round(random.uniform(10, 40), 2)
    humidity = round(random.uniform(20, 80), 2)
    pressure = round(random.uniform(800, 1200), 2)
    gas = round(random.uniform(0, 5000), 2)
    return temperature, humidity, pressure, gas

# Define a function to create a sensor reading node in Neo4j
def create_sensor_reading(tx, temperature, humidity, pressure, gas):
    tx.run("CREATE (:SensorReading {temperature: $temperature, humidity: $humidity, pressure: $pressure, gas: $gas, timestamp: $timestamp})",
           temperature=temperature, humidity=humidity, pressure=pressure, gas=gas, timestamp=int(time.time()))

# Generate and insert random sensor readings into Neo4j every 5 seconds
while True:
    with driver.session() as session:
        temperature, humidity, pressure, gas = generate_sensor_data()
        session.write_transaction(create_sensor_reading, temperature, humidity, pressure, gas)
        print(f"Inserted sensor reading - temperature: {temperature}, humidity: {humidity}, pressure: {pressure}, gas: {gas}")
    time.sleep(5)
