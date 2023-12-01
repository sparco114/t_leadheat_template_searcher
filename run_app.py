from template_search_app.main import template_search_app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(template_search_app, host="127.0.0.1", port=8000)
