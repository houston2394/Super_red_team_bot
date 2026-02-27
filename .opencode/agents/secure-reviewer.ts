export default {
  name: "secure-reviewer",
  description: "Perform secure coding review using OWASP and language-specific rules.",
  run: async ({ context, tools }) => {
    const tree = await tools.filesystem.readTree(".");
    return context.llm.generate({
      prompt: `
Perform secure coding review:
- OWASP ASVS
- Input validation
- Secrets handling
- Dependency risks
- Unsafe patterns

Project tree: ${JSON.stringify(tree).slice(0, 20000)}
`
    });
  }
};