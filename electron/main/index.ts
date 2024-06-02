import { app, BrowserWindow, shell, ipcMain } from "electron";
import fs from "fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import os from "node:os";
import { update } from "./update";
import { spawn, exec } from "node:child_process";

globalThis.__filename = fileURLToPath(import.meta.url);
globalThis.__dirname = path.dirname(__filename);

// The built directory structure
//
// ├─┬ dist-electron
// │ ├─┬ main
// │ │ └── index.js    > Electron-Main
// │ └─┬ preload
// │   └── index.mjs   > Preload-Scripts
// ├─┬ dist
// │ └── index.html    > Electron-Renderer
//
process.env.APP_ROOT = path.join(__dirname, "../..");

export const MAIN_DIST = path.join(process.env.APP_ROOT, "dist-electron");
export const RENDERER_DIST = path.join(process.env.APP_ROOT, "dist");
export const VITE_DEV_SERVER_URL = process.env.VITE_DEV_SERVER_URL;

process.env.VITE_PUBLIC = VITE_DEV_SERVER_URL
  ? path.join(process.env.APP_ROOT, "public")
  : RENDERER_DIST;

// Disable GPU Acceleration for Windows 7
if (os.release().startsWith("6.1")) app.disableHardwareAcceleration();

// Set application name for Windows 10+ notifications
if (process.platform === "win32") app.setAppUserModelId(app.getName());

if (!app.requestSingleInstanceLock()) {
  app.quit();
  process.exit(0);
}

ipcMain.handle(
  "save-file",
  async (event, { buffer, filename, contentType }) => {
    try {
      const basePath = path.join(__dirname, "../../public/uploads");
      if (!fs.existsSync(basePath)) {
        fs.mkdirSync(basePath, { recursive: true });
      }
      const filePath = path.join(basePath, filename);

      // Write the file based on content type
      if (contentType === "application/json") {
        await fs.promises.writeFile(filePath, buffer, "utf8");
      } else {
        await fs.promises.writeFile(filePath, Buffer.from(buffer));
      }

      return { success: true, filePath };
    } catch (err) {
      console.error(`Failed to save file (ipcMain): ${err}`);
      return { success: false, message: err.message };
    }
  }
);

ipcMain.handle("upload_resume", async (event, { buffer }) => {
  try {
    // Define the base path for uploads relative to the application's root directory
    const file_uploader = path.join(
      __dirname,
      "../../public/python/ChatGPTDriver.py"
    );

    var process = spawn("python3", ["-u", file_uploader, "upload_resume"]);

    process.stdout.on("data", function (data: any) {
      console.log(data.toString());
    });

    process.stderr.on("data", function (data: any) {
      console.log(data.toString());
    });

    return { success: true };
  } catch (err) {
    console.error(`Failed to upload resume: ${err}`);
    return { success: false, message: err.message };
  }
});

ipcMain.handle("form_data_from_json", async (event, { buffer }) => {
  try {
    // Define the base path for uploads relative to the application's root directory
    const json_file = path.join(__dirname, "../../user_info_table.json");

    const data = fs.readFileSync(json_file, "utf8");

    return { success: true, data };
  } catch (err) {
    console.error(`Failed to upload resume: ${err}`);
    return { success: false, message: err.message };
  }
});

ipcMain.handle("get_previous_applications", async (event, { buffer }) => {
  try {
    // Get the path from Tahmid once he makes it
    const pathname = path.join(
      __dirname,
      "../../public/uploads/completed_apps.txt"
    );
    const data = fs.readFileSync(pathname, "utf8");

    return { success: true, data };
  } catch (err) {
    console.error(`Failed to upload resume: ${err}`);
    return { success: false, message: err.message };
  }
});

ipcMain.handle("run_linkedin", async (event, { buffer }) => {
  try {
    // Define the base path for uploads relative to the application's root directory
    const linked_in_finder = path.join(
      __dirname,
      "../../public/python/linkedin.py"
    );

    var process = spawn("python3", ["-u", linked_in_finder]);

    process.stdout.on("data", function (data: any) {
      const basePath = path.join(__dirname, "../../public/uploads");
      if (!fs.existsSync(basePath)) {
        fs.mkdirSync(basePath, { recursive: true });
      }
      const filePath = path.join(basePath, "completed_apps.txt");

      fs.promises.appendFile(filePath, data + "\n", "utf8");
    });

    process.stderr.on("data", function (data: any) {
      console.log(data.toString());
    });

    return { success: true };
  } catch (err) {
    console.error(`Failed to upload resume: ${err}`);
    return { success: false, message: err.message };
  }
});

ipcMain.handle("run_workday", async (event, { buffer }) => {
  try {
    // Define the base path for uploads relative to the application's root directory
    const linked_in_finder = path.join(
      __dirname,
      "../../public/python/workday.py"
    );

    var process = spawn("python3", ["-u", linked_in_finder]);

    process.stdout.on("data", function (data: any) {
      const basePath = path.join(__dirname, "../../public/uploads");
      if (!fs.existsSync(basePath)) {
        fs.mkdirSync(basePath, { recursive: true });
      }
      const filePath = path.join(basePath, "completed_apps.txt");

      fs.promises.appendFile(filePath, data + "\n", "utf8");
    });

    process.stderr.on("data", function (data: any) {
      console.log(data.toString());
    });

    return { success: true };
  } catch (err) {
    console.error(`Failed to upload resume: ${err}`);
    return { success: false, message: err.message };
  }
});

// Setup IPC to run Python script
ipcMain.handle("workdayscrape", async (event, args) => {
  // Specify the path to your Python script and include args if necessary
  const scriptPath = "public/python/WorkDayScrape.py"; // Change this to your actual script path
  const command = `python ${scriptPath} ${args}`;

  return new Promise((resolve, reject) => {
    resolve("ignored: demo");
    // exec(command, (error, stdout, stderr) => {
    //   if (error) {
    //     console.error(`exec error: ${error}`);
    //     return reject(stderr);
    //   }
    //   console.log(`stdout: ${stdout}`);
    //   resolve(stdout);
    // });
  });
});

ipcMain.handle("stop_process", async (event, { buffer }) => {
  var process = spawn("pkill", ["-9", "-f", buffer]);
});

let win: BrowserWindow | null = null;
const preload = path.join(__dirname, "../preload/index.mjs");
const indexHtml = path.join(RENDERER_DIST, "index.html");

async function createWindow() {
  win = new BrowserWindow({
    title: "Main window",
    icon: path.join(process.env.VITE_PUBLIC, "favicon.ico"),
    fullscreenable: false, // Disable full-screen mode
    maximizable: false, // Disable window maximizing
    resizable: false,
    webPreferences: {
      preload,
      // Warning: Enable nodeIntegration and disable contextIsolation is not secure in production
      nodeIntegration: true,

      // Consider using contextBridge.exposeInMainWorld
      // Read more on https://www.electronjs.org/docs/latest/tutorial/context-isolation
      // contextIsolation: false,
    },
  });

  if (VITE_DEV_SERVER_URL) {
    // #298
    win.loadURL(VITE_DEV_SERVER_URL);
    // Open devTool if the app is not packaged
    win.webContents.openDevTools();
  } else {
    win.loadFile(indexHtml);
  }

  // Test actively push message to the Electron-Renderer
  win.webContents.on("did-finish-load", () => {
    win?.webContents.send("main-process-message", new Date().toLocaleString());
  });

  // Make all links open with the browser, not with the application
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith("https:")) shell.openExternal(url);
    return { action: "deny" };
  });

  // Auto update
  update(win);
}

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  win = null;
  if (process.platform !== "darwin") app.quit();
});

app.on("second-instance", () => {
  if (win) {
    // Focus on the main window if the user tried to open another
    if (win.isMinimized()) win.restore();
    win.focus();
  }
});

app.on("activate", () => {
  const allWindows = BrowserWindow.getAllWindows();
  if (allWindows.length) {
    allWindows[0].focus();
  } else {
    createWindow();
  }
});

// New window example arg: new windows url
ipcMain.handle("open-win", (_, arg) => {
  const childWindow = new BrowserWindow({
    webPreferences: {
      preload,
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  if (VITE_DEV_SERVER_URL) {
    childWindow.loadURL(`${VITE_DEV_SERVER_URL}#${arg}`);
  } else {
    childWindow.loadFile(indexHtml, { hash: arg });
  }
});
