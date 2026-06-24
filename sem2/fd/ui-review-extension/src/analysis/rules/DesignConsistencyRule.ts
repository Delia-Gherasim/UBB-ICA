import { Rule } from "./Rule";
import { Issue } from "../../models/Issue";

export class DesignConsistencyRule implements Rule {
  name = "Design Consistency";

  analyze(fileContent: string, filePath: string): Issue[] {
    const issues: Issue[] = [];
    const lines = fileContent.split("\n");

    lines.forEach((line, i) => {
      if (
        /#([0-9a-fA-F]{3}){1,2}\b|rgba?\(/i.test(line) &&
        !line.includes("var(--")
      ) {
        issues.push({
          file: filePath,
          severity: "low",
          message: "Hardcoded color detected. Use theme variables.",
          line: i + 1,
          category: "design",
        });
      }

      if (
        /font-size:\s*([1-9]|1[0-1])px/i.test(line) ||
        /text-(xs|xxs)/i.test(line)
      ) {
        issues.push({
          file: filePath,
          severity: "high",
          message: "Font size too small.",
          line: i + 1,
          category: "design",
        });
      }

      if (/(margin|padding).*\b(1[1345789]|2[1235679])px/i.test(line)) {
        issues.push({
          file: filePath,
          severity: "low",
          message: "Non-standard spacing detected.",
          line: i + 1,
          category: "design",
        });
      }
    });
    return issues;
  }
}
