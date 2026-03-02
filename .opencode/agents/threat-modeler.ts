export default {
  name: "threat-modeler",
  description: "Enumerate STRIDE threats (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) for the project.",
  
  run: async ({ context, tools }) => {
    let projectTree: any;
    
    try {
      projectTree = await tools.filesystem.readTree(".");
    } catch (e) {
      throw new Error(`Failed to read project tree: ${e instanceof Error ? e.message : 'unknown error'}`);
    }
    
    let treeStr: string;
    try {
      treeStr = JSON.stringify(projectTree);
      if (treeStr.length > 20000) {
        treeStr = treeStr.slice(0, 20000) + '... (truncated)';
      }
    } catch (e) {
      throw new Error(`Failed to process project tree: ${e instanceof Error ? e.message : 'unknown error'}`);
    }
    
    try {
      return await context.llm.generate({
        prompt: `
You are a threat modeling expert. Perform a STRIDE threat analysis on this project.

STRIDE Categories:

1. Spoofing Identity
   - Authentication bypass
   - Identity theft
   - Credential theft

2. Tampering with Data
   - Data modification in transit
   - Data modification at rest
   - Input manipulation

3. Repudiation
   - Lack of audit logs
   - Log tampering
   - Non-repudiable actions

4. Information Disclosure
   - Data leaks
   - Sensitive information exposure
   - Privacy violations

5. Denial of Service
   - Resource exhaustion
   - Service disruption
   - Rate limiting bypass

6. Elevation of Privilege
   - Privilege escalation
   - Access control bypass
   - Administrative access abuse

For each identified threat:
- Category
- Description
- Impact (Critical/High/Medium/Low)
- Likelihood (High/Medium/Low)
- Mitigation recommendations

Project structure:
${treeStr}
`
      });
    } catch (e) {
      throw new Error(`LLM generation failed: ${e instanceof Error ? e.message : 'unknown error'}`);
    }
  }
};
