from rest_framework.serializers import ValidationError

from ...helpers.serialization_errors import error_dict
from ..models import Post


def retrieve_post_by_id(query_instance, post_id):
    """Retrieves a post by its id."""
    try:
        return query_instance.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise ValidationError(error_dict['does_not_exist'].format("Post"))


def validate_author(is_author):
    """Function that validates the author of a post."""
    if not is_author:
        raise ValidationError(error_dict['object_permission_denied'].format("post"))