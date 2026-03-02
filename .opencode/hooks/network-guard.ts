export default async function networkGuard({ tool, args }: { tool: string; args?: any }) {
  /**
   * Guard against unauthorized network operations
   * Blocks network calls in sensitive contexts
   */
  
  const blockedTools = [
    'http.request',
    'http.get',
    'http.post',
    'fetch',
    'axios',
    'network.request'
  ];
  
  const blockedDomains = [
    'production.internal',
    'admin.internal',
    'sensitive.internal'
  ];
  
  // Check if tool is blocked
  if (blockedTools.includes(tool)) {
    throw new Error(`Network tool '${tool}' blocked by security policy. Use approved methods only.`);
  }
  
  // Check for suspicious patterns in args
  if (args) {
    const argsStr = typeof args === 'string' ? args : JSON.stringify(args);
    
    for (const domain of blockedDomains) {
      if (argsStr.includes(domain)) {
        throw new Error(`Network request to blocked domain '${domain}' prevented by security policy.`);
      }
    }
  }
}
