import { Issue } from "../../models/Issue";

export interface Rule {
  name: string;
  analyze(fileContent: string, filePath: string): Issue[];
}
