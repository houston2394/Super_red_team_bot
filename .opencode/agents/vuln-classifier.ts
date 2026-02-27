export default {
  name: "vuln-classifier",
  description: "Classify endpoint clusters into likely vulnerability classes.",
  run: async ({ context, input }) => {
    return context.llm.generate({
      prompt: `
For each cluster, infer likely vulnerability classes:
IDOR, SSRF, XSS, SQLi, Auth bypass, Unsafe deserialization, File upload issues.

Clusters: ${JSON.stringify(input).slice(0, 20000)}
`
    });
  }
};