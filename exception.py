def exist_exception(db, model, field, validate_data):
    if bool(db.query(model).filter_by(field=getattr(validate_data, 'skill', None)).one_or_none()):
        raise HTTPException(
            status_code=404, detail=f"{getattr(skill, 'skill', None)} already in database"
        )