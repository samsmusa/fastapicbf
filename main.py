from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder

import models
import schema
from database import SessionLocal, engine

app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


import time


@app.get("/skill")
async def read_item(request: Request, db: Session = Depends(get_database_session)):
    records = db.query(models.FilterSkill).order_by(models.FilterSkill.id.asc()).all()
    return records


@app.post("/skill")
async def read_item(skill: schema.FilterSkill, db: Session = Depends(get_database_session)):
    db_skill = models.FilterSkill(**skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

# @app.get("/actor")
# async def read_item(request: Request, db: Session = Depends(get_database_session)):
#     return db.query(model.Actor).all()
#     # actor = jsonable_encoder(records)
#     # return JSONResponse(status_code=200, content={
#     #     "status_code": 200,
#     #     "message": "success",
#     #     "actor": actor
#     # })
#
#
# @app.post("/actor/")
# async def create_actor(actor: schema.ActorPost = Depends(schema.ActorPost.as_form),
#                        db: Session = Depends(get_database_session)):
#
#     name = getattr(actor, 'name', None)
#     if bool(db.query(model.Actor).filter_by(name=name).one_or_none()):
#         print(name)
#         raise HTTPException(
#             status_code=404, detail=f"{getattr(actor, 'name', None)} already in database"
#         )
#     db_actor = model.Actor(**actor.dict())
#     db.add(db_actor)
#     db.commit()
#     db.refresh(db_actor)
#     return db_actor
#
#
#
# # def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
# #     db_item = models.Item(**item.dict(), owner_id=user_id)
# #     db.add(db_item)
# #     db.commit()
# #     db.refresh(db_item)
# #     return db_item
#
# # @app.patch("/movie/{id}")
# # async def update_movie(request: Request, id: int, db: Session = Depends(get_database_session)):
# #     requestBody = await request.json()
# #     movie = db.query(Movie).get(id)
# #     movie.name = requestBody['name']
# #     movie.desc = requestBody['desc']
# #     db.commit()
# #     db.refresh(movie)
# #     newMovie = jsonable_encoder(movie)
# #     return JSONResponse(status_code=200, content={
# #         "status_code": 200,
# #         "message": "success",
# #         "movie": newMovie
# #     })
#
#
# @app.delete("/movie/{id}")
# async def delete_movie(request: Request, id: int, db: Session = Depends(get_database_session)):
#     movie = db.query(model.Movie).get(id)
#     db.delete(movie)
#     db.commit()
#     return JSONResponse(status_code=200, content={
#         "status_code": 200,
#         "message": "success",
#         "movie": None
#     })
