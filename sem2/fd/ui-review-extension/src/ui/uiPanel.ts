import * as vscode from "vscode";
import { Issue } from "../models/Issue";
import { ScoreEngine } from "../scoring/ScoreEngine";
import * as path from "path";

export class UiPanel implements vscode.WebviewViewProvider {
  public static readonly viewType = "uiReviewPanel";

  private view?: vscode.WebviewView;
  private currentIssues: Issue[] = [];

  constructor(private readonly extensionUri: vscode.Uri) {}

  resolveWebviewView(
    webviewView: vscode.WebviewView,
    _context: vscode.WebviewViewResolveContext,
    _token: vscode.CancellationToken,
  ) {
    this.view = webviewView;

    webviewView.webview.options = {
      enableScripts: true,

      localResourceRoots: [
        vscode.Uri.joinPath(this.extensionUri, "src", "resources"),
      ],
    };

    this.render();
  }

  private getIconUri(): vscode.Uri {
    if (!this.view) {
      throw new Error("Webview not initialized");
    }

    return this.view.webview.asWebviewUri(
      vscode.Uri.joinPath(this.extensionUri, "src", "resources", "icon.png"),
    );
  }

  public update(data: Issue[]) {
    this.currentIssues = data;
    this.render();
  }

  private render() {
    if (!this.view) {return;}

    const issues = this.currentIssues;
    const scores = ScoreEngine.calculateScores(issues);

    const icon = this.getIconUri();

    const groupedIssues: Record<string, Issue[]> = {};

    issues.forEach((issue) => {
      const fileName = path.basename(issue.file);

      if (!groupedIssues[fileName]) {
        groupedIssues[fileName] = [];
      }

      groupedIssues[fileName].push(issue);
    });

    this.view.webview.html = `
<!DOCTYPE html>
<html>

<head>

<style>

body{
font-family:var(--vscode-font-family);
padding:12px;
color:var(--vscode-foreground);
}

.header{
display:flex;
align-items:center;
gap:12px;
margin-bottom:20px;
}

.logo{
width:52px;
height:52px;
object-fit:contain;
}

.subtitle{
opacity:.7;
font-size:12px;
}

.metrics{
display:grid;
grid-template-columns:1fr 1fr;
gap:10px;
margin-bottom:20px;
}

.metric-card{
background:var(--vscode-editor-background);
padding:10px;
border-radius:8px;
border:1px solid var(--vscode-widget-border);
text-align:center;
}

.metric-value{
font-size:22px;
font-weight:bold;
}

.issue-file{
margin-top:14px;
font-weight:bold;
}

ul{
list-style:none;
padding:0;
}

li{
padding:8px;
margin-bottom:6px;
border-radius:6px;
background:var(--vscode-textCodeBlock-background);
}

.high{
border-left:4px solid var(--vscode-charts-red);
}

.medium{
border-left:4px solid var(--vscode-charts-yellow);
}

.low{
border-left:4px solid var(--vscode-charts-blue);
}

.badge{
padding:2px 6px;
border-radius:4px;
font-size:10px;
background:var(--vscode-badge-background);
}

</style>

</head>

<body>

<div class="header">

<img
class="logo"
src="${icon}"
/>

<div>

<h2 style="margin:0;">
UI Review
</h2>

<div class="subtitle">
Frontend Quality Analyzer
</div>

</div>

</div>

<div class="metrics">

<div class="metric-card">
<div class="metric-value">${scores.overall}</div>
Overall
</div>

<div class="metric-card">
<div class="metric-value">${scores.accessibility}</div>
Accessibility
</div>

<div class="metric-card">
<div class="metric-value">${scores.design}</div>
Design
</div>

<div class="metric-card">
<div class="metric-value">${scores.complexity}</div>
Complexity
</div>

</div>

<h3>
Found ${issues.length} Issues
</h3>

${Object.entries(groupedIssues)
  .map(
    ([file, fileIssues]) => `
<div class="issue-file">
${file}
</div>

<ul>

${fileIssues
  .map(
    (i) => `
<li class="${i.severity}">
<span class="badge">
${i.category}
</span>

<strong>
Line ${i.line}
</strong>

${i.message}
</li>
`,
  )
  .join("")}

</ul>
`,
  )
  .join("")}

</body>

</html>
`;
  }
}
