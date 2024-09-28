from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db.models import F
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics

from .filters import PhoneFilter
from .forms import PhoneForm, BrandForm, ColorForm, CountryForm
from django.contrib import messages

from .models import Phone
from .serializers import PhoneListSerializer


class PhoneCreateView(View):
    form_class = PhoneForm
    template_name = 'warehouse/phone_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, "current_page": 'add phone'})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Save the form and redirect to a success page
            form.save()
            messages.success(request, "Phone successfully added!")
            return redirect('phone:add')
        else:
            # If the form is not valid, render the form with errors
            messages.error(request, "Please correct the errors below.")
            return render(request, self.template_name, {'form': form})


class ColorCreateView(View):
    form_class = ColorForm
    template_name = 'warehouse/color_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, "current_page": 'add color'})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Color successfully added!")
            return redirect('phone:color_add')
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, self.template_name, {'form': form})


class BrandCreateView(View):
    form_class = BrandForm
    template_name = 'warehouse/brand_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, "current_page": 'add brand'})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Brand successfully added!")
            return redirect('phone:brand_add')
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, self.template_name, {'form': form})


@extend_schema(
    description="search query",
    parameters=[
        OpenApiParameter(
            name="search",
            description="search query",
            required=False,
            type=str,
        ),
    ],
)
class PhoneListAPIView(generics.ListAPIView):
    """
    API view to list phones with the ability to filter and search using the search_vector.
    Supports searching by model and brand name along with existing filters.
    """
    serializer_class = PhoneListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PhoneFilter  # Use your PhoneFilter class

    def get_queryset(self):
        """
        Customizes the queryset to filter based on search criteria.
        Search is performed using the 'search_vector' field for full-text search.
        """
        queryset = Phone.objects.all()

        # Capture search query from URL parameters
        search_query = self.request.query_params.get('search', None)

        if search_query:
            # Create a SearchQuery object for the search term
            search_vector = SearchVector('model', 'brand__name')
            queryset = queryset.annotate(
                search=search_vector
            ).filter(
                search=SearchQuery(search_query)
            )

        return queryset


class CountryCreateView(View):
    form_class = CountryForm
    template_name = 'warehouse/country_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, "current_page": 'add country'})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Country successfully added!")
            return redirect('phone:country_add')
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, self.template_name, {'form': form})


@extend_schema(
    description="Retrieve phones based on country similarity.",
    parameters=[
        OpenApiParameter(
            name="country_similar",
            description="Set to 'true' to get phones where the country matches the brand's country. Set to 'false' to get phones where they differ.",
            required=False,
            type=bool,  # This indicates that it's a boolean parameter
        ),
    ],
)
class SimilarityPhoneListAPIView(generics.ListAPIView):
    serializer_class = PhoneListSerializer

    def get_queryset(self):
        # Get the country_similar query parameter and convert it to a boolean
        country_similar = self.request.query_params.get('country_similar', 'false').lower() == 'true'

        if country_similar:
            # If true, return phones where the country matches the brand's country
            return Phone.objects.filter(country__name=F('brand__country__name'))
        else:
            # If false, return phones where the country is different from the brand's country
            return Phone.objects.exclude(country__name=F('brand__country__name'))
