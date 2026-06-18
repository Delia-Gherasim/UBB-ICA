import * as vscode from "vscode";
import { Issue } from "../models/Issue";
import { ScoreEngine } from "../scoring/ScoreEngine";
import * as path from "path";

export class UiPanel implements vscode.WebviewViewProvider {
  public static readonly viewType = "uiReviewPanel";

  private view?: vscode.WebviewView;
  private currentIssues: Issue[] = [];

  resolveWebviewView(webviewView: vscode.WebviewView) {
    this.view = webviewView;
    webviewView.webview.options = { enableScripts: true };
    this.render();
  }

  public update(data: Issue[]) {
    this.currentIssues = data;
    this.render();
  }

  private render() {
    if (!this.view) return;

    const issues = this.currentIssues;
    const scores = ScoreEngine.calculateScores(issues);

    const groupedIssues: Record<string, Issue[]> = {};
    issues.forEach((issue) => {
      const fileName = path.basename(issue.file);
      if (!groupedIssues[fileName]) groupedIssues[fileName] = [];
      groupedIssues[fileName].push(issue);
    });

    this.view.webview.html = `
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <style>
          body { font-family: var(--vscode-font-family); padding: 10px; color: var(--vscode-foreground); }
          h2 { border-bottom: 1px solid var(--vscode-panel-border); padding-bottom: 5px; }
          .metrics { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px; }
          .metric-card { background: var(--vscode-editor-background); padding: 10px; border-radius: 6px; text-align: center; border: 1px solid var(--vscode-widget-border); }
          .metric-value { font-size: 24px; font-weight: bold; }
          .high { color: var(--vscode-charts-red); }
          .medium { color: var(--vscode-charts-yellow); }
          .low { color: var(--vscode-charts-blue); }
          .issue-group { margin-top: 15px; }
          .issue-file { font-weight: bold; margin-bottom: 5px; color: var(--vscode-textLink-foreground); }
          ul { list-style: none; padding: 0; margin: 0; }
          li { background: var(--vscode-textCodeBlock-background); margin-bottom: 5px; padding: 8px; border-left: 3px solid transparent; border-radius: 4px; }
          li.high { border-left-color: var(--vscode-charts-red); }
          li.medium { border-left-color: var(--vscode-charts-yellow); }
          li.low { border-left-color: var(--vscode-charts-blue); }
          .badge { display: inline-block; padding: 2px 6px; border-radius: 3px; font-size: 10px; text-transform: uppercase; font-weight: bold; background: var(--vscode-badge-background); color: var(--vscode-badge-foreground); margin-right: 5px;}
        </style>
      </head>
      <body>
        <h2>UI/UX Dashboard</h2>
        
        <div class="metrics">
          <div class="metric-card"><div class="metric-value">${scores.overall}</div><div>Overall Score</div></div>
          <div class="metric-card"><div class="metric-value">${scores.accessibility}</div><div>A11y Score</div></div>
          <div class="metric-card"><div class="metric-value">${scores.design}</div><div>Design Match</div></div>
          <div class="metric-card"><div class="metric-value">${scores.complexity}</div><div>Simplicity</div></div>
        </div>

        <h3>Found ${issues.length} Issues</h3>

        <div class="issues-list">
          ${Object.entries(groupedIssues)
            .map(
              ([fileName, fileIssues]) => `
            <div class="issue-group">
              <div class="issue-file">${fileName}</div>
              <ul>
                ${fileIssues
                  .map(
                    (i) => `
                  <li class="${i.severity}">
                    <span class="badge">${i.category}</span>
                    <strong class="${i.severity}">[Line ${i.line}]</strong> ${i.message}
                  </li>
                `,
                  )
                  .join("")}
              </ul>
            </div>
          `,
            )
            .join("")}
        </div>
      </body>
      </html>
    `;
  }
}
