from ninja import Router
from .models import Category, Model
from ninja import Schema

router = Router()


class CategoryIN(Schema):
    title: str

class ModelIn(Schema):
    title: str
    price: int
    category_id: int


@router.get("categories")
def get_categories(request, contain: str = None):
    categories = Category.objects.all()
    if contain is not None:
        categories = categories.filter(title__icontains=contain)
    return {"categories": [c.to_json() for c in categories]}

@router.get("models")
def get_models(request, min_price: int = None, max_price: int = None, category : str = None):
    models = Model.objects.all()
    if min_price is not None:
        models = models.filter(price__gte=min_price)
    if max_price is not None:
        models = models.filter(price__lte=max_price)
    if category is not None:
        models = models.filter(category__title=category)
    return {"models": [m.to_json() for m in models]}



@router.post("categories")
def create_category(request, data: CategoryIN):

    new_category = Category.objects.create(title=data.title)
    return new_category.to_json()

@router.post("models")
def create_model(request, data: ModelIn):

    new_model = Model.objects.create(
        title=data.title,
        price=data.price,
        category_id=data.category_id
    )
    return new_model.to_json()