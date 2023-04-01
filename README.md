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

## Implemantation 

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
flask --app drones_dispatcher/app run
```
