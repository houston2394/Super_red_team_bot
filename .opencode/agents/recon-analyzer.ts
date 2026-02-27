export default {
  name: "recon-analyzer",
  description: "Analyze recon artifacts and cluster endpoints.",
  run: async ({ tools, context }) => {
    const endpoints = await tools.filesystem.readJson("./recon/endpoints.json");

    return context.llm.generate({
      prompt: `
Cluster endpoints by:
- authentication level
- data sensitivity
- HTTP method
- parameter type

Use context-compression and filesystem-context patterns.
Endpoints: ${JSON.stringify(endpoints).slice(0, 20000)}
`
    });
  }
};