from haystack import indexes
from models import Product

class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    category = indexes.CharField(model_attr='category.slug')
    def get_model(self):
        return Product
    
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all() #filter(pub_date__lte=datetime.datetime.now())

