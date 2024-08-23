#! /bin/bash

locust -H http://127.0.0.1:8000 --spawn-rate 100 --users 11000 --run-time 3m --processes -1
