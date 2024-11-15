main.py
from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

# Assuming send_email is defined in email_service.py
# from email_service import send_email  

app = FastAPI()

# Adding session middleware to handle sessions for logged-in users
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

templates = Jinja2Templates(directory="templates")  # Assuming you have an HTML template directory

# Redirect root URL ("/") to the login page
@app.get("/")
async def root():
    return RedirectResponse("/login")

# Login page route
@app.get("/login")
async def login_page(request: Request):
    # Render the login page
    return templates.TemplateResponse("login.html", {"request": request, "success": "", "error": ""})

# Login functionality
@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    # Check credentials (use a real database or API in production)
    if email == "your-email@example.com" and password == "your-password":
        request.session['logged_in'] = True
        # Return success message and redirect to the dashboard page
        return templates.TemplateResponse("login.html", {"request": request, "success": "Login successful!", "error": ""})
    else:
        # Invalid credentials, show error message
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials", "success": ""})

# Dashboard page route (email sending page)
@app.get("/dashboard")
async def dashboard(request: Request):
    if request.session.get("logged_in"):
        return templates.TemplateResponse("dashboard.html", {"request": request})
    else:
        # Redirect to login if the user is not logged in
        return RedirectResponse("/login")