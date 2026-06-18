import * as vscode from "vscode";

export class WorkspaceScanner {
  async getFrontendFiles(): Promise<vscode.Uri[]> {
    return vscode.workspace.findFiles(
      "**/*.{js,jsx,ts,tsx,html,css}",
      "**/node_modules/**",
    );
  }
}
