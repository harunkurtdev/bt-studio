import glob
import os
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import FileContentSerializer
from . import app_generator
from . import tree_generator
from . import json_translator
from . import templates
from .project_view import list_dir, EntryEncoder
from django.http import HttpResponse
from django.http import JsonResponse
import mimetypes
import json
import shutil
import zipfile
from rest_framework import status
from django.core.files.storage import default_storage
import base64


@api_view(["GET"])
def create_project(request):

    project_name = request.GET.get("project_name")
    folder_path = os.path.join(settings.BASE_DIR, "filesystem")
    project_path = os.path.join(folder_path, project_name)
    action_path = os.path.join(project_path, "code/actions")
    universes_path = os.path.join(project_path, "universes")

    if not os.path.exists(project_path):
        os.mkdir(project_path)
        os.mkdir(action_path)
        os.mkdir(universes_path)
        return Response({"success": True})
    else:
        return Response(
            {"success": False, "message": "Project already exists"}, status=400
        )


@api_view(["GET"])
def delete_project(request):
    project_name = request.GET.get("project_name")
    folder_path = os.path.join(settings.BASE_DIR, "filesystem")
    project_path = os.path.join(folder_path, project_name)

    if os.path.exists(project_path):
        shutil.rmtree(project_path)
        return Response({"success": True})
    else:
        return Response(
            {"success": False, "message": "Project does not exist"}, status=400
        )


@api_view(["GET"])
def delete_universe(request):
    project_name = request.GET.get("project_name")
    universe_name = request.GET.get("universe_name")

    folder_path = os.path.join(settings.BASE_DIR, "filesystem")
    project_path = os.path.join(folder_path, project_name)
    universes_path = os.path.join(project_path, "universes/")
    universe_path = os.path.join(universes_path, universe_name)

    if os.path.exists(universe_path):
        shutil.rmtree(universe_path)
        return Response({"success": True})
    else:
        return Response(
            {"success": False, "message": "Project does not exist"}, status=400
        )


@api_view(["GET"])
def get_project_list(request):

    folder_path = os.path.join(settings.BASE_DIR, "filesystem")

    try:
        # List all folders in the directory
        project_list = [
            d
            for d in os.listdir(folder_path)
            if os.path.isdir(os.path.join(folder_path, d))
        ]

        # Return the list of projects
        return Response({"project_list": project_list})

    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)


@api_view(["POST"])
def save_project(request):

    # Get the app name and the graph
    project_name = request.data.get("project_name")
    graph_json = request.data.get("graph_json")

    # Generate the paths
    base_path = os.path.join(settings.BASE_DIR, "filesystem")
    project_path = os.path.join(base_path, project_name)
    graph_path = os.path.join(project_path, "code/graph.json")

    if project_path and graph_json:

        try:
            # Obtain pretty json
            graph = json.loads(graph_json)
            graph_formated = json.dumps(graph, indent=4)

            with open(graph_path, "w") as f:
                f.write(graph_formated)

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse(
                {"success": False, "message": f"Error deleting file: {str(e)}"},
                status=500,
            )
    else:
        return Response({"error": "app_name parameter is missing"}, status=400)


@api_view(["GET"])
def get_project_graph(request):

    project_name = request.GET.get("project_name")

    # Generate the paths
    base_path = os.path.join(settings.BASE_DIR, "filesystem")
    project_path = os.path.join(base_path, project_name)
    graph_path = os.path.join(project_path, "code/graph.json")

    # Check if the project exists
    if os.path.exists(graph_path):
        try:
            with open(graph_path, "r") as f:
                graph_data = json.load(f)
            return JsonResponse({"success": True, "graph_json": graph_data})
        except Exception as e:
            return JsonResponse(
                {"success": False, "message": f"Error reading file: {str(e)}"},
                status=500,
            )
    else:
        return Response(
            {"error": "The project does not have a graph definition"}, status=404
        )


@api_view(["GET"])
def get_universes_list(request):

    project_name = request.GET.get("project_name")
    folder_path = os.path.join(settings.BASE_DIR, "filesystem")
    project_path = os.path.join(folder_path, project_name)
    universes_path = os.path.join(project_path, "universes/")

    try:
        # List all files in the directory
        universes_list = [
            d
            for d in os.listdir(universes_path)
            if os.path.isdir(os.path.join(universes_path, d))
        ]

        # Return the list of files
        return Response({"universes_list": universes_list})

    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)


@api_view(["GET"])
def get_universe_configuration(request):

    project_name = request.GET.get("project_name")
    universe_name = request.GET.get("universe_name")

    folder_path = os.path.join(settings.BASE_DIR, "filesystem")
    project_path = os.path.join(folder_path, project_name)
    universes_path = os.path.join(project_path, "universes/")

    if universe_name:
        universe_path = os.path.join(universes_path, universe_name)
        config_path = os.path.join(universe_path, "config.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                content = f.read()
            return Response(content)
        else:
            return Response({"error": "File not found"}, status=404)
    else:
        return Response({"error": "Universe parameter is missing"}, status=400)


@api_view(["GET"])
def import_universe_from_zip(request):

    project_name = request.GET.get("project_name")
    zip_file = request.GET.get("zip_file")

    folder_path = os.path.join(settings.BASE_DIR, "filesystem")
    project_path = os.path.join(folder_path, project_name)
    universes_path = os.path.join(project_path, "universes/")


@api_view(["GET"])
def get_file_list(request):

    project_name = request.GET.get("project_name")
    folder_path = os.path.join(settings.BASE_DIR, "filesystem")
    project_path = os.path.join(folder_path, project_name)
    action_path = os.path.join(project_path, "code")

    try:
        # List all files in the directory
        file_list = [
            os.path.relpath(f, action_path)
            for f in glob.glob(action_path + "/**", recursive=True)
        ]

        file_list = list_dir(action_path)

        # Return the list of files
        return Response({"file_list": EntryEncoder().encode(file_list)})

    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)


@api_view(["GET"])
def get_actions_list(request):

    project_name = request.GET.get("project_name")
    folder_path = os.path.join(settings.BASE_DIR, "filesystem")
    project_path = os.path.join(folder_path, project_name)
    action_path = os.path.join(project_path, "code/actions")

    try:
        # List all actions in the directory
        actions_list = [
            f
            for f in os.listdir(action_path)
            if os.path.isfile(os.path.join(action_path, f))
        ]

        # Return the list of files
        return Response({"actions_list": actions_list})

    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)


@api_view(["GET"])
def get_file(request):

    project_name = request.GET.get("project_name", None)
    filename = request.GET.get("filename", None)

    # Make folder path relative to Django app
    folder_path = os.path.join(settings.BASE_DIR, "filesystem")
    project_path = os.path.join(folder_path, project_name)
    action_path = os.path.join(project_path, "code")

    if filename:
        file_path = os.path.join(action_path, filename)
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                content = f.read()
            serializer = FileContentSerializer({"content": content})
            return Response(serializer.data)
        else:
            return Response({"error": "File not found"}, status=404)
    else:
        return Response({"error": "Filename parameter is missing"}, status=400)


@api_view(["GET"])
def create_file(request):

    # Get the file info
    project_name = request.GET.get("project_name", None)
    filename = request.GET.get("filename", None)
    template = request.GET.get("template", None)

    # Make folder path relative to Django app
    folder_path = os.path.join(settings.BASE_DIR, "filesystem")
    project_path = os.path.join(folder_path, project_name)
    action_path = os.path.join(project_path, "code/actions")
    file_path = os.path.join(action_path, filename)

    if not os.path.exists(file_path):
        if templates.create_file_from_template(file_path, filename, template):
            return Response({"success": True})
        else:
            return Response(
                {"success": False, "message": "Template does not exist"}, status=400
            )
    else:
        return Response(
            {"success": False, "message": "File already exists"}, status=400
        )


@api_view(["GET"])
def delete_file(request):

    # Get the file info
    project_name = request.GET.get("project_name", None)
    path = request.GET.get("path", None)

    # Make folder path relative to Django app
    folder_path = os.path.join(settings.BASE_DIR, "filesystem")
    project_path = os.path.join(folder_path, project_name)
    action_path = os.path.join(project_path, "code")
    rel_path = os.path.relpath(path, action_path)
    file_path = os.path.join(action_path, rel_path)
    print(file_path)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse(
                {"success": False, "message": f"Error deleting file: {str(e)}"},
                status=500,
            )
    else:
        return JsonResponse(
            {"success": False, "message": "File does not exist"}, status=404
        )


@api_view(["POST"])
def save_file(request):

    project_name = request.data.get("project_name")
    filename = request.data.get("filename")
    content = request.data.get("content")

    folder_path = os.path.join(settings.BASE_DIR, "filesystem")
    project_path = os.path.join(folder_path, project_name)
    action_path = os.path.join(project_path, "code/actions")
    file_path = os.path.join(action_path, filename)

    # If file doesn't exist simply return
    if not os.path.exists(file_path):
        return JsonResponse(
            {"success": False, "message": "File does not exist"}, status=404
        )

    try:
        with open(file_path, "w") as f:
            f.write(content)
        return Response({"success": True})
    except Exception as e:
        return Response({"success": False, "message": str(e)}, status=400)


@api_view(["GET"])
def get_project_configuration(request):

    project_name = request.GET.get("project_name")

    folder_path = os.path.join(settings.BASE_DIR, "filesystem")

    if project_name:
        project_path = os.path.join(folder_path, project_name)
        config_path = os.path.join(project_path, "config.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                content = f.read()
            return Response(content)
        else:
            return Response({"error": "File not found"}, status=404)
    else:
        return Response({"error": "Project parameter is missing"}, status=400)


@api_view(["POST"])
def save_project_configuration(request):

    project_name = request.data.get("project_name")

    folder_path = os.path.join(settings.BASE_DIR, "filesystem")
    project_path = os.path.join(folder_path, project_name)
    config_path = os.path.join(project_path, "config.json")

    try:
        content = request.data.get("settings")
        if content is None:
            return Response(
                {"success": False, "message": "Settings are missing"}, status=400
            )

        d = json.loads(content)

        with open(config_path, "w") as f:
            json.dump(d, f, indent=4)

        return Response({"success": True})
    except Exception as e:
        return Response({"success": False, "message": str(e)}, status=400)


@api_view(["POST"])
def translate_json(request):

    folder_path = os.path.join(settings.BASE_DIR, "filesystem")
    bt_order = request.data.get("bt_order")

    try:
        content = request.data.get("content")
        if content is None:
            return Response(
                {"success": False, "message": "Content is missing"}, status=400
            )

        # Pass the JSON content to the translate function
        json_translator.translate(content, folder_path + "/tree.xml", bt_order)

        return Response({"success": True})
    except Exception as e:
        return Response({"success": False, "message": str(e)}, status=400)


@api_view(["POST"])
def generate_app(request):

    if (
        "app_name" not in request.data
        or "tree_graph" not in request.data
        or "bt_order" not in request.data
    ):
        return Response(
            {"error": "Incorrect request parameters"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Get the parameters
    app_name = request.data.get("app_name")
    tree_graph = request.data.get("tree_graph")
    bt_order = request.data.get("bt_order")

    # Make folder path relative to Django app
    base_path = os.path.join(settings.BASE_DIR, "filesystem")
    project_path = os.path.join(base_path, app_name)
    action_path = os.path.join(project_path, "code/actions")
    tree_path = os.path.join("/tmp/tree.xml")
    self_contained_tree_path = os.path.join("/tmp/self_contained_tree.xml")
    template_path = os.path.join(settings.BASE_DIR, "ros_template")
    tree_gardener_src = os.path.join(settings.BASE_DIR, "tree_gardener")

    try:
        # Generate a basic tree from the JSON definition
        json_translator.translate(tree_graph, tree_path, bt_order)

        # Generate a self-contained tree
        tree_generator.generate(tree_path, action_path, self_contained_tree_path)

        # Using the self-contained tree, package the ROS 2 app
        zip_file_path = app_generator.generate(
            self_contained_tree_path,
            app_name,
            template_path,
            action_path,
            tree_gardener_src,
        )

        # Confirm ZIP file exists
        if not os.path.exists(zip_file_path):
            return Response(
                {"success": False, "message": "ZIP file not found"}, status=400
            )

        # Prepare file response
        zip_file = open(zip_file_path, "rb")
        mime_type, _ = mimetypes.guess_type(zip_file_path)
        response = HttpResponse(zip_file, content_type=mime_type)
        response["Content-Disposition"] = (
            f"attachment; filename={os.path.basename(zip_file_path)}"
        )

        return response

    except Exception as e:
        return Response({"success": False, "message": str(e)}, status=400)


@api_view(["POST"])
def generate_dockerized_app(request):

    # Check if 'name' and 'zipfile' are in the request data
    if "app_name" not in request.data or "tree_graph" not in request.data:
        return Response(
            {"error": "Incorrect request parameters"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Get the request parameters
    app_name = request.data.get("app_name")
    tree_graph = request.data.get("tree_graph")
    bt_order = request.data.get("bt_order")

    # Make folder path relative to Django app
    base_path = os.path.join(settings.BASE_DIR, "filesystem")
    project_path = os.path.join(base_path, app_name)
    action_path = os.path.join(project_path, "code/actions")

    working_folder = "/tmp/wf"
    tree_path = "/tmp/tree.xml"
    self_contained_tree_path = os.path.join(working_folder, "self_contained_tree.xml")
    tree_gardener_src = os.path.join(settings.BASE_DIR, "tree_gardener")
    template_path = os.path.join(settings.BASE_DIR, "ros_template")

    if app_name and tree_graph:

        try:
            # 1. Create the working folder
            if os.path.exists(working_folder):
                shutil.rmtree(working_folder)
            os.mkdir(working_folder)

            # 2. Generate a basic tree from the JSON definition
            json_translator.translate(tree_graph, tree_path, bt_order)

            # 3. Generate a self-contained tree
            tree_generator.generate(tree_path, action_path, self_contained_tree_path)

            # 4. Copy necessary files to execute the app in the RB
            factory_location = tree_gardener_src + "/tree_gardener/tree_factory.py"
            tools_location = tree_gardener_src + "/tree_gardener/tree_tools.py"
            entrypoint_location = template_path + "/ros_template/execute_docker.py"
            shutil.copy(factory_location, working_folder)
            shutil.copy(tools_location, working_folder)
            shutil.copy(entrypoint_location, working_folder)

            # 5. Generate the zip
            zip_path = working_folder + ".zip"
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for root, dirs, files in os.walk(working_folder):
                    for file in files:
                        zipf.write(
                            os.path.join(root, file),
                            os.path.relpath(os.path.join(root, file), working_folder),
                        )

            # 6. Return the zip
            zip_file = open(zip_path, "rb")
            mime_type, _ = mimetypes.guess_type(zip_path)
            response = HttpResponse(zip_file, content_type=mime_type)
            response["Content-Disposition"] = (
                f"attachment; filename={os.path.basename(zip_path)}"
            )

            return response
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=400)
    else:
        return Response({"error": "app_name parameter is missing"}, status=500)


@api_view(["POST"])
def get_universe_zip(request):

    # Check if 'name' and 'zipfile' are in the request data
    if "app_name" not in request.data or "universe_name" not in request.data:
        return Response(
            {"error": "Incorrect request parameters"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Get the request parameters
    app_name = request.data.get("app_name")
    universe_name = request.data.get("universe_name")

    # Make folder path relative to Django app
    base_path = os.path.join(settings.BASE_DIR, "filesystem")
    project_path = os.path.join(base_path, app_name)
    universes_path = os.path.join(project_path, "universes")
    universe_path = os.path.join(universes_path, universe_name)

    working_folder = "/tmp/wf"

    try:
        # 1. Create the working folder
        if os.path.exists(working_folder):
            shutil.rmtree(working_folder)
        os.mkdir(working_folder)

        # 2. Copy necessary files
        shutil.copytree(universe_path, working_folder, dirs_exist_ok=True)

        # 3. Generate the zip
        zip_path = working_folder + ".zip"
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for root, dirs, files in os.walk(working_folder):
                for file in files:
                    zipf.write(
                        os.path.join(root, file),
                        os.path.relpath(os.path.join(root, file), working_folder),
                    )

        # 4. Return the zip
        zip_file = open(zip_path, "rb")
        mime_type, _ = mimetypes.guess_type(zip_path)
        response = HttpResponse(zip_file, content_type=mime_type)
        response["Content-Disposition"] = (
            f"attachment; filename={os.path.basename(zip_path)}"
        )

        return response
    except Exception as e:
        return Response(
            {"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def upload_universe(request):

    # Check if 'name' and 'zipfile' are in the request data
    if (
        "universe_name" not in request.data
        or "app_name" not in request.data
        or "zip_file" not in request.data
    ):
        return Response(
            {"error": "Name and zip file are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Get the name and the zip file from the request
    universe_name = request.data["universe_name"]
    app_name = request.data["app_name"]
    zip_file = request.data["zip_file"]

    # Make folder path relative to Django app
    base_path = os.path.join(settings.BASE_DIR, "filesystem")
    project_path = os.path.join(base_path, app_name)
    universes_path = os.path.join(project_path, "universes")
    universe_path = os.path.join(universes_path, universe_name)

    # Create the folder if it doesn't exist
    if not os.path.exists(universe_path):
        os.makedirs(universe_path)

    try:
        zip_file_data = base64.b64decode(zip_file)
    except (TypeError, ValueError):
        return Response(
            {"error": "Invalid zip file data."}, status=status.HTTP_400_BAD_REQUEST
        )

    # Save the zip file temporarily
    temp_zip_path = os.path.join(universe_path, "temp.zip")
    with open(temp_zip_path, "wb") as temp_zip_file:
        temp_zip_file.write(zip_file_data)

    # Unzip the file
    try:
        with zipfile.ZipFile(temp_zip_path, "r") as zip_ref:
            zip_ref.extractall(universe_path)
    except zipfile.BadZipFile:
        return Response(
            {"error": "Invalid zip file."}, status=status.HTTP_400_BAD_REQUEST
        )
    finally:
        # Clean up the temporary zip file
        if os.path.exists(temp_zip_path):
            os.remove(temp_zip_path)

    # Fill the config dictionary of the universe
    ram_launch_path = "/workspace/worlds/" + universe_name + "/universe.launch.py"
    universe_config = {
        "name": universe_name,
        "type": "custom",
        "ram_config": {
            "ros_version": "ROS2",
            "world": "gazebo",
            "launch_file_path": ram_launch_path,
        },
    }

    # Generate the json config
    config_path = os.path.join(universe_path, "config.json")
    with open(config_path, "w") as config_file:
        json.dump(universe_config, config_file, ensure_ascii=False, indent=4)

    return Response(
        {"success": True, "message": "Universe uploaded successfully"},
        status=status.HTTP_200_OK,
    )
