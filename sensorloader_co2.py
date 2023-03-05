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
