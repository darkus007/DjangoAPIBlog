from rest_framework.routers import SimpleRouter

from .views import UserViewSet, PostViewSet

# строим автоматические маршруты для наборов представлений
router = SimpleRouter()
router.register('users', UserViewSet, basename='users')
router.register('', PostViewSet, basename='posts')
urlpatterns = router.urls
