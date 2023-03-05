# This script assumes that you have a BME680 sensor attached to your system and that the necessary dependencies (e.g. the bme680 Python module) are installed. 
# You will need to replace the placeholder values for the Neo4j instance URL and password with the actual values for your instance.
# The script starts by setting up the Neo4j driver and the BME680 sensor. 
# It then defines a function to create a CO2 reading node in Neo4j, which takes the CO2 concentration as an input.
# Next, the script waits for the sensor to warm up by setting the gas status to enable gas measurements and waiting for 300 seconds (5 minutes).
# After that, it starts retrieving CO2 concentration data by calling sensor.get_sensor_data() in a loop. 
# If the data retrieval is successful, the CO2 concentration is calculated as sensor.data.gas_resistance / 10 and rounded to two decimal places. 
# The script then inserts a new CO2 reading node into the Neo4j database by calling the create_co2_reading function within a with driver.session() 
# as session: block.

The script runs indefinitely, sleeping for 60 seconds between each data retrieval and insertion. If there is an error retrieving the sensor data, an error message is printed to the console.
#
#
#
from neo4j import GraphDatabase
import time
import bme680

# Set up the Neo4j driver
uri = "neo4j+s://your-neo4j-instance-url-here"
driver = GraphDatabase.driver(uri, auth=("neo4j", "your-neo4j-instance-password-here"))

# Set up the BME680 sensor
sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)

# Define a function to create a CO2 reading node in Neo4j
def create_co2_reading(tx, co2_concentration):
    tx.run("CREATE (:CO2Reading {concentration: $concentration, timestamp: $timestamp})",
           concentration=co2_concentration, timestamp=int(time.time()))

# Wait for the sensor to warm up
print("Warming up sensor...")
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
time.sleep(300)

# Start retrieving CO2 concentration data and inserting it into Neo4j
print("Starting CO2 data collection...")
while True:
    if sensor.get_sensor_data():
        co2_concentration = round(sensor.data.gas_resistance / 10, 2)
        with driver.session() as session:
            session.write_transaction(create_co2_reading, co2_concentration)
            print(f"Inserted CO2 reading - concentration: {co2_concentration}")
    else:
        print("Error retrieving sensor data")
    time.sleep(60)
