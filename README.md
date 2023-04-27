<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://cdn-icons-png.flaticon.com/512/6542/6542849.png" alt="Project logo"></a>
</p>

<h3 align="center">Fermento</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/BastianLo/Fermento/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/BastianLo/Fermento/pulls)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](/LICENSE)
![CI Pipeline](https://github.com/BastianLo/Fermento/actions/workflows/docker-image.yml/badge.svg)
</div>

---

<p align="center"> Fermento is a self-hostable recipe manager specifically for fermentation.
    <br> 
</p>

## 📝 Table of Contents

- [Features](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 Features <a name = "about"></a>
WIP: Project is still in development and not feature complete!

* Manage your fermentation recipes
* Create recipe variations (e.g if you are having multiple Kombuchas with the same Base) (TODO)
* Create reoccuring tasks
  * Each recipes can contain reoccuring tasks which have to be done overtime 
  * Never again forget to feed your sourdough


## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Installing

A step by step series of examples that tell you how to get a development env running.

First clone this repository
```
git clone https://github.com/BastianLo/Fermento
```

Then install the required dependencies

```
pip install -r Fermento/requirements.txt
```

After successfully installing the dependencies, apply the django database migrations

```
Fermento/Fermento/manage.py migrate
```

The Application is now correctly installed and can be run

```
python3 Fermento/Fermento/manage.py runserver
```

## 🔧 Running the tests <a name = "tests"></a>
WIP

## 🎈 Usage <a name="usage"></a>
WIP

## 🚀 Deployment <a name = "deployment"></a>

### Docker
Fermento can easily be deployed using docker.

```
version: '3.3'
services:
    fermento:
        container_name: fermento
        environment:
            - LISTEN_PORT=6733
            - USERNAME=${USERNAME}
            - PASSWORD=${PASSWORD}
            - EMAIL=${EMAIL}
            - DEBUG=False
            - APP_DOMAIN=http://127.0.0.1:6733
        ports:
            - '6733:6733'
        image: 'bastianlo/fermento:latest'
        volumes:
            - ./data:/Fermento/Fermento/data
```

## ⛏️ Built Using <a name = "built_using"></a>

- [Django](https://www.djangoproject.com/) - Web Framework
- [halfmoon](https://www.gethalfmoon.com) - Css Framework

## ✍️ Authors <a name = "authors"></a>

- [@BastianLo](https://github.com/BastianLo) - Idea & Initial work

See also the list of [contributors](https://github.com/kylelobo/The-Documentation-Compendium/contributors) who participated in this project.

## 🎉 Acknowledgements <a name = "acknowledgement"></a>
This project is using icons from flaticon.com
