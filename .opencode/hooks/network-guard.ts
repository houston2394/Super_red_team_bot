export default async function networkGuard({ tool }) {
  if (tool === "http.request") {
    throw new Error("Network calls blocked by security policy.");
  }
}
