# FastBrick 🚀

A simple CLI tool to generate FastAPI project structures.

## Installation

Install FastBrick using:
```sh
pip install fastbrick
```

## Run Server

Start the FastAPI server with:
```sh
uvicorn main:app --reload
```

## Help Command

To see available options and commands:
```sh
fastbrick --help
```

## Usage
Create a New Project
Creates a new FastAPI project with a structured layout.
```sh
fastbrick create-project my_project
```
Create a New App
Creates a new FastAPI app (router) with database settings.

```sh
fastbirck create-app my_app
```

## Project Structure

```
myproject/
│── main.py          # Entry point for FastAPI app
│── routes.py        # Contains 'app routes'
│── models.py
│── schemas.py
│── middlewares/
│   ├── middleware.py  # Global middleware logic
│── routers/         # API route modules
│── settings/
│   ├── config.py  # Database configuration
│   ├── database.py  # Database configuration
│   ├── routing.py   # Router configurations
```

This structure ensures modularity and scalability for your FastAPI project. Adjust the folders and files as needed based on your project requirements.

