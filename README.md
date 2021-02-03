# Vaccine Distribution Database
#### System Programmimg course assignment.
#### Demonstrates the usage of Persistence Layer, Data Transfer Object, Data Access Object, ORM, and SQL.
#### Uses python 3.6 and SQLite.
### USAGE:
```python3 main.py config.txt orders.txt output.txt```
### INPUT:
#### Configuration file:
> Includes into 5 sections, each corresponding to a specific table in the database.
> - 1st section: single row, unsigned integers seperated by commas, each number states how many rows are there for each section.
> - 2nd section: vaccine stocks, each row represents a single stock entry.
> - 3rd section: suppliers, each row represents a vaccine supplier.
> - 4th section: clinics, each row represents a vaccination clinic.
> - 5th section: logistics, each row represents a delivery service.

> Configuration file structure:
```
<#1>,<#2>,<#3>,<#4>
<vaccines>
<suppliers>
<clinics>
<logistics>
```

> Example:
```3,1,2,2
1,2021-01-10,1,10
2,2021-01-11,1,20
3,2021-01-12,1,20
1,Pfizer,1
1,Beer-Sheva,50,1
2,Tel-Aviv,150,2
1,DHL,0,0
2,UPS,0,0
```
#### Orders file:
> Each order is represented by one row, which includes the name of the vaccine supplier, the amount of vaccines, and the date of the shipment:
```
<name>,<amount>,<date>
```

> Example:
```
Pfizer,20,2021-01-02
```

### OUTPUT:
