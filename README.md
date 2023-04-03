# REST API that allows clients to communicate with the drones (i.e. dispatch controller)

## Introduction

There is a major new technology that is destined to be a disruptive force in the field of transportation: the
drone. Just as the mobile phone allowed developing countries to leapfrog older technologies for personal
communication, the drone has the potential to leapfrog traditional transportation infrastructure.
Useful drone functions include delivery of small items that are (urgently) needed in locations with difficult
access.

## Description

We have a fleet of 10 drones. A drone is capable of carrying devices, other than cameras, and capable of
delivering small loads. For our use case the load is medications.

## The service allows:
* Registering a drone
* Loading a drone with medication items
* Checking loaded medication items for a given drone
* Checking available drones for loading
* Check drone battery level for a given drone

## How to run locally
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd drones_dispatcher
flask db upgrade
flask --app app run
```

## How to test

### Login
```
curl --location --request POST 'http://127.0.0.1:5000/api/auth/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "john@example.com",
    "password": "johndoe"
}'
```

### Register a drone
```
curl --location --request POST 'http://127.0.0.1:5000/api/drone/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjdkMGI2NGYyLTNhYzctNGJhZS04Mzk3LTU1Y2YwZTU4YWVhMSIsImVtYWlsIjoiam9obkBleGFtcGxlLmNvbSIsInVzZXJuYW1lIjoiam9obmRvZSIsImV4cCI6MTY4MDU0NjA3MX0.m_6VHPJjLomoHRn5L6bK4ksTsb2x5yQ0cSv1VbqPFKY' \
--header 'Content-Type: application/json' \
--data-raw '{
    "serial_number": "Drone6",
    "model": "Cruiserweight",
    "weight_limit": 450,
    "battery_capacity": 90,
    "state": "LOADING"
}'
```

### Loda a dron
```
curl --location --request POST 'http://127.0.0.1:5000/api/medication/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjdkMGI2NGYyLTNhYzctNGJhZS04Mzk3LTU1Y2YwZTU4YWVhMSIsImVtYWlsIjoiam9obkBleGFtcGxlLmNvbSIsInVzZXJuYW1lIjoiam9obmRvZSIsImV4cCI6MTY4MDU0NjA3MX0.m_6VHPJjLomoHRn5L6bK4ksTsb2x5yQ0cSv1VbqPFKY' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "medication1",
    "weight": 100,
    "code": "NEDICATION1",
    "drone_id": "bb0e4ccd-ef49-48d5-a50a-a4574a931f7e"
}'
```

### Checking loaded medication items for a given drone
```
curl --location --request GET 'http://127.0.0.1:5000/api/drone/bb0e4ccd-ef49-48d5-a50a-a4574a931f7e/medications/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjdkMGI2NGYyLTNhYzctNGJhZS04Mzk3LTU1Y2YwZTU4YWVhMSIsImVtYWlsIjoiam9obkBleGFtcGxlLmNvbSIsInVzZXJuYW1lIjoiam9obmRvZSIsImV4cCI6MTY4MDU0NjA3MX0.m_6VHPJjLomoHRn5L6bK4ksTsb2x5yQ0cSv1VbqPFKY' \
--header 'Content-Type: application/json'
```

### Checking available drones for loading
```
curl --location --request GET 'http://127.0.0.1:5000/api/drone/available/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjdkMGI2NGYyLTNhYzctNGJhZS04Mzk3LTU1Y2YwZTU4YWVhMSIsImVtYWlsIjoiam9obkBleGFtcGxlLmNvbSIsInVzZXJuYW1lIjoiam9obmRvZSIsImV4cCI6MTY4MDU0NjA3MX0.m_6VHPJjLomoHRn5L6bK4ksTsb2x5yQ0cSv1VbqPFKY' \
--header 'Content-Type: application/json'
```

### Check drone battery level for a given drone
```
curl --location --request GET 'http://127.0.0.1:5000/api/drone/d9662688-c3ab-4a58-b8d9-54e785c7633e/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjdkMGI2NGYyLTNhYzctNGJhZS04Mzk3LTU1Y2YwZTU4YWVhMSIsImVtYWlsIjoiam9obkBleGFtcGxlLmNvbSIsInVzZXJuYW1lIjoiam9obmRvZSIsImV4cCI6MTY4MDU0NjA3MX0.m_6VHPJjLomoHRn5L6bK4ksTsb2x5yQ0cSv1VbqPFKY' \
--header 'Content-Type: application/json'
```
