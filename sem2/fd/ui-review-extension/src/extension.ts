import * as vscode from "vscode";
import { WorkspaceScanner } from "./scanner/workspaceScanner";
import { AnalysisEngine } from "./analysis/analysisEngine";
import { UiPanel } from "./ui/uiPanel";

import { NoInlineStylesRule } from "./analysis/rules/NoInlineStylesRule";
import { AccessibilityRule } from "./analysis/rules/AccessibilityRule";
import { DesignConsistencyRule } from "./analysis/rules/DesignConsistencyRule";
import { ResponsiveRule } from "./analysis/rules/ResponsiveRule";
import { ComplexityRule } from "./analysis/rules/ComplexityRule";

export function activate(context: vscode.ExtensionContext) {
  const scanner = new WorkspaceScanner();

  const engine = new AnalysisEngine([
    new NoInlineStylesRule(),
    new AccessibilityRule(),
    new DesignConsistencyRule(),
    new ResponsiveRule(),
    new ComplexityRule(),
  ]);

  const panelProvider = new UiPanel(context.extensionUri);

  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider("uiReviewPanel", panelProvider),
  );

  let isRunning = false;

  const runAnalysis = async () => {
    if (isRunning) return;
    isRunning = true;

    try {
      const files = await scanner.getFrontendFiles();
      let allIssues: any[] = [];

      for (const file of files) {
        const content = await vscode.workspace.fs.readFile(file);
        const text = Buffer.from(content).toString("utf8");

        const issues = engine.run(text, file.fsPath);
        allIssues.push(...issues);
      }

      panelProvider.update(allIssues);

      vscode.window.showInformationMessage(
        `UI/UX Scan complete: Found ${allIssues.length} issues`,
      );
    } finally {
      isRunning = false;
    }
  };

  const command = vscode.commands.registerCommand(
    "ui-review.analyze",
    runAnalysis,
  );

  context.subscriptions.push(command);

  const watcher = vscode.workspace.createFileSystemWatcher(
    "**/*.{js,jsx,ts,tsx,html,css}",
  );

  let timeout: NodeJS.Timeout | undefined;

  const triggerAnalysis = () => {
    if (timeout) clearTimeout(timeout);

    timeout = setTimeout(() => {
      vscode.commands.executeCommand("ui-review.analyze");
    }, 1000);
  };

  watcher.onDidChange(triggerAnalysis);
  watcher.onDidCreate(triggerAnalysis);
  watcher.onDidDelete(triggerAnalysis);

  context.subscriptions.push(watcher);

  setTimeout(() => {
    vscode.commands.executeCommand("ui-review.analyze");
  }, 1500);

  if (vscode.workspace.workspaceFolders) {
    vscode.commands.executeCommand("ui-review.analyze");
  }

  context.subscriptions.push(watcher);
}

export function deactivate() {}
