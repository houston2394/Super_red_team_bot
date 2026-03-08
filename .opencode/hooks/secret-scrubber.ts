export default async function secretScrubber({ args }: { args: any }) {
  /**
   * Recursively scrub secrets from strings, objects, and arrays
   */
  
  function scrubValue(value: any): any {
    if (typeof value === 'string') {
      // Scrub common secret patterns
      return value
        .replace(/(api[_-]?key|apikey)[\s=:]+[^\s&]+/gi, '$1=REDACTED')
        .replace(/(token|bearer)[\s=:]+[^\s&]+/gi, '$1=REDACTED')
        .replace(/(secret|password|passwd|pwd)[\s=:]+[^\s&]+/gi, '$1=REDACTED')
        .replace(/(authorization:\s*bearer\s+)[^\s&]+/gi, '$1REDACTED')
        // Pattern for key=value in URLs or JSON
        .replace(/([?&](api_key|token|secret|password|key)=)[^&\s]+/gi, '$1REDACTED');
    } else if (Array.isArray(value)) {
      return value.map(item => scrubValue(item));
    } else if (value !== null && typeof value === 'object') {
      const scrubbed: any = {};
      for (const key in value) {
        if (Object.prototype.hasOwnProperty.call(value, key)) {
          // Redact sensitive keys entirely
          if (/(api[_-]?key|token|secret|password|passwd|pwd|bearer|authorization)/i.test(key)) {
            scrubbed[key] = 'REDACTED';
          } else {
            scrubbed[key] = scrubValue(value[key]);
          }
        }
      }
      return scrubbed;
    }
    
    return value;
  }
  
  return scrubValue(args);
}
