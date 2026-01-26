# FastAPI Learning Journey

I am learning FastAPI.

This repository contains my practice code, experiments, and notes created while learning FastAPI step by step.

---

## How to Run

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

Open:

* [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Structure

Each folder represents a topic or practice session related to FastAPI.

---

## Author

Abhijit Zende

---
Notes

# FastAPI vs. Uvicorn

### 1. Core Definitions
* **FastAPI:** A high-performance web **framework**. It provides the tools to build the API logic (routes, validation, database connection).
* **Uvicorn:** A lightning-fast **ASGI web server**. It handles the network connections and communicates between the internet and the Python application.

### 2. Key Differences Table

| Feature | FastAPI | Uvicorn |
| :--- | :--- | :--- |
| **Role** | Application Framework (The "App") | Web Server (The "Runner") |
| **Function** | Defines *what* the API does. | Defines *how* the API is served. |
| **Protocol** | HTTP (High-level handling) | ASGI (Asynchronous Server Gateway Interface) |
| **Responsibility** | Routing, Validation, Serialization. | Process management, Port listening, Parsing. |
| **Analogy** | The **Chef** (Cooks the food). | The **Waiter** (Takes orders/Delivers food). |

### 3. How They Work Together (The ASGI Bridge)
1.  **Client Request:** A browser sends an HTTP request.
2.  **Uvicorn:** Receives the raw request, parses it, and translates it into an ASGI event (Python dictionary).
3.  **FastAPI:** Receives the event, routes it to the correct function (e.g., `@app.get("/items")`), executes the logic, and returns Python data.
4.  **Uvicorn:** Takes the response, converts it back to HTTP, and sends it to the client.

### 4. Practical Example

**A. The Code (`main.py`)**
This is the **FastAPI** part.
```python
from fastapi import FastAPI

# Framework instance
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

**B. The Execution (Terminal) This is the Uvicorn part.**

```Bash
uvicorn main:app --reload
```
Command Breakdown:

uvicorn: The Server program that listens for traffic.

main: The file name (main.py) containing the code.

app: The variable name of the FastAPI instance inside main.py.

--reload: Flag to restart the server automatically when code changes (dev only).
---

# Why Instantiate FastAPI? (`app = FastAPI()`)

### 1. The Short Answer
We must instantiate the class because **Uvicorn needs a concrete object** to interact with, not a blueprint (class). The `app` object acts as the central registry that holds all your routes, configurations, and middleware.

### 2. Class vs. Instance

| Concept | Code | Analogy | Why Uvicorn can't use it |
| :--- | :--- | :--- | :--- |
| **Class** | `FastAPI` | The **Blueprint** for a house. | You cannot live in a blueprint. |
| **Instance** | `app = FastAPI()` | The **Actual House** built from the blueprint. | Uvicorn needs a real "house" to send requests into. |

### 3. Key Functions of the `app` Instance
When you run `app = FastAPI()`, this specific object starts doing critical work that the raw class cannot do:

* **Route Registry:** It creates a list to store paths (e.g., `/`, `/users`). When you use `@app.get("/")`, you are adding an entry to this specific list.
* **Configuration Holder:** It stores settings like `title`, `version`, and `debug` mode.
* **ASGI Application:** It implements the `__call__` method required by the ASGI standard, allowing Uvicorn to "call" it when a request arrives.

### 4. Code Example: The "Registry" Concept

If you didn't create `app`, your decorators wouldn't know where to attach the functions.

```python
from fastapi import FastAPI

# 1. Create the container (Instance)
app = FastAPI() 

# 2. Attach a route TO that container
# If we just used 'FastAPI.get', it wouldn't know which app we are talking about.
@app.get("/") 
def greet():
    return "Hello from Abhi"
```
5. Why Uvicorn Needs It
When you run uvicorn main:app:

Uvicorn looks inside main.py.

It looks for the variable app.

It verifies that app is a valid ASGI application (an instance with a __call__ method).

It starts sending network traffic to that specific app object.
---

# What is ASGI?

**ASGI** stands for **Asynchronous Server Gateway Interface**. It is the modern standard specification that acts as a bridge between Python web servers (like Uvicorn) and web frameworks (like FastAPI).



### 1. The Core Purpose
ASGI allows Python web applications to be **Asynchronous**. This means the server can handle many incoming requests simultaneously without waiting for one to finish before starting the next.

### 2. WSGI vs. ASGI
Before ASGI, Python used **WSGI** (Web Server Gateway Interface). The key difference is how they handle "waiting" (latency).

| Feature | WSGI (Legacy) | ASGI (Modern) |
| :--- | :--- | :--- |
| **Execution Model** | **Synchronous** (Serial) | **Asynchronous** (Concurrent) |
| **Behavior** | Handles one request at a time. If one request waits (e.g., for a database), the server is blocked. | Handles multiple requests at once. If one request waits, the server switches to work on another. |
| **Capabilities** | HTTP only. | HTTP, **WebSockets**, HTTP/2. |
| **Frameworks** | Flask, Django (older versions). | FastAPI, Quart, Django (newer versions). |

### 3. Analogy: The Coffee Shop

* **WSGI (Blocking):** A coffee shop with **one employee**. They take your order, brew the coffee, hand it to you, and *only then* turn to the next customer. If the machine takes 2 minutes, everyone waits.
* **ASGI (Non-Blocking):** A coffee shop with **one smart employee**. They take your order and start the machine. While the machine is brewing, they immediately take the next customer's order. They juggle multiple orders efficiently.

### 4. Why FastAPI Needs ASGI
FastAPI is built on top of Starlette (an ASGI toolkit) to enable:
* **High Performance:** It matches the speed of Node.js and Go.
* **`async` / `await`:** You can use Python's modern async keywords to pause functions while waiting for I/O (Database, API calls) without blocking the server.
* **WebSockets:** Essential for real-time features like chat apps or live notifications.

### 5. Code Context
Because FastAPI is ASGI, you define routes using `async def`:

```python
@app.get("/")
async def read_results():
    # The server can handle other requests while waiting for this line
    results = await some_long_database_query()
    return results
```

# Web Development Core Concepts

### 1. HTTP & Methods
**HTTP (HyperText Transfer Protocol):** The set of rules for transferring files (text, images, sound, video, etc.) on the World Wide Web.



**HTTP Methods (The Verbs):**
These tell the server *what action* to perform on the resource.

| Method | Action | SQL Equivalent | Example Usage |
| :--- | :--- | :--- | :--- |
| **GET** | **Retrieve** data. | `SELECT` | Reading a blog post. |
| **POST** | **Create** new data. | `INSERT` | Submitting a sign-up form. |
| **PUT** | **Update** existing data. | `UPDATE` | Editing your user profile. |
| **DELETE** | **Remove** data. | `DELETE` | Deleting a comment. |

---

### 2. Key Terminology

* **REST (Representational State Transfer):** An architectural style for designing networked applications. A "RESTful" API uses standard HTTP methods (GET, POST, etc.) and stateless communication.
* **JSON (JavaScript Object Notation):** A lightweight data format used to exchange information between the Frontend and Backend. It looks like a Python dictionary.
    * *Example:* `{"name": "Abhi", "age": 25}`
* **Route:** The code logic that handles a specific request. It is the combination of the URL path and the HTTP method.
    * *Example:* `@app.get("/users")`
* **Endpoint:** The specific URL (address) where a service can be accessed by a client.
    * *Example:* `https://api.myapp.com/users/123`

---

### 3. Architecture Components



[Image of frontend backend database architecture diagram]


* **Frontend (The Client):** The part the user sees and interacts with (Website, Mobile App). It runs in the browser.
* **Backend (The Server):** The logic behind the scenes (FastAPI/Uvicorn). It processes requests, runs business logic, and talks to the database.
* **Database (DB):** The storage system where data is kept permanently (PostgreSQL, MySQL).

---

### 4. How It All Works Together (The Flow)

Here is the step-by-step lifecycle of a single request (e.g., "Abhi posts a tweet"):

| Step | Component | Action |
| :--- | :--- | :--- |
| **1** | **Frontend** | User clicks "Post". The browser sends a **POST** request to the **Endpoint** `/tweets` with data in **JSON** format. |
| **2** | **HTTP** | The request travels over the internet using the **HTTP** protocol. |
| **3** | **Backend** | The **Route** in FastAPI (`@app.post("/tweets")`) receives the request. It validates the data. |
| **4** | **DB** | The Backend asks the **Database** to `INSERT` the new tweet. The DB confirms it is saved. |
| **5** | **Response** | The Backend sends a success message (JSON) back to the Frontend. |
| **6** | **Frontend** | The browser receives the data and updates the screen to show the new tweet. |

---
# What is Pydantic?

### 1. Core Definition
**Pydantic** is a data validation and settings management library for Python using Python type hints.

* **Simple Terms:** It is the **Gatekeeper** for your data. It checks if the data coming into your API is correct, clean, and in the right format.
* **How it works:** You define a class with type hints (e.g., `str`, `int`), and Pydantic ensures the data matches those types.

### 2. Why is it important in FastAPI?
FastAPI is tightly coupled with Pydantic. It doesn't just "use" it; it relies on it for almost everything related to data handling.

| Feature | Without Pydantic | With Pydantic (FastAPI) |
| :--- | :--- | :--- |
| **Data Validation** | You write manual `if` statements: `if not isinstance(age, int)...` | **Automatic.** If you say `age: int`, Pydantic ensures it's an integer. |
| **Data Conversion** | You manually parse strings: `id = int(request.args.get("id"))` | **Automatic.** It converts `"5"` (string) to `5` (int) for you. |
| **Error Handling** | You manually write error messages for every bad input. | **Automatic.** Returns clear JSON errors pointing exactly to what is wrong. |
| **Documentation** | You have to manually write what fields your API accepts. | **Automatic.** It generates the Swagger UI schemas from your models. |

### 3. The "Gatekeeper" Flow



1.  **Incoming Data:** User sends JSON `{"name": "Abhi", "age": "25"}`.
2.  **Pydantic Layer:** Checks the data against your model.
    * *Check:* Is "name" a string? Yes.
    * *Check:* Is "age" an integer? It's a string "25", but Pydantic **converts** it to integer `25`.
3.  **Result:**
    * **Success:** The route function receives clean Python data.
    * **Failure:** The user immediately gets a `422 Unprocessable Entity` error.

### 4. Code Example

**The Model (The Rules):**
```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    is_student: bool = False # Default value
```

### The FastAPI Route:
```python
@app.post("/users/")
def create_user(user: User):
    # 'user' is now a valid Python object, not just a raw dictionary
    return {"message": f"Created user {user.name} who is {user.age} years old"}
```

|Input JSON| Model Definition| Result|
| :--- | :--- | :--- |
|"{""age"": 25}"|age: int|Valid. (25)|
|"{""age"": ""25""}"|age: int|Valid. (Converted to 25)|
|"{""age"": ""twenty""}"|age: int|Error. (422 Unprocessable Entity)|

# Pydantic & Swagger in FastAPI

FastAPI automates the relationship between your code (Pydantic) and your documentation (Swagger). You write the code once, and FastAPI handles the rest.

### 1. Pydantic with FastAPI (The "Engine")
Pydantic is the mechanism FastAPI uses to understand data structures.

* **Request Validation:** When you define a Pydantic model for a request body, FastAPI validates incoming JSON against it.
* **Response Serialization:** FastAPI uses Pydantic to convert your Python objects (from a DB or logic) into clean JSON for the client.
* **Schema Generation:** Pydantic models are converted into **JSON Schemas**, which are the building blocks for the documentation.

### 2. Swagger UI with FastAPI (The "Display")
Swagger UI is the interactive website that FastAPI generates automatically for you.

* **Automatic Generation:** You do not write Swagger documentation manually. FastAPI reads your Pydantic models and function parameters to build it.
* **Interactive Testing:** It allows you (and other developers) to click "Try it out" and send real requests to your API directly from the browser.
* **Standards Based:** It is based on **OpenAPI** (formerly known as Swagger specification), a standard format for defining APIs.

### 3. The "Magic" Link
The beauty of FastAPI is how these two connect:
**Pydantic Model** $\rightarrow$ **OpenAPI Schema** $\rightarrow$ **Swagger UI**

| Component | Role | What you do |
| :--- | :--- | :--- |
| **Pydantic** | Defines the "Shape" of data. | Write Python Classes. |
| **FastAPI** | Connects the shape to the HTTP route. | Add the class as a type hint. |
| **OpenAPI** | The raw JSON description of your API. | Nothing (Generated automatically). |
| **Swagger UI** | Visualizes the OpenAPI JSON. | Visit `/docs` in your browser. |

### 4. Code Example: Seeing the Connection



**The Code:**
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 1. Pydantic Model (The Definition)
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

# 2. FastAPI Route (The Usage)
@app.post("/items/")
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}
```

The Result in Swagger UI (/docs):

You will see a POST button for /items/.

Clicking it shows an Example Value JSON box.

The box is pre-filled with name, price, and is_offer because Swagger read the Pydantic model.

If you send "price": "hello", Swagger shows the error defined by Pydantic.
---
# Documentation: Get Product by ID

### 1. Function Overview
The `get_product_by_id` function allows a user to retrieve the details of a single specific product from the list by providing its unique `id`.

### 2. Logic Flow


1.  **Input:** The API receives an `id` as a **Path Parameter**.
2.  **Processing:** * It loops through the `products` list.
    * It compares each `product.id` with the input `id`.
3.  **Output:**
    * **Success:** Returns the full Product object if a match is found.
    * **Failure:** Returns "Product not found!" if the loop finishes without a match.

### 3. Key Concepts Used

| Concept | Implementation in Code | Purpose |
| :--- | :--- | :--- |
| **Path Parameter** | `"/product/{id}"` | Tells FastAPI that the value in the URL is a variable. |
| **Type Hinting** | `id: int` | Ensures the input is an integer; otherwise, FastAPI returns a 422 Error. |
| **Iteration** | `for product in products:` | Steps through the data to find the specific record. |

### 4. API Specification

**Endpoint:** `/product/{id}`  
**Method:** `GET`

**Example Request:**
`GET http://127.0.0.1:8000/product/2`

**Example Successful Response (JSON):**
```json
{
  "id": 2,
  "name": "laptop",
  "description": "budget laptop",
  "price": 98,
  "quantity": 30
}
```

# Documentation: Add a New Product

### 1. Function Overview
The `add_product` function allows clients to send data to the API to create and store a new product in the system's memory.

### 2. Logic Flow


1.  **Input:** The API receives a JSON object in the **Request Body**.
2.  **Validation:** FastAPI uses the `Product` Pydantic model to ensure all required fields (name, price, etc.) are present and have the correct data types.
3.  **Processing:** The validated `product` object is appended to the global `products` list.
4.  **Output:** The function returns the newly created product object back to the user to confirm successful creation.

### 3. Key Concepts Used

| Concept | Implementation in Code | Purpose |
| :--- | :--- | :--- |
| **POST Method** | `@app.post("/product")` | Used for sending data to the server to create a resource. |
| **Request Body** | `product: Product` | Tells FastAPI to look for the data inside the body of the HTTP request, not the URL. |
| **Pydantic Model** | `Product` | Automatically converts the incoming JSON into a Python object and validates it. |
| **In-Memory Storage**| `products.append()` | Temporarily saves the data in a Python list (data is lost if the server restarts). |

### 4. API Specification

**Endpoint:** `/product`  
**Method:** `POST`

**Example Request Body (JSON):**
```json
{
  "id": 5,
  "name": "tablet",
  "description": "high-res display",
  "price": 299,
  "quantity": 15
}
```

**Example Successful Response (JSON):**
```json
{
  "id": 5,
  "name": "tablet",
  "description": "high-res display",
  "price": 299,
  "quantity": 15
}
```

### 5. Interaction with Swagger UI
1. Navigate to /docs.

2. Find the POST /product endpoint.

3. Click Try it out.

4. FastAPI will provide a pre-filled JSON template based on your Product model.

5. Modify the values in the JSON box and click Execute.

6. Verify the result by calling the GET /products endpoint to see your new item in the list.