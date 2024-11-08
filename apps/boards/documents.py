from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Post


@registry.register_document
class PostDocument(Document):
    author = fields.ObjectField(
        properties={
            "id": fields.IntegerField(),
            "username": fields.TextField(),
        }
    )
    board = fields.ObjectField(
        properties={
            "id": fields.IntegerField(),
            "title": fields.TextField(),
            "description": fields.TextField(),
        }
    )
    title = fields.TextField(analyzer="nori_analyzer")
    content = fields.TextField(analyzer="nori_analyzer")

    class Index:
        name = "posts"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
                "analyzer": {
                    "nori_analyzer": {
                        "type": "custom",
                        "tokenizer": "nori_tokenizer",
                    }
                }
            },
        }

    class Django:
        model = Post
        fields = ["id", "views", "is_deleted", "created_at", "updated_at"]


# python manage.py search_index --rebuild
