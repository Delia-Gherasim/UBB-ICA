import { Rule } from "./Rule";
import { Issue } from "../../models/Issue";

export class ComplexityRule implements Rule {
  name = "Component Complexity";

  analyze(fileContent: string, filePath: string): Issue[] {
    const issues: Issue[] = [];
    const lines = fileContent.split("\n");

    lines.forEach((line, i) => {
      if (/^(\s{12,}|\t{6,})</.test(line)) {
        issues.push({
          file: filePath,
          severity: "medium",
          message:
            "Deep HTML/JSX nesting detected. Consider breaking into sub-components.",
          line: i + 1,
          category: "complexity",
        });
      }
    });
    return issues;
  }
}
