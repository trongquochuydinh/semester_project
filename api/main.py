from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

if __name__ == "__main__":
    def run_service():
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=os.environ.get("PORT_APP", 8500)
        )

    run_service()