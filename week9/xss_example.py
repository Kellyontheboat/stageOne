from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def get_form():
    return """
    <html>
        <body>
            <form action="/submit" method="post">
                <label for="message">Message:</label>
                <input type="text" id="message" name="message">
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """

@app.post("/submit", response_class=HTMLResponse)
def submit_form(message: str = Form(...)):
    # Vulnerable response
    return f"""
    <html>
        <body>
            <h2>Submitted Message:</h2>
            <p>{message}</p>
            <a href="/">Back</a>
        </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
