

def create_object():
    name = getattr(actor, 'name', None)
        if bool(db.query(model.Actor).filter_by(name=name).one_or_none()):
            print(name)
            raise HTTPException(
                status_code=404, detail=f"{getattr(actor, 'name', None)} already in database"
            )
        db_actor = model.Actor(**actor.dict())
        db.add(db_actor)
        db.commit()
        db.refresh(db_actor)
        return db_actor