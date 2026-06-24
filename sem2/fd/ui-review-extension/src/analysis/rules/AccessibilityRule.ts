import { Rule } from "./Rule";
import { Issue } from "../../models/Issue";

export class AccessibilityRule implements Rule {
  name = "Accessibility Checks";

  analyze(fileContent: string, filePath: string): Issue[] {
    const issues: Issue[] = [];
    const lines = fileContent.split("\n");

    lines.forEach((line, i) => {
      if (
        /<img(?![^>]*\balt\s*=)[^>]*>/i.test(line) ||
        /alt=(['""])\1/i.test(line)
      ) {
        issues.push({
          file: filePath,
          severity: "high",
          message: "Image missing alt text.",
          line: i + 1,
          category: "accessibility",
        });
      }

      if (
        /(height:\s*[1-3]?[0-9]px)|(w-[1-4]\b)|(h-[1-4]\b)/i.test(line) &&
        (line.includes("<button") || line.includes("<a "))
      ) {
        issues.push({
          file: filePath,
          severity: "medium",
          message: "Touch target might be too small.",
          line: i + 1,
          category: "accessibility",
        });
      }
    });
    return issues;
  }
}
