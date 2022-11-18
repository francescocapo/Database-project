import mysql.connector as mysql
from mysql.connector import Error
import pandas as pd

db = mysql.connect(
    host = "localhost",
    user = "root ",
   passwd = "Giuliagiulia3"
)
print(db)


'''
CREATE TABLE `Airplane` (
  `serial number` varchar(100),
  `registration` varchar(100),
  `operator` varchar(100),
  `type` varchar(100),
  PRIMARY KEY (`serial number`, `registration`)
);

CREATE TABLE `Flight` (
  `flight number` varchar(100),
  `aboard` int,
  `route` varchar(100),
  `serial number` varchar(100),
  `registration` varchar(100),
  PRIMARY KEY (`flight number`),
  FOREIGN KEY (`registration`) REFERENCES `Airplane`(`registration`),
  FOREIGN KEY (`serial number`) REFERENCES `Airplane`(`serial number`)
);

CREATE TABLE `Crash` (
  `index` int,
  `location` varchar(100),
  `time` time,
  `date` date,
  `summary` varchar(100),
  `serial number` varchar(100),
  `registration` varchar(100),
  PRIMARY KEY (`index`),
  FOREIGN KEY (`serial number`) REFERENCES `Airplane`(`serial number`),
  FOREIGN KEY (`registration`) REFERENCES `Airplane`(`registration`)
);

CREATE TABLE `Fatalities` (
  `number of fatalities` int,
  `ground` int,
  `crash index` int,
  PRIMARY KEY (`crash index`),
  FOREIGN KEY (`crash index`) REFERENCES `Crash`(`index`)
);
'''