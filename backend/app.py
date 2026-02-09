from fastapi import FastAPI
from fastapi.responses import RedirectResponse


app = FastAPI(title="ENS'ALL IN")


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect to the API documentation"""
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
