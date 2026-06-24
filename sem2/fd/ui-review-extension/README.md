# UI/UX Review Extension for Visual Studio Code

## Project Overview

**UI Review Extension** is a Visual Studio Code extension developed to analyze frontend projects and provide automated UI/UX quality feedback directly inside the editor.

The extension scans source files and applies rule-based static analysis to detect common design, accessibility, responsiveness, and maintainability problems.

The goal is to help developers improve frontend quality early in development by identifying issues before manual testing.

This project was developed as a **framework extension project** using the **Visual Studio Code Extension API**.

# Objectives

The project aims to:

- Extend Visual Studio Code with custom functionality
- Perform static UI/UX analysis
- Detect frontend anti-patterns
- Improve accessibility compliance
- Encourage responsive design
- Generate design quality metrics
- Present results inside a dashboard

# Technologies Used

## Languages

- TypeScript
- HTML
- CSS

## Frameworks / APIs

- Visual Studio Code Extension API
- Node.js
- Webview API

## Development Tools

- Visual Studio Code
- npm
- TypeScript Compiler
- ESBuild

# Functional Requirements

1. Scan frontend project files
2. Analyze source code
3. Detect UI/UX issues
4. Generate quality scores
5. Display a dashboard
6. Present diagnostics and recommendations

# Supported File Types

- `.html`
- `.css`
- `.js`
- `.jsx`
- `.ts`
- `.tsx`

# System Architecture

```
Frontend Workspace
        ↓
Workspace Scanner
        ↓
Analysis Engine
        ↓
Rule System
        ↓
Issue Collection
        ↓
Score Engine
        ↓
Dashboard UI
```

# Component Architecture

## 1. WorkspaceScanner

### Responsibility

Searches project files and collects frontend resources.

### Input

Workspace directory

### Output

List of source files

Methods:

```
getFrontendFiles()
```

## 2. AnalysisEngine

### Responsibility

Executes analysis rules.

### Input

- File content
- File path

### Output

- Issue collection

Methods:

```
run()
```

## 3. Rule Engine

### Responsibility

Executes UI/UX validation rules.

Implemented interface:

```
Rule
```

Methods:

```
analyze()
```

## 4. ScoreEngine

### Responsibility

Calculates project quality metrics.

Generated scores:

- Overall Score
- Accessibility Score
- Design Score
- Complexity Score

## 5. UiPanel

### Responsibility

Displays analysis results.

Displayed information:

- Metrics
- Issues
- Categories
- Severity

# Implemented Rules

## Accessibility Rules

### Missing Alt Text

Detects:

```html
<img src="photo.jpg" />
```

### Small Touch Targets

Detects:

```css
height: 20px;
```

## Design Rules

### Hardcoded Colors

Detects:

```css
color: #ff0000;
```

### Tiny Font Sizes

Detects:

```css
font-size: 10px;
```

### Inconsistent Spacing

Detects irregular spacing values.

## Responsive Rules

### Fixed Width Detection

Detects:

```css
width: 1200px;
```

## Complexity Rules

### Deep Nesting Detection

Detects excessive nesting.

## Inline Style Rules

Detects:

```jsx
style={{}}
```

# Scoring Algorithm

Issue severity impacts score.

| Severity | Penalty |
| -------- | ------- |
| High     | −5      |
| Medium   | −2      |
| Low      | −1      |

Final scores:

```
Overall Score
Accessibility Score
Design Score
Complexity Score
```

Range:

```
0–100
```

# User Workflow

## Run Analysis

Open:

```
Ctrl + Shift + P
```

Execute:

```
UI Review: Analyze
```

## Dashboard Output

Displayed information:

- Overall score
- Accessibility score
- Design score
- Simplicity score
- Detected issues

# Project Structure

```
src/

analysis/
 ├── rules/
 ├── analysisEngine.ts

models/
 └── Issue.ts

scanner/
 └── workspaceScanner.ts

scoring/
 └── ScoreEngine.ts

ui/
 └── uiPanel.ts

extension.ts
```

# Installation

Clone repository:

```bash
git clone <repository-url>
```

Install dependencies:

```bash
npm install
```

Compile:

```bash
npm run compile
```

Run:

```
F5
```

# Testing

Test procedure:

1. Open Extension Development Host
2. Open a frontend project
3. Execute analysis
4. Validate results

# Limitations

Current limitations:

- Rule-based analysis only
- No automatic fixes
- No runtime UI testing
- Limited semantic understanding

# Future Improvements

Planned features:

- VS Code Diagnostics integration
- Squiggly warnings
- Hover explanations
- Auto-fix suggestions
- Export reports (PDF/JSON)

# Conclusion

UI Review Extension demonstrates how a development framework can be extended through modular architecture to provide automated UI/UX quality analysis directly inside Visual Studio Code.

The project combines static analysis, accessibility validation, scoring mechanisms, and visual reporting to improve frontend development workflows.
