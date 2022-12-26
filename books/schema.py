import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Book, Category, Question, Quizzes, Answer

# without
class BooksType(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()

    def resolve_id(self, info):
        return self.id

    def resolve_title(self, info):
        return self.title

    def resolve_description(self, info):
        return self.description

# class BooksType(DjangoObjectType):    # like serializer or model form
    # class Meta:
    #     model = Book
    #     fields = ['id', 'title', 'description']


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ['id', 'name']


class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = ['id', 'title', 'category', 'quiz']


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ['title', 'quiz']


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ['question', 'answer_text']


class Query(graphene.ObjectType):
    all_books = graphene.List(BooksType)    # graphene.List and DjangoListField both will do same work
    all_quizzes = DjangoListField(QuizzesType)
    question = graphene.Field(QuestionType, id=graphene.Int())  # getting and individual question object
    answer = graphene.Field(AnswerType, id=graphene.Int())

    def resolve_all_books(self, info):   # why not taking self
        return Book.objects.all()
        # return Book.objects.filter(title="Lion King")

    def resolve_all_quizzes(self, info):
        return Quizzes.objects.all()

    def resolve_question(self, info, id):
        return Question.objects.get(pk=id)

    def resolve_answer(self, info, id):
        return Answer.objects.get(question=id)   # if returning queryset then causing problem


""" Mutations in django-GraphQL"""


class CategoryMutationCreate(graphene.Mutation):    # Mutation for creating category
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, self, info, name):
        category = Category(name=name)
        category.save()
        return CategoryMutationCreate(category=category)


class CategoryMutationUpdate(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, self, info, name, id):
        category = Category.objects.get(pk=id)
        category.name = name
        category.save()
        return CategoryMutationUpdate(category=category)


class CategoryMutationDelete(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, self, info, id):
        category = Category.objects.get(pk=id)
        print(category)
        category.delete()
        return "data deleted"


class Mutation(graphene.ObjectType):
    create_category = CategoryMutationCreate.Field()
    update_category = CategoryMutationUpdate.Field()
    delete_category = CategoryMutationDelete.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)    # building schema for graphql like we used to build in SQL
