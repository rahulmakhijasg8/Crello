from . import views
from rest_framework_nested import routers
from pprint import pprint

router = routers.DefaultRouter()
router.register('workspaces',views.WorkspaceViewset,basename='workspaces')
# router.register('columns',views.ColumnViewset,basename='columns')
router.register('worskpace/<int:id>/columns',views.ColumnViewset,basename='workspace-columns')
workspace_column = routers.NestedDefaultRouter(router,'worskpace/<int:id>/columns',lookup = 'column')
workspace_column.register('cards',views.CardViewset,basename='workspace-column-cards')
workspace_router = routers.NestedDefaultRouter(router,'workspaces',lookup='workspace')
workspace_router.register('columns',views.ColumnViewset,basename='workspace-columns')
workspace_router.register('cards',views.CardViewset,basename='workspace-cards')
# pprint(workspace_column.urls)
# column_router = routers.NestedDefaultRouter(router,'columns',lookup='column'

urlpatterns = router.urls + workspace_router.urls
                # + workspace_column.urls