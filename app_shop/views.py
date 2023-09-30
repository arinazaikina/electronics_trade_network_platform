from django.core.exceptions import ValidationError
from django.db.models import Model
from mptt.exceptions import InvalidMove
from rest_framework import status
from rest_framework import viewsets, filters
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Supplier, Product
from .serializers import SupplierSerializer, ProductSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.get_all_suppliers()
    serializer_class = SupplierSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['country']
    http_method_names = ['get', 'post', 'delete', 'patch']

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление объекта поставщика.

        Перед удалением проверяет, есть ли у поставщика или его дочерних элементов
        на следующем уровне иерархи долг.
        Если есть долг, возвращает ошибку.
        В противном случае удаляет поставщика.

        :param request: Объект запроса DRF.
        """
        instance = self.get_object()
        can_delete, debtor = instance.can_be_deleted()

        if not can_delete:
            return self._deletion_error_response(instance, debtor)

        self._reparent_children(instance)
        self.perform_destroy(instance)
        Supplier.objects.rebuild()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def _deletion_error_response(instance: Model, debtor: Supplier) -> Response:
        """
        Формирует ответ с ошибкой при попытке удаления объекта с долгом.

        :param instance: Объект, который пытаются удалить.
        :param debtor: Объект с долгом.
        """
        if debtor == instance:
            return Response(
                {"error": f"Ошибка: нельзя удалить звено {instance.name} с долгом перед поставщиком"},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response({
                "error": f"Ошибка: нельзя удалить звено {instance.name}, так как у его поставщика "
                         f"{debtor.name} на следующем уровне иерархии есть долг"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def _reparent_children(instance: Supplier) -> None:
        """
        Переназначает родителя для дочерних объектов перед удалением родителя.

        :param instance: Родительский объект, который планируется удалить.
        """
        children = instance.get_children()
        for child in children:
            child.parent = instance.parent
            child.save()

    def update(self, request: Request, *args, **kwargs) -> Response:
        """
        Обновление объекта поставщика.

        Перед сохранением объекта проверяет наличие исключений валидации.
        В случае ошибки возвращает соответствующий ответ.

        :param request: Объект запроса DRF.
        """
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidMove:
            return Response({'error': 'Зацикленные отношения не допустимы'}, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.get_all_products()
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post', 'delete', 'patch']
