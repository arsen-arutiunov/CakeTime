from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
import logging


logger = logging.getLogger(__name__)


class CategoryViewSet(viewsets.ModelViewSet):
    """
        API endpoint for managing product categories.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Get all categories',
        operation_description="Retrieve a list of all categories",
        responses={200: CategorySerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get a specific category by ID",
        operation_description="Retrieve details of a specific category",
        responses={200: CategorySerializer(),
                   404: "Category not found"}
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            category = self.get_object()
        except NotFound:
            raise NotFound(detail="Category not found")
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new category",
        operation_description="Create a new category",
        request_body=CategorySerializer,
        responses={201: CategorySerializer()}
    )
    def create(self, request, *args, **kwargs):
        # Только администраторы могут создавать продукты
        if not request.user.is_staff:
            raise PermissionDenied(
                "You do not have permission to create categories."
            )
        response = super().create(request, *args, **kwargs)
        logger.info(
            f"Сategory created: {response.data['name']} by {request.user}"
        )
        return response

    @swagger_auto_schema(
        operation_summary="Update an existing category by ID",
        operation_description="Update an existing category",
        request_body=CategorySerializer,
        responses={200: CategorySerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update an existing category by ID",
        operation_description="Partially update an existing category",
        request_body=CategorySerializer,
        responses={200: CategorySerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete an existing category by ID",
        operation_description="Delete a category",
        responses={204: "Category deleted"}
    )
    def destroy(self, request, *args, **kwargs):
        # Только администраторы могут удалять категории
        if not request.user.is_staff:
            raise PermissionDenied(
                "You do not have permission to delete categories."
            )
        category = self.get_object()
        response = super().destroy(request, *args, **kwargs)
        logger.info(f"Category deleted: {category.name} by {request.user}")
        return response


class ProductViewSet(viewsets.ModelViewSet):
    """
        API endpoint for managing products.
        """

    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get all products",
        operation_description="Retrieve a list of all products",
        responses={200: ProductSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get a specific product by ID",
        operation_description="Retrieve details of a specific product",
        responses={200: ProductSerializer(),
                   404: "Product not found"}
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            product = self.get_object()
        except NotFound:
            raise NotFound(detail="Product not found")
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new product",
        operation_description="Create a new product",
        request_body=ProductSerializer,
        responses={201: ProductSerializer()}
    )
    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:  # Только администраторы могут создавать продукты
            raise PermissionDenied(
                "You do not have permission to create products."
            )
        response = super().create(request, *args, **kwargs)
        logger.info(
            f"Product created: {response.data['name']} by {request.user}"
        )
        return response

    @swagger_auto_schema(
        operation_summary="Update an existing product by ID",
        operation_description="Update an existing product",
        request_body=ProductSerializer,
        responses={200: ProductSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update an existing product by ID",
        operation_description="Partially update an existing product",
        request_body=ProductSerializer,
        responses={200: ProductSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete an existing product by ID",
        operation_description="Delete a product",
        responses={204: "Product deleted"}
    )
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:  # Только администраторы могут удалять продукты
            raise PermissionDenied(
                "You do not have permission to delete products."
            )
        product = self.get_object()
        response = super().destroy(request, *args, **kwargs)
        logger.info(f"Product deleted: {product.name} by {request.user}")
        return response
