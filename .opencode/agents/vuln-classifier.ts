export default {
  name: "vuln-classifier",
  description: "Classify endpoint clusters into likely vulnerability classes (OWASP Top 10 and beyond).",
  
  run: async ({ context, input }) => {
    // Input validation
    if (!input) {
      throw new Error("vuln-classifier requires input data");
    }
    
    // Safely stringify input with size limit
    let inputStr: string;
    try {
      inputStr = typeof input === 'string' 
        ? input 
        : JSON.stringify(input);
      
      // Truncate to prevent token overflow
      if (inputStr.length > 20000) {
        inputStr = inputStr.slice(0, 20000) + '... (truncated)';
      }
    } catch (e) {
      throw new Error(`Failed to process input: ${e instanceof Error ? e.message : 'unknown error'}`);
    }
    
    try {
      return await context.llm.generate({
        prompt: `
You are a security vulnerability classifier. Analyze the following endpoint clusters and classify them into likely vulnerability categories.

Consider these vulnerability classes:
- IDOR (Insecure Direct Object Reference)
- SSRF (Server-Side Request Forgery)
- XSS (Cross-Site Scripting)
- SQLi (SQL Injection)
- Authentication/Authorization bypass
- Unsafe deserialization
- File upload vulnerabilities
- Command injection
- Path traversal
- CSRF (Cross-Site Request Forgery)

For each cluster, provide:
1. Primary vulnerability class
2. Confidence level (high/medium/low)
3. Reasoning
4. Suggested test cases

Input clusters:
${inputStr}
`
      });
    } catch (e) {
      throw new Error(`LLM generation failed: ${e instanceof Error ? e.message : 'unknown error'}`);
    }
  }
};
