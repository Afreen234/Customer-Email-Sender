@app.get("/login")
async def login_page(request: Request):
    # Get success and error messages from session
    success_message = request.session.get("success", "")
    error_message = request.session.get("error", "")

    # Clear session messages after they are shown
    request.session.pop("success", None)
    request.session.pop("error", None)

    return templates.TemplateResponse("login.html", {
        "request": request,
        "success": success_message,
        "error": error_message
    })
