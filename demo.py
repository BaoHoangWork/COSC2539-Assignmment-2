from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from html import escape
from collections import defaultdict
import time

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rate_limit = defaultdict(lambda: {"count": 0, "start_time": time.time()})
REQUEST_LIMIT = 100  # Max requests per minute
token = "1234"

# XSS Attack DEMO
@app.get("/xss-demo", response_class=HTMLResponse)
async def get_comment_form(request: Request):
    comment_form = """
    <form method="post">
        <label for="comment">Leave a comment:</label>
        <input style="width: 300px" type="text" name="comment" required>
        <button type="submit">Submit</button>
    </form>
    """

    # --------------- IMPLEMENT DoS prevention - rate limit --------------- 
    client_ip = request.client.host
    current_time = time.time()

    # Reset rate limit after 60 seconds
    if current_time - rate_limit[client_ip]["start_time"] > 60:
        rate_limit[client_ip] = {"count": 0, "start_time": current_time}

    # Count requests
    rate_limit[client_ip]["count"] += 1

    # Check if the request limit is exceeded
    if rate_limit[client_ip]["count"] > REQUEST_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    # --------------- IMPLEMENT DoS prevention - rate limit --------------- 

    return HTMLResponse(content=comment_form)

@app.post("/xss-demo", response_class=HTMLResponse)
async def post_comment(comment: str = Form(...)):

    # --------------- IMPLEMENT XSS prevention - sanitisastion --------------- 
    # Sanitise the request before response to the user
    sanitized_comment = escape(comment)
    return HTMLResponse(content=f"Your comment: {sanitized_comment}")
# --------------- IMPLEMENT XSS prevention - sanitisastion  --------------- 

    # No Validation or process -> response HTML immediately for testing XSS purpose
    return HTMLResponse(content=f"Your comment: {comment}")

# CSFR Attack DEMO
@app.get("/csfr-demo", response_class=HTMLResponse)
async def get_comment_form(request: Request):
    token = "1234"
    comment_form = """
    <form method="post">
        <input type="hidden" name="token" value="{{ token }}">
        <label for="comment">CSFR Attack:</label>
        <input style="width: 300px" type="text" name="comment" required>
        <button type="submit">Submit</button>
    </form>
    """

    return HTMLResponse(comment_form.replace("{{ token }}", token or ""))

@app.post("/csfr-demo", response_class=HTMLResponse)
async def post_comment(comment: str = Form(...), token: str = Form(...)):

# --------------- IMPLEMENT CSFR prevention - token  ---------------     
    token_key = "1234"
    if token_key != token:
        raise HTTPException(status_code=403, detail="invalidation token")
# --------------- IMPLEMENT CSFR prevention - token  ---------------     

    return HTMLResponse(content=f"Your comment: {comment} {token}")
   
# CSFR Attack
@app.get("/csfr-attack", response_class=HTMLResponse)
async def get_form(request: Request):
    form_html = """
    <form action="http://127.0.0.1:8008/csfr-demo" method="post">
        <input type="hidden" name="token" value="wrong token">
        <label for="comment">CSFR Attack:</label>
        <input style="width: 300px" type="text" name="comment" required>
        <button type="submit">Submit</button>
    </form>
    """
    return HTMLResponse(content=form_html)



