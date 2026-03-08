export default {
  name: "secure-reviewer",
  description: "Perform comprehensive secure coding review using OWASP ASVS, language-specific rules, and security best practices.",
  
  run: async ({ context, tools }) => {
    let projectTree: any;
    
    try {
      projectTree = await tools.filesystem.readTree(".");
    } catch (e) {
      throw new Error(`Failed to read project tree: ${e instanceof Error ? e.message : 'unknown error'}`);
    }
    
    // Safely stringify and truncate
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
You are a security code reviewer. Perform a comprehensive secure coding review of this project.

Review criteria (OWASP ASVS compliant):

1. Input Validation
   - All user inputs sanitized
   - Whitelist validation where possible
   - Proper type checking

2. Secrets Handling
   - No hardcoded credentials
   - Secrets in environment variables
   - Proper key rotation mechanisms

3. Authentication & Authorization
   - Strong authentication mechanisms
   - Proper session management
   - Authorization checks on all protected resources

4. Cryptography
   - Modern, secure algorithms
   - Proper key management
   - No deprecated crypto

5. Dependency Management
   - Known vulnerable dependencies
   - Outdated packages
   - Supply chain risks

6. Unsafe Patterns
   - Eval/exec usage
   - Unsafe deserialization
   - Command injection risks
   - SQL injection risks
   - XSS vulnerabilities

Provide findings in order of severity (Critical, High, Medium, Low, Info).

Project structure:
${treeStr}
`
      });
    } catch (e) {
      throw new Error(`LLM generation failed: ${e instanceof Error ? e.message : 'unknown error'}`);
    }
  }
};
