from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProjectViewSet, TaskViewSet, RoleViewSet, UserProjectRoleViewSet, CommentViewSet

app_name = 'users'

router = DefaultRouter()
router.register('users',UserViewSet)
router.register('projects', ProjectViewSet)
router.register('tasks', TaskViewSet)
router.register('roles', RoleViewSet)
router.register('comments', CommentViewSet)

project_router = DefaultRouter()
project_router.register('members', UserProjectRoleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('projects/<int:project_pk>/', include(project_router.urls))
]
