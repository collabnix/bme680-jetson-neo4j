from random import uniform
from datetime import datetime
from influxdb import InfluxDBClient

# Define InfluxDB configuration
influx_host = 'localhost'
influx_port = 8086
influx_database = 'sensor_data'
influx_measurement = 'bme680'

# Connect to InfluxDB
influx_client = InfluxDBClient(host=influx_host, port=influx_port)
influx_client.switch_database(influx_database)

# Define number of sensors to simulate
num_sensors = 50

# Define simulation parameters
temp_min = 20.0
temp_max = 30.0
hum_min = 30.0
hum_max = 50.0
gas_min = 0.0
gas_max = 1000.0

# Simulate data for each sensor
for i in range(num_sensors):
    # Generate random sensor data
    temperature = uniform(temp_min, temp_max)
    humidity = uniform(hum_min, hum_max)
    gas_resistance = uniform(gas_min, gas_max)

    # Create InfluxDB data point
    data_point = {
        "measurement": influx_measurement,
        "tags": {
            "sensor_id": i+1
        },
        "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "fields": {
            "temperature": temperature,
            "humidity": humidity,
            "gas_resistance": gas_resistance
        }
    }

    # Write data to InfluxDB
    influx_client.write_points([data_point])

print("Simulated data sent to InfluxDB!")
