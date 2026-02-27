export default async function writeAudit({ tool, args, context }) {
  if (tool === "filesystem.writeFile") {
    await context.tools.filesystem.appendFile(
      "./security-write-log.txt",
      `WRITE: ${args.path} at ${new Date().toISOString()}\n`
    );
  }
}
