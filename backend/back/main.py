from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI(
        title='AFEADA',
        version='0.0.1a',
    )

    return app

app = create_app()