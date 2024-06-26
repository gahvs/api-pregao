from fastapi import FastAPI

# Routers
import pregao.routes
import solicitacoes.routes

app = FastAPI()

app.include_router(pregao.routes.router)
app.include_router(solicitacoes.routes.router)