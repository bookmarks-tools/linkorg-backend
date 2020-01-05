from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from slugify import slugify
from mongoengine import DoesNotExist
from models import Post, PostSchema, Tag, TagSchema, Provider

app = Flask(__name__)


@app.route('/posts', methods=['GET'])
def posts_get():
    schema = PostSchema()
    return jsonify([schema.dump(i) for i in Post.objects])


@app.route('/posts/<post_id>', methods=['DELETE'])
def posts_delete(post_id):
    Post.objects.get(id=post_id).delete()
    return 'OK'


@app.route('/tags', methods=['GET'])
def tags():
    schema = TagSchema()
    return jsonify([schema.dump(i) for i in Tag.objects])


@app.route('/posts', methods=['POST'])
def posts():
    post = request.get_json()
    provider = Provider(name=post['provider'])
    tags = post['tags']
    tag_refs = []
    for tag in tags:
        tag_id = tag.get('id')
        if tag_id:
            tag_ref = Tag.objects.get(id=tag_id)
        else:
            tag_ref = Tag(label=tag['label'], value=slugify(tag['label'])).save()
        tag_refs.append(tag_ref)
    try:
        provider_ref = Provider.objects.get(name=post['provider'])
    except DoesNotExist:
        provider_ref = Provider(name=post['provider']).save()
    post1 = Post(tags=tag_refs, provider=provider_ref, href=post['href'])
    post1.save()
    schema = PostSchema()
    return jsonify(schema.dump(post1))


CORS(app)
