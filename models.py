from mongoengine import *
import datetime
from slugify import slugify
from marshmallow import Schema, fields

connect('mydb')


class Provider(Document):
    name = StringField()


class ProviderSchema(Schema):
    name = fields.String()


class Tag(Document):
    label = StringField(unique=True)
    value = StringField()


class Post(Document):
    tags = ListField(ReferenceField(Tag))
    href = StringField(max_length=512)
    provider = ReferenceField(Provider)


class TagSchema(Schema):
    id = fields.String()
    label = fields.String()
    value = fields.String()


class PostSchema(Schema):
    id = fields.String()
    href = fields.String()
    provider = fields.Nested(ProviderSchema())
    tags = fields.List(fields.Nested(TagSchema()))


if __name__ == '__main__':
    # provider = Provider(name="twitter").save()
    # tag1 = Tag(label="kek lol", value=slugify("kek lol")).save()
    # tag2 = Tag(label="lol kek", value=slugify("lol kek")).save()
    # post1 = Post(tags=[tag1, tag2], provider=provider, href="https://twitter.com/dan_abramov/status/1176597851822010375")
    # post1.save()
    # print(Tag.objects.get(id='5d8f915a85690acacb15475b').label)
    # print(Tag.objects)
    # schema = TagSchema()
    # print([schema.dump(i) for i in Tag.objects])
    # schema = PostSchema()
    # print([schema.dump(i) for i in Post.objects])
    try: 
        print(Provider.objects.get(name="twitte"))
    except DoesNotExist:
        print("kek")
