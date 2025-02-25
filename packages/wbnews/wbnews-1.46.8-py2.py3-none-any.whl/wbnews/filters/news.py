from wbcore import filters as wb_filters

from wbnews.models import News


class NewsFilterSet(wb_filters.FilterSet):
    class Meta:
        model = News
        fields = {"title": ["icontains"], "datetime": ["lte", "gte"], "source": ["exact"], "language": ["exact"]}
