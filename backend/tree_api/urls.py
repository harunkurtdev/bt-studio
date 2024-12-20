from django.urls import path
from . import views

urlpatterns = [
    path("create_project/", views.create_project, name="create_project"),
    path("delete_project/", views.delete_project, name="delete_project"),
    path("delete_universe/", views.delete_universe, name="delete_universe"),
    path("save_project/", views.save_project, name="save_project"),
    path("get_project_graph/", views.get_project_graph, name="get_project_graph"),
    path("get_project_list/", views.get_project_list, name="get_project_list"),
    path("get_file_list/", views.get_file_list, name="get_file_list"),
    path("get_actions_list/", views.get_actions_list, name="get_actions_list"),
    path("get_universes_list/", views.get_universes_list, name="get_universes_list"),
    path("get_file/", views.get_file, name="get_file"),
    path("create_action/", views.create_action, name="create_action"),
    path("create_file/", views.create_file, name="create_file"),
    path("create_folder/", views.create_folder, name="create_folder"),
    path("rename_file/", views.rename_file, name="rename_file"),
    path("delete_file/", views.delete_file, name="delete_file"),
    path("save_file/", views.save_file, name="save_file"),
    path("translate_json/", views.translate_json, name="translate_json"),
    path("get_tree_structure/", views.get_tree_structure, name="get_tree_structure"),
    path(
        "get_subtree_structure/",
        views.get_subtree_structure,
        name="get_subtree_structure",
    ),
    path(
        "get_universe_configuration/",
        views.get_universe_configuration,
        name="get_universe_configuration",
    ),
    path("generate_app/", views.generate_app, name="generate_app"),
    path(
        "generate_dockerized_app/",
        views.generate_dockerized_app,
        name="generate_dockerized_app",
    ),
    path("get_universe_zip/", views.get_universe_zip, name="generate_app"),
    path("upload_universe/", views.upload_universe, name="upload_universe"),
    path("upload_code/", views.upload_code, name="upload_code"),
    path(
        "get_project_configuration/",
        views.get_project_configuration,
        name="get_project_configuration",
    ),
    path(
        "save_project_configuration/",
        views.save_project_configuration,
        name="save_project_configuration",
    ),
    path("get_subtree_list/", views.get_subtree_list, name="get_subtree_list"),
    path("create_subtree/", views.create_subtree, name="create_subtree"),
    path("get_subtree/", views.get_subtree, name="get_subtree"),
    path("save_subtree/", views.save_subtree, name="save_subtree"),
]
