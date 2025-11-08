from fastapi import FastAPI

app = FastAPI(
    title="My First API",
    description="Learning FastAPI step by step",
    version="1.0.0"
)


@app.get("/")
def read_root():
    return {"message": "Hello World"}



@app.get("/health")
def health_check():
    return {"status": "healthy"}


# @app.get("/hello/{name}")
# def say_hello(name: str):
#     return {"message": f"Hello, {name}!"}



@app.get("/weather")
def get_weather(city: str = "New York", units: str = "celsius"):
    temp = 22 if units == "celsius" else 72
    return {"city": city, "temperature": temp, "units": units}



# Combine Path + Query
@app.get("/cities/{city_name}/restaurants")
def get_restaurants(city_name: str, cuisine: str = "all", rating: float = 0.0):
    return {"city": city_name, "cuisine": cuisine, "rating": rating}



# Greeting Endpoint

# Path: /hello/{name}
# Method: GET
# Returns: "Hello, {name}!"
# 👉 Example:

# Request: /hello/Alex
# Response: {"message": "Hello, Alex!"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello, {name}!"}


# Weather Endpoint

# Path: /weather

# Method: GET

# Parameters:

# city (query param, default = "New York")
# Returns:

# {
#   "city": "Delhi",
#   "temperature": 28,
#   "condition": "sunny"
# }

# (Temperature can be a hardcoded value, no real API needed)


@app.get("/weather")
def get_weather(city: str = "New York", units: str = "celsius"):
    temp = 22 if units == "celsius" else 72
    return {"city": city, "temperature": temp, "units": units}



@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b}


@app.post("/tasks/")
def create_task(title: str, description: str, completed: bool = False):
    return title, description, completed

