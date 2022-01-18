import graphene

import demencia.schema


class Query(demencia.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
