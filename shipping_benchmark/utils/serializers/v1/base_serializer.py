from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemyAutoSchemaOpts


class BaseModelSchemaOpts(SQLAlchemyAutoSchemaOpts):
    def __init__(self, meta, *args, **kwargs):
        super(BaseModelSchemaOpts, self).__init__(meta=meta, *args, **kwargs)
        self.include_fk = getattr(meta, "include_fk", True)
        self.include_relationships = getattr(meta, "include_relationships", True)


class BaseModelSchema(SQLAlchemyAutoSchema):
    OPTIONS_CLASS = BaseModelSchemaOpts
