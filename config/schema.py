import graphene

import demencia_test.schema

import demencia.schema


class Query(demencia.schema.Query, graphene.ObjectType):
    pass


class Mutation(demencia_test.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
