from django.test import RequestFactory
from haystack import fields, indexes
from leonardo.module.web.models import Page
from leonardo.templatetags.leonardo_tags import _render_content


class PageIndex(indexes.SearchIndex, indexes.Indexable):

    """
    Index for FeinCMS Page objects

    Body is generated using a complex template which includes rendered content
    for many content objects
    """

    url = fields.CharField(model_attr="_cached_url")
    text = fields.CharField(document=True, use_template=True)

    title = fields.CharField(model_attr="title")
    slug = fields.CharField(model_attr="slug")
    page_title = fields.CharField(model_attr="_page_title")
    meta_description = fields.CharField(model_attr="meta_description")
    meta_keywords = fields.CharField(model_attr="meta_keywords")
    content_title = fields.CharField(model_attr="_content_title")
    content = fields.CharField()

    creation_date = fields.DateTimeField(model_attr='creation_date', null=True)
    modification_date = fields.DateTimeField(
        model_attr='modification_date', null=True)

    def prepare_content(self, obj):
        request_factory = RequestFactory()
        request = request_factory.get(
            obj.get_absolute_url(), data={'name': u'test'})
        content = ''.join(
            _render_content(content, request=request, context={})
            for content in getattr(obj.content, 'col3'))
        return content

    def should_update(self, instance, **kwargs):
        return instance.is_active()

    def get_model(self):
        return Page

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(active=True)

# I don't know if this date is changed if some widget was changed..
#    def get_updated_field(self):
#        return "modification_date"
