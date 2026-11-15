from rest_framework.routers import DefaultRouter

from viagens.api.views import CategoriaViewSet, ViagemViewSet

router = DefaultRouter()
router.register("viagens", ViagemViewSet, basename="viagem")
router.register("categorias", CategoriaViewSet, basename="categoria")

urlpatterns = router.urls
