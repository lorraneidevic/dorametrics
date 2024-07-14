# DORA Metrics
https://www.thoughtworks.com/radar/techniques/four-key-metrics

For now i'm only trying to get the deployment frequency metric, but the idea is to get all of them.

This code assumes that whenever you push to main (or any other production branch, you can change in the code)
you are deploying to production.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them.

```bash
python3 -m pip install -r requirements.txt
```

### Setting Up

A step by step series of examples that tell you how to get a development environment running.

1. Clone the repository to your local machine

2. Copy the `.env.example` file to a new file named `.env`:

```bash
cp .env.example .env
```

3. Open the `.env` file and fill in the `GITHUB_ACCESS_TOKEN` and `REPOSITORY_OWNER_NAME` with your own details. The `REPOSITORY_OWNER_NAME` is the name of the owner of the repository you want to analyze.

4. This code only gets the one repo from all owner repositories. If you want to change this, there is a TODO: 
in the code and right below you can change the index of the list to get the repo you want. I did not test it yet but
right approach is to got through all repos and get the metrics from all of them, maybe next version :) .

## How to run the project.

```bash
python main.py
```
