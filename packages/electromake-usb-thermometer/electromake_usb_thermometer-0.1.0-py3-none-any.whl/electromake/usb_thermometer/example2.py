"""
Author: Electromake
Website: https://electromake.pl/

Example 2: Save sensor samples to a SQLite database using SQLAlchemy.
The database contains two tables:
 - sensors: with sensor IDs and their ROM codes.
 - samples: with timestamps and temperature readings.
"""

import time
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from .thermometer import USBThermometer  # Adjust import as necessary
from .sensors import DS18B20

# Define the SQLAlchemy ORM models
Base = declarative_base()

class Sensor(Base):
    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True)
    rom_code = Column(String, unique=True)
    samples = relationship("TemperatureSample", back_populates="sensor")

class TemperatureSample(Base):
    __tablename__ = 'samples'
    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey('sensors.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    temperature = Column(Float)
    sensor = relationship("Sensor", back_populates="samples")

def main() -> None:
    # Create a SQLite database (or adjust the URI for PostgreSQL)
    engine = create_engine('sqlite:///sensors.db', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    port: str = "/dev/ttyUSB0"  # Adjust the port for your system
    usb_therm = USBThermometer(port)
    sensors = usb_therm.discover_ROMs()

    # Add discovered sensors to the database if not already present
    for sensor in sensors:
        rom_hex: str = str(sensor)
        db_sensor = session.query(Sensor).filter_by(rom_code=rom_hex).first()
        if not db_sensor:
            db_sensor = Sensor(rom_code=rom_hex)
            session.add(db_sensor)
    session.commit()

    print("Beginning temperature sampling. Press Ctrl+C to stop.")
    try:
        while True:
            for i, sensor in enumerate(sensors):
                temp = usb_therm.read_temperature(i)
                rom_hex = str(sensor)
                db_sensor = session.query(Sensor).filter_by(rom_code=rom_hex).first()
                sample = TemperatureSample(
                    sensor_id=db_sensor.id,
                    timestamp=datetime.utcnow(),
                    temperature=temp
                )
                session.add(sample)
                print(f"Sensor {rom_hex}: {temp:.2f}°C at {sample.timestamp}")
            session.commit()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nExiting sampling loop.")
    finally:
        session.close()
        del usb_therm

if __name__ == "__main__":
    main()
