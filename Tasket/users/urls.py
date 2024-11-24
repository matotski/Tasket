from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet, ProjectViewSet, TaskViewSet, RoleViewSet, UserProjectRoleViewSet, CommentViewSet, RegisterView

app_name = 'users'

router = DefaultRouter()
router.register('users',UserViewSet)
router.register('projects', ProjectViewSet)

project_router = DefaultRouter()
project_router.register('roles', RoleViewSet)
project_router.register('tasks', TaskViewSet)
project_router.register('members', UserProjectRoleViewSet)

task_router = DefaultRouter()
task_router.register('comments', CommentViewSet)

# project_router = NestedDefaultRouter(router, 'projects')
# project_router.register('roles', RoleViewSet)
# project_router.register('tasks', TaskViewSet)
# project_router.register('members', UserProjectRoleViewSet)

# task_router = NestedDefaultRouter(project_router, 'tasks')
# task_router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('projects/<int:project_pk>/', include(project_router.urls)),
    path('projects/<int:project_pk>/tasks/<int:task_pk>/', include(task_router.urls)),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
]
