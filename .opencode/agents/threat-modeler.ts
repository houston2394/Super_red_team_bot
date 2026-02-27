export default {
  name: "threat-modeler",
  description: "Enumerate STRIDE threats for the project.",
  run: async ({ context, tools }) => {
    const tree = await tools.filesystem.readTree(".");
    return context.llm.generate({
      prompt: `
Perform STRIDE threat modeling:
Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation of Privilege.

Project tree: ${JSON.stringify(tree).slice(0, 20000)}
`
    });
  }
};