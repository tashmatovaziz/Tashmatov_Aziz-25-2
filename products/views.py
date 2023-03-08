from django.shortcuts import HttpResponse, render, redirect
from datetime import datetime
from products.models import Products, Hashtag, Review
from products.forms import ReviewCreateform, ProductCreateForm
from products.constants import PAGINATION_LIMIT
from django.views.generic import ListView, CreateView, DetailView, DeleteView


def hello(request):
    if request.method == 'GET':
        return HttpResponse('Hello! Its my project')


def now_date(request):
    if request.method == 'GET':
        return HttpResponse(datetime.now())


def goodby(request):
    if request.method == 'GET':
        return HttpResponse('Goodby User!')


class MainPageCBV(ListView):
    model = Products


# def hashtags(request):
#     if request.method == 'GET':
#         Hashtags = Hashtag.objects.all()
#         context = {
#             'Hashtags': Hashtags
#         }
#         return render(request, 'hashtag/Hashtags.html', context=context)


class HashtagCBV(ListView):
    model = Hashtag
    template_name = 'hashtag/Hashtags.html'

    def get(self, request, *args, **kwargs):
        Hashtags = self.get_queryset().objects.all()
        context = {
            'Hashtags': Hashtags
        }
        return render(request, self.template_name, context=context)


# def products_view(request):
#     if request.method == 'GET':
#         products = Products.objects.all().order_by('-created_date')
#         search = request.GET.get('search')
#         page = int(request.GET.get('page', 1))
#
#         if search:
#             products = products.filter(title__contains=search) | products.filter(description__contains=search)
#
#         max_page = products.__len__() / PAGINATION_LIMIT
#
#         if round(max_page) < max_page:
#             max_page = round(max_page + 1)
#         else:
#             max_page = round(max_page)
#
#         products = products[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]
#
#         context = {
#             'products': [
#                 {
#                     'id': product.id,
#                     'title': product.title,
#                     'price': product.price,
#                     'rate': product.rate,
#                     'image': product.image,
#                     'hashtags': product.hashtags.all()
#                 }
#                 for product in products
#             ],
#             'user': request.user,
#             'pages': range(1, max_page + 1),
#         }
#
#         return render(request, 'products/products.html', context=context)

class ProductsCBV(ListView):
    model = Products
    template_name = 'products/products.html'

    def get(self, request, *args, **kwargs):
        products = self.get_queryset().order_by('-created_date')
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if search:
            products = products.filter(title__contains=search) | products.filter(description__contains=search)

        max_page = products.__len__() / PAGINATION_LIMIT

        if round(max_page) < max_page:
            max_page = round(max_page + 1)
        else:
            max_page = round(max_page)

        products = products[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]

        context = {
            'products': [
                {
                    'id': product.id,
                    'title': product.title,
                    'price': product.price,
                    'rate': product.rate,
                    'image': product.image,
                    'hashtags': product.hashtags.all()
                }
                for product in products
            ],
            'user': request.user,
            'pages': range(1, max_page + 1),
        }

        return render(request, self.template_name, context=context)


def product_detail_view(request, id):
    if request.method == 'GET':
        product = Products.objects.get(id=id)

        context = {
            'product': product,
            'reviews': product.Reviews.all(),
            'form': ReviewCreateform
        }

        return render(request, 'products/detail.html', context=context)

    if request.method == 'POST':
        data = request.POST

        form = ReviewCreateform(data=data)
        product = Products.objects.get(id=id)

        if form.is_valid():
            Review.objects.create(
                text=form.cleaned_data.get('text'),
                product=product
            )

        context = {
            'product': product,
            'review': product.Reviews.all,
            'form': form
        }
        return render(request, 'products/detail.html', context=context)


# def create_product_veiw(request):
#     if request.method == 'GET':
#         context = {
#             'form': ProductCreateForm
#         }
#         return render(request, 'products/create.html', context=context)
#
#     if request.method == 'POST':
#         data, files = request.POST, request.FILES
#
#         form = ProductCreateForm(data, files)
#
#         if form.is_valid():
#             Products.objects.create(
#                 image=form.cleaned_data.get('image'),
#                 title=form.cleaned_data.get('title'),
#                 price=form.cleaned_data.get('price'),
#                 description=form.cleaned_data.get('description'),
#                 rate=form.cleaned_data.get('rate')
#             )
#             return redirect('/products')
#         return render(request, 'products/create.html', context={
#             "form": form
#         })


class CreateProductsCBV(ListView, CreateView):
    model = Products
    template_name = 'products/create.html'
    form_class = ProductCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'form': self.form_class if not kwargs.get('form') else kwargs['form']
        }

    def get(self, request, **kwargs):
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request, **kwargs):
        data, files = request.POST, request.FILES

        form = self.form_class(data, files)

        if form.is_valid():
            self.model.objects.create(
                image=form.cleaned_data.get('image'),
                title=form.cleaned_data.get('title'),
                price=form.cleaned_data.get('price'),
                description=form.cleaned_data.get('description'),
                rate=form.cleaned_data.get('rate')
            )
            return redirect('/products')
        return render(request, self.template_name, context=self.get_context_data(form=form))