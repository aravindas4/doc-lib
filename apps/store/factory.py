import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "store.User"
        django_get_or_create = ("username",)

    email = factory.Faker("ascii_safe_email")
    username = factory.lazy_attribute(lambda obj: f"{obj.email}")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")


class DocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "store.Document"

    owner = factory.SubFactory(UserFactory)


class UserDocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "store.UserDocument"

    user = factory.SubFactory(UserFactory)
    document = factory.SubFactory(DocumentFactory)
