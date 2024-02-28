# Simple Page Analyzer (SPA)

[![Actions Status](https://github.com/Mr-Freewan/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Mr-Freewan/python-project-83/actions)
[![CI check](https://github.com/Mr-Freewan/python-project-83/actions/workflows/work-check.yml/badge.svg)](https://github.com/Mr-Freewan/python-project-83/actions/workflows/work-check.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/2d7b759fc7462a88dc10/maintainability)](https://codeclimate.com/github/Mr-Freewan/python-project-83/maintainability)

### Description

SPA is an application based on the Flask framework that analyzes specified
pages for SEO suitability.

Demo app is [HERE](https://page-analyzer-alr1.onrender.com/)  (Requests can be delayed about 50 seconds or more).

### Features

* [X] Validate, normalize and add new URL to the database;
* [X] Check the site for its availability;
* [X] Query the desired site, collect information about it and add it to the
  database;
* [X] Display all added URLs;
* [X] Display the specific entered URL on a separate page with obtained
  information;

### Links

This project was built using these tools:

| Tool                                                            | Description                                                                                                                                                          |
|-----------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Flask](https://flask.palletsprojects.com/en/3.0.x/)            | "Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications" |
| [Poetry](https://python-poetry.org/)                            | "Python dependency management and packaging made easy"                                                                                                               |
| [Flake8](https://flake8.pycqa.org/)                             | "Your tool for style guide enforcement"                                                                                                                              | 
| [Bootstrap](https://getbootstrap.com/)                          | "Powerful, extensible, and feature-packed frontend toolkit."                                                                                                         | 
| [Jinja](https://jinja.palletsprojects.com/en/3.1.x/)            | "A fast, expressive, extensible templating engine"                                                                                                                   | 
| [PostgreSQL](https://www.postgresql.org/)                       | "The World's Most Advanced Open Source Relational Database"                                                                                                          | 
| [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) | "Python library designed for quick turnaround projects like screen-scraping"                                                                                         | 
| [Gunicorn](https://gunicorn.org/)                               | "WSGI HTTP Server for UNIX"                                                                                                                                          | 

---

## Installation

### Important!

* [X] The project uses the Poetry dependency manager. Install it
  with [official instruction](https://python-poetry.org/docs/#installation).
* [X] You need to install the Postgre SQL
  from [official website](https://www.postgresql.org/download/).

### Application

Clone the project:

    git clone https://github.com/Mr-Freewan/python-project-83.git && cd python-project-83

Then install dependencies:

    make install

Create .env file in the root folder and add following variables:

    DATABASE_URL = postgresql://{provider}://{user}:{password}@{host}:{port}/{db}
    SECRET_KEY = '{your secret key}'

Run commands from `database.sql` to create the required tables.

---

## Usage

Start the gunicorn server by running (UNIX):

    make start

Or start the development mode:

    make dev

The server url will be at terminal, for example http://127.0.0.1:5000.

Open server url in a browser. To add a new site, enter its address into the
form on the home page. The specified address will be validated and then added
to the database. After the site is added, you can start checking it. A button
appears on the page of a particular site `/urls/<id>`, and clicking on it creates an entry
in the validation table. You can see all added URLs on the `/urls` page.