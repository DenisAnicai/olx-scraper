import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

os.environ['PATH'] = os.path.dirname(os.path.abspath(__file__)) + os.pathsep + os.environ['PATH']
from main import main

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def root():
    return main()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'api:app',
        host='127.0.0.1',
        port=8000,
        reload=True,
        debug=True,
        workers=1,
    )
