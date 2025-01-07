from django.db.models import prefetch_related_objects
from rest_framework import mixins, response, viewsets


class PatchModelMixin:
    """Миксим только для частичного обновления."""

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        queryset = self.filter_queryset(self.get_queryset())
        if queryset._prefetch_related_lookups:
            instance._prefetched_objects_cache = {}
            prefetch_related_objects(
                [instance], *queryset._prefetch_related_lookups
            )
        return response.Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class ListCreateMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """Вьюсет для списков и создания объекта."""

    pass


class ListCreateDestroyMixin(
    mixins.DestroyModelMixin,
    ListCreateMixin,
):
    """Вьюсет с действиями для списка, создания и удаления объектов."""

    pass


class CRUDMixin(
    PatchModelMixin,
    mixins.RetrieveModelMixin,
    ListCreateDestroyMixin,
):
    """CRUD вьюсет без поддержки PUT метода."""

    pass
