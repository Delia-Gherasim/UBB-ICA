import { Rule } from "./Rule";
import { Issue } from "../../models/Issue";

export class ResponsiveRule implements Rule {
  name = "Responsive Design checks";

  analyze(fileContent: string, filePath: string): Issue[] {
    const issues: Issue[] = [];
    const lines = fileContent.split("\n");

    lines.forEach((line, i) => {
      if (/width:\s*[1-9][0-9]{2,}px/i.test(line)) {
        issues.push({
          file: filePath,
          severity: "medium",
          message: "Fixed large width detected.",
          line: i + 1,
          category: "responsive",
        });
      }
    });
    return issues;
  }
}
