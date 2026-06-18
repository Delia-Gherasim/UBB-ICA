import { Issue } from "../models/Issue";

export class ScoreEngine {
  static calculateScores(issues: Issue[]) {
    let overallScore = 100;
    let accessibilityScore = 100;
    let complexityScore = 100;
    let designScore = 100;

    issues.forEach((issue) => {
      const deduction =
        issue.severity === "high" ? 5 : issue.severity === "medium" ? 2 : 1;
      overallScore -= deduction;

      switch (issue.category) {
        case "accessibility":
          accessibilityScore -= deduction * 2;
          break;
        case "complexity":
          complexityScore -= deduction * 2;
          break;
        case "design":
        case "responsive":
          designScore -= deduction * 1.5;
          break;
      }
    });

    return {
      overall: Math.max(0, Math.round(overallScore)),
      accessibility: Math.max(0, Math.round(accessibilityScore)),
      complexity: Math.max(0, Math.round(complexityScore)),
      design: Math.max(0, Math.round(designScore)),
    };
  }
}
