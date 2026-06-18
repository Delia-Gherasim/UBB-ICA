import { Rule } from "./rules/Rule";
import { Issue } from "../models/Issue";

export class AnalysisEngine {
  constructor(private rules: Rule[]) {}

  run(fileContent: string, filePath: string): Issue[] {
    let issues: Issue[] = [];

    for (const rule of this.rules) {
      issues = issues.concat(rule.analyze(fileContent, filePath));
    }

    return issues;
  }
}
