from neo4j import GraphDatabase
from bme680 import BME680
import time

# Set up the Neo4j driver
uri = "neo4j+s://41275b2a.databases.neo4j.io"
driver = GraphDatabase.driver(uri, auth=("neo4j", "3DXXXXXXXXXXXXXXXaM"))

# Set up the BME680 sensor
sensor = BME680()

# Define a function to create a sensor reading node in Neo4j
def create_sensor_reading(tx, temperature, humidity, pressure, gas):
    tx.run("CREATE (:SensorReading {temperature: $temperature, humidity: $humidity, pressure: $pressure, gas: $gas, timestamp: $timestamp})",
           temperature=temperature, humidity=humidity, pressure=pressure, gas=gas, timestamp=int(time.time()))

# Generate and insert sensor readings into Neo4j every 5 seconds
while True:
    if sensor.get_sensor_data():
        temperature = round(sensor.data.temperature, 2)
        humidity = round(sensor.data.humidity, 2)
        pressure = round(sensor.data.pressure, 2)
        gas = round(sensor.data.gas_resistance, 2)

        with driver.session() as session:
            session.write_transaction(create_sensor_reading, temperature, humidity, pressure, gas)
            print(f"Inserted sensor reading - temperature: {temperature}, humidity: {humidity}, pressure: {pressure}, gas: {gas}")
    else:
        print("Error reading BME680 sensor data.")

    time.sleep(5)
