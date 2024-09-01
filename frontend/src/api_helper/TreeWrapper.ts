import axios from "axios";

// Project management

const createProject = async (projectName: string) => {
  if (!projectName.trim()) {
    throw new Error("Project name cannot be empty.");
  }

  const apiUrl = `/tree_api/create_project?project_name=${encodeURIComponent(projectName)}`;

  try {
    const response = await axios.get(apiUrl);

    // Handle unsuccessful response status (e.g., non-2xx status)
    if (!response.data.success) {
      throw new Error(response.data.message || "Failed to create project."); // Response error
    }
  } catch (error: unknown) {
    throw error; // Rethrow
  }
};

const saveProject = async (modelJson: string, currentProjectname: string) => {
  if (!modelJson) throw new Error("Tree JSON is empty!");
  if (!currentProjectname) throw new Error("Current Project name is not set");

  const apiUrl = "/tree_api/save_project/";
  try {
    const response = await axios.post(apiUrl, {
      project_name: currentProjectname,
      graph_json: modelJson,
    });

    // Handle unsuccessful response status (e.g., non-2xx status)
    if (!response.data.success) {
      throw new Error(response.data.message || "Failed to create project."); // Response error
    }
  } catch (error: unknown) {
    throw error; // Rethrow
  }
};

// Universe management

const getUniverseConfig = async (
  universeName: string,
  currentProjectname: string
) => {
  if (!universeName) throw new Error("The universe name is not set");
  if (!currentProjectname) throw new Error("Current Project name is not set");

  const apiUrl = `/tree_api/get_universe_configuration?project_name=${encodeURIComponent(
    currentProjectname
  )}&universe_name=${encodeURIComponent(universeName)}`;
  try {
    const response = await axios.get(apiUrl);

    // Handle unsuccessful response status (e.g., non-2xx status)
    if (!response.data.success) {
      throw new Error(
        response.data.message || "Failed to retrieve universe config"
      ); // Response error
    }

    return JSON.stringify(response.data.config);
  } catch (error: unknown) {
    throw error; // Rethrow
  }
};

const getCustomUniverseZip = async (
  universeName: string,
  currentProjectname: string
) => {
  if (!universeName) throw new Error("The universe name is not set");
  if (!currentProjectname) throw new Error("Current Project name is not set");

  const apiUrl = "/tree_api/get_universe_zip/";
  try {
    // Configure the request options
    const config = {
      method: "POST",
      url: apiUrl,
      headers: {
        "Content-Type": "application/json",
      },
      data: JSON.stringify({
        app_name: currentProjectname,
        universe_name: universeName,
      }),
    };

    // Make the request
    const response = await axios(config);

    // Handle unsuccessful response status (e.g., non-2xx status)
    if (!response.data.success) {
      throw new Error(
        response.data.message || "Failed to retrieve custom universe"
      ); // Response error
    }
    return new Blob([response.data], { type: "application/octet-stream" });
  } catch (error: unknown) {
    throw error; // Rethrow
  }
};

// App management

const generateApp = async (
  modelJson: string,
  currentProjectname: string,
  btOrder: string
) => {
  if (!modelJson) throw new Error("Tree JSON is empty!");
  if (!currentProjectname) throw new Error("Current Project name is not set");

  const apiUrl = "/tree_api/generate_app/";
  try {
    // Configure the request options
    const config = {
      method: "POST",
      url: apiUrl,
      headers: {
        "Content-Type": "application/json",
      },
      data: JSON.stringify({
        app_name: currentProjectname,
        tree_graph: modelJson,
        bt_order: btOrder,
      }),
    };

    // Make the request
    const response = await axios(config);

    // Handle unsuccessful response status (e.g., non-2xx status)
    if (!response.data.success) {
      throw new Error(response.data.message || "Failed to create app."); // Response error
    }
    return new Blob([response.data], { type: "application/octet-stream" });
  } catch (error: unknown) {
    throw error; // Rethrow
  }
};

// Named export
export {
  createProject,
  saveProject,
  generateApp,
  getUniverseConfig,
  getCustomUniverseZip,
};
