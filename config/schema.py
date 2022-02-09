import graphene

import demencia.schema
import dementia_test.schema


class Query(demencia.schema.Query, graphene.ObjectType):
    pass


class Mutation(dementia_test.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
