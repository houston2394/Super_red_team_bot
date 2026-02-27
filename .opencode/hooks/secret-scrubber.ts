export default async function secretScrubber({ args }) {
  if (typeof args === "string") {
    return args.replace(/(api_key|token|secret)=\w+/gi, "$1=REDACTED");
  }
}
