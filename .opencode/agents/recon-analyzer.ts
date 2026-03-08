export default {
  name: "recon-analyzer",
  description: "Analyze reconnaissance data to identify attack surface, interesting endpoints, and security-relevant patterns.",
  
  run: async ({ context, input }) => {
    if (!input) {
      throw new Error("recon-analyzer requires input data (recon results)");
    }
    
    let inputStr: string;
    try {
      inputStr = typeof input === 'string' 
        ? input 
        : JSON.stringify(input);
      
      if (inputStr.length > 25000) {
        inputStr = inputStr.slice(0, 25000) + '... (truncated)';
      }
    } catch (e) {
      throw new Error(`Failed to process input: ${e instanceof Error ? e.message : 'unknown error'}`);
    }
    
    try {
      return await context.llm.generate({
        prompt: `
You are a reconnaissance data analyst. Analyze the following recon data and identify:

1. Attack Surface Analysis
   - Exposed endpoints and their purposes
   - Authentication requirements
   - Parameter patterns

2. Interesting Endpoints
   - Administrative interfaces
   - Debug/test endpoints
   - API endpoints with sensitive operations
   - File upload/download endpoints

3. Security-Relevant Patterns
   - Inconsistent authentication
   - Verbose error messages
   - Version disclosure
   - Technology stack fingerprinting

4. Prioritized Target List
   - High-value targets
   - Low-hanging fruit
   - Recommended testing order

Recon data:
${inputStr}
`
      });
    } catch (e) {
      throw new Error(`LLM generation failed: ${e instanceof Error ? e.message : 'unknown error'}`);
    }
  }
};
