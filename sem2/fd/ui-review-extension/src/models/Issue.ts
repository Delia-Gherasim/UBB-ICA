export interface Issue {
  file: string;
  severity: "low" | "medium" | "high";
  message: string;
  line: number;
  category: "accessibility" | "design" | "responsive" | "complexity";
}
