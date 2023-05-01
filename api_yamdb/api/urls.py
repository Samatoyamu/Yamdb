from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (GetTokenView, RegistrationView,
                    CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet,
                    TitleViewSet, UserViewSet)

router = DefaultRouter()
auth_urls = [
    path('signup/', RegistrationView.as_view(), name='register'),
    path('token/', GetTokenView.as_view(), name='token')
]
router.register(r'users', UserViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'categories', CategoryViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')
router.register(r'titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_urls)),
]
