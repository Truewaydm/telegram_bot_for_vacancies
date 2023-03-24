import datetime
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from scraping.models import City, Vacancy, Language
from .serializers import *

period = datetime.date.today() - datetime.timedelta(1)


# class DateFilterBackend(filters.BaseFilterBackend):
#     """
#     Filter that only allows users to see their own objects.
#     https://www.django-rest-framework.org/api-guide/filtering/
#     """
#
#     def filter_queryset(self, request, queryset, view):
#         # return queryset.filter(timestamp__gte=period)
#         city_slug = request.query_params.get('city', None)
#         language_slug = request.query_params.get('language', None)
#         return queryset.filter(
#             city__slug=city_slug,
#             language__slug=language_slug,
#             timestamp__gte=period)


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class LanguageViewSet(ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class VacancyViewSet(ModelViewSet):
    """
    ?city=kyiv&language=python
    """
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # filter_backends = [DjangoFilterBackend, DateFilterBackend]
    # filterset_fields = ['city__slug', 'language__slug']

    def get_queryset(self):
        city_slug = self.request.query_params.get('city', None)
        language_slug = self.request.query_params.get('language', None)
        qs = None
        if city_slug and language_slug:
            qs = Vacancy.objects.filter(
                city__slug=city_slug,
                language__slug=language_slug, timestamp__gte=period)
            if not qs.exists():
                qs = Vacancy.objects.filter(
                    city__slug=language_slug,
                    language__slug=city_slug, timestamp__gte=period)
        self.queryset = qs
        return self.queryset

    # def get_queryset(self):
    #     city_slug = self.request.query_params.get('city', None)
    #     language_slug = self.request.query_params.get('language', None)
    #     qs = None
    #     if city_slug and language_slug:
    #         city = City.objects.filter(slug=city_slug).first()
    #         language = Language.objects.filter(slug=language_slug).first()
    #         if city and language:
    #             qs = Vacancy.objects.filter(city=city, language=language, timestamp__gte=period)
    #     self.queryset = qs
    #     return self.queryset
