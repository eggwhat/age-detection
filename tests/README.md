# Test Scenarios


## Table of Contents
1. [Introduction](#introduction)
2. [Environment Setup](#environment-setup)
    - [Install Dependencies](#install-dependencies)
    - [Run Api](#run-api)
    - [Launch App](#launch-app)
3. [Semi-Automated Test](#semi-automated-test)
    - [Run Test](#run-test)
    - [Test Results](#test-results)
4. [Manual Tests](#manual-tests)


## Introduction
This document describes the test scenarios for the project. There is separate directory for each test scenario.
Each directory contains a README.md file that describes the scenario with manual test. There are also .py files that
contain semi-automated tests for the scenario. 

## Environment Setup
### Install Dependencies
```bash
pip install -r requirements.txt
```
### Run Api
```bash
cd backend/
uvicorn api:app
```
### Launch App
This step is only required for the manual tests. To know how to launch the app, please head over to the README.md file
in the root directory of the project.

## Semi-Automated Test
### Run Test
```bash
cd tests/
pytest
```
### Test Results
The test results will be displayed on the terminal. These tests only check the API endpoints and if they are working as
expected. 

## Manual Tests
For each test scenario, there is a README.md file in the directory that describes the scenario. Please head over to the
corresponding directory.
