import { Rule } from "./Rule";
import { Issue } from "../../models/Issue";

export class NoInlineStylesRule implements Rule {
  name = "No Inline Styles";

  analyze(fileContent: string, filePath: string): Issue[] {
    const issues: Issue[] = [];
    const lines = fileContent.split("\n");

    lines.forEach((line, i) => {
      if (line.includes("style={{") || line.includes('style="')) {
        issues.push({
          file: filePath,
          severity: "medium",
          message:
            "Inline styles detected. Consider using CSS classes instead.",
          line: i + 1,
          category: "design",
        });
      }
    });
    return issues;
  }
}
