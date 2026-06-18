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

  const panelProvider = new UiPanel();

  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider("uiReviewPanel", panelProvider),
  );

  const command = vscode.commands.registerCommand(
    "ui-review.analyze",
    async () => {
      const files = await scanner.getFrontendFiles();
      let allIssues: any[] = [];

      for (const file of files) {
        const content = await vscode.workspace.fs.readFile(file);
        const text = Buffer.from(content).toString("utf8");

        const issues = engine.run(text, file.fsPath);
        allIssues.push(...issues);
      }

      await vscode.commands.executeCommand("uiReviewPanel.focus");
      panelProvider.update(allIssues);

      vscode.window.showInformationMessage(
        `UI/UX Scan complete: Found ${allIssues.length} issues`,
      );
    },
  );

  context.subscriptions.push(command);
}

export function deactivate() {}
