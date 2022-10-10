import numpy as np
from fastapi import Depends, FastAPI, Request
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from sqlalchemy.orm import Session

import models
import schema
from database import SessionLocal, engine
from sqlalchemy.exc import SQLAlchemyError

import utils

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


@app.get("/skill")
async def read_item(request: Request, db: Session = Depends(get_database_session)):
    records = db.query(models.FilterSkill).order_by(models.FilterSkill.id.asc()).all()
    return records


@app.post("/skill")
async def read_item(skill: schema.FilterSkill, db: Session = Depends(get_database_session)):
    # if bool(db.query(models.FilterSkill).filter_by(skill=getattr(skill, 'skill', None)).one_or_none()):
    #     raise HTTPException(
    #         status_code=404, detail=f"{getattr(skill, 'skill', None)} already in database"
    #     )
    try:
        # try something
        print('------1--------')
        db_skill = models.FilterSkill(**skill.dict())
        print('------2--------')
        db.add(db_skill)
        print('------3--------')
        db.commit()
        print('------4--------')
        db.refresh(db_skill)
        print('------5--------')
        return db_skill
    except SQLAlchemyError as e:
        print(e.__dict__)
        error = str(e.__dict__['orig'])
        # print(error)
        return error


# @app.get('/{client_id}')
# async def root(client_id):
#     print(f'Start processing a request from client: {client_id}')
#     count = 0
#     for _ in range(100000000):
#         count += 1
#     print(f'Start processing a request from client: {client_id}')
#     return {}


@app.post('/job/')
async def job(request: Request, jobschema=Depends(schema.FilterJob.as_form), db: Session = Depends(get_database_session)):
    # async def job(job: schema.FilterJob, db: Session = Depends(get_database_session)):
    job = models.FilterJob(**jobschema.dict())
    # db.add(job)
    # db.commit()
    # db.refresh(job)
    skills = []
    Jobdesc = job.title + ' ' + job.description
    tokens = utils.generate_token(Jobdesc)
    print(tokens)
    for skill in db.query(models.FilterSkill).all():
        if skill.skill.lower() in tokens:
            skills.append(1)
            job.skill.add(skill)
        else:
            skills.append(0)
    JobSkill = job.skill.all()
    print(JobSkill)
    # for skill in models.Skill.objects.all():
    #     if skill in JobSkill:
    #         skills.append(1)
    #     else:
    #         skills.append(0)

    # skill_text = ''.join(map(str, skills))
    # print(skill_text)
    # models.JobProfile.objects.create(job=job, skills=skill_text)
    # return job


@app.get('/{user_id}')
async def job_recom(user_id: int, db: Session = Depends(get_database_session)):
    youth = db.query(models.FilterYouthprofile).filter_by(youth_id=user_id).first().skills
    print(youth)
    # youth = models.YouthProfile.objects.filter(youth_id=pk).first().skills
    youth_skills = list(map(int, tuple(youth)))
    #
    jobs = db.query(models.FilterJobprofile).all()
    # jobs = models.JobProfile.objects.all()
    recomjob = {}
    for job in jobs:
        job_skill = list(map(int, tuple(job.skills)))
        rate = utils.cos_similarity(job_skill, youth_skills) * 100
        recomjob[job] = rate
        print('-------------2334-------------')
    ids = [i[0] for i in sorted(recomjob.items(), key=lambda item: item[1], reverse=True)]
    # print(ids[0].job.title)
    # serializer = serializers.RecomJobSerializer(ids, many=True)
    return ids

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
