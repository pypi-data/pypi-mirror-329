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

## Project Structure

```
myproject/
│── main.py          # Entry point for FastAPI app
│── routes.py        # Contains 'custom_routes'
│── alembic.ini
│── models.py
│── schemas.py
│── middlewares/
│   ├── middleware.py  # Global middleware logic
│── routers/         # API route modules
│── settings/
│   ├── database.py  # Database configuration
│   ├── routing.py   # Router configurations
│── alembic/
```

This structure ensures modularity and scalability for your FastAPI project. Adjust the folders and files as needed based on your project requirements.

