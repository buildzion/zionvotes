import base64
import uuid


def random_slug(prefix='', length_limit=26):
    slug = base64.b32encode(uuid.uuid4().bytes).decode('utf8').rstrip('=').lower()[:length_limit]
    return "{}-{}".format(prefix, slug) if prefix else slug
