# USB Thermometer Python library
## Overview
This project provides a Python 3 library for interfacing with DS18B20 temperature sensors via a USB-based 1-Wire interface. The library implements the 1-Wire protocol over a serial port, allowing you to discover connected sensors, read temperature measurements, configure sensor settings (precision, alarm thresholds), and perform low-level bit manipulations required for proper communication with the sensors.

## Features

- **Sensor Discovery:** Detect all DS18B20 sensors on the 1-Wire bus.
- **Temperature Reading:** Continuously read sensor temperature values.
- **Sensor Configuration:** Write to and read from the sensor scratchpad, set measurement precision and alarm thresholds.
- **Utilities:** Functions for converting bit lists to hexadecimal strings/bytearrays and computing CRC8 checksums.
- **Examples:** Three comprehensive examples demonstrate:
  1. Discovering sensors and continuously reading their temperatures.
  2. Storing sensor data in an SQL database using SQLAlchemy.
  3. Configuring sensor settings (precision and alarm thresholds).

## Project Structure

- **wire.py**  
  Implements the `USBThermometer` class which manages communication with DS18B20 sensors via a serial port.

- **sensors.py**  
  Contains the `DS18B20` class that represents individual temperature sensors, handling their ROM codes, serial numbers, and configuration registers.

- **utils.py**  
  Provides utility functions for bit manipulation, hexadecimal conversion, and CRC8 calculation.

- **tests**  
  Unit tests for verifying the functionality of the library.

- **examples**  
  Example scripts demonstrating different use cases:
  - `example1.py`: Discover sensors and continuously read temperatures until interrupted.
  - `example2.py`: Record sensor samples to a SQL database (SQLite or PostgreSQL) using SQLAlchemy.
  - `example3.py`: Configure sensor settings such as precision and alarm thresholds.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/electromake/usb-thermometer-python.git
    cd usb-thermometer-python
    ```

2. **Install required dependencies:**
    ```bash
    pip install pyserial sqlalchemy
    # If you would like to run SQL example, run also:
    pip install sqlalchemy
    ```

## Usage

### Example 1: Continuous Temperature Reading

Discover all sensors and continuously read their temperatures until a keyboard interrupt (Ctrl+C) is detected.
```bash
python example1.py
```
### Example 2: Storing Sensor Samples in a Database
Discover sensors and store temperature samples (with timestamps) in a SQL database. The database contains two tables: one for sensor details (ROM codes) and one for temperature samples.
```bash
python example2.py
```
### Example 3: Configuring Sensor Settings
Configure sensor settings by adjusting measurement precision and alarm thresholds. The example shows how to write new settings to the sensor's scratchpad and verify them.
```bash
python example3.py
```

### Testing
To run the unit tests, execute:
```bash
python -m unittest discover
```

### More resources
- [DS18B20 Datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/DS18B20.pdf)  
- [1-wire serial port implementation](https://www.analog.com/en/resources/technical-articles/using-a-uart-to-implement-a-1wire-bus-master.html)  

### Author
Electromake  
[https://electromake.pl/](https://electromake.pl) 