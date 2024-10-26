from fastapi import FastAPI

# Routers
import pregao.routes
import solicitacoes.routes
import itens.routes
import usuarios.routes

app = FastAPI()

app.include_router(pregao.routes.router)
app.include_router(solicitacoes.routes.router)
app.include_router(itens.routes.router)
app.include_router(usuarios.routes.router)