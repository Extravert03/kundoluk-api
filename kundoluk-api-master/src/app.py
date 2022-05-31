from fastapi import FastAPI

import endpoints

app = FastAPI()
app.include_router(endpoints.auth.router)
app.include_router(endpoints.student.router)
