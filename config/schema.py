import graphene
import demencia.schema
import demencia.mutations


class Query(demencia.schema.Query, graphene.ObjectType):
    pass


class Mutation(demencia.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
