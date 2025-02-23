import { expect, test } from "@jest/globals";
import { ChromaClient } from "../src/ChromaClient";
import { ChromaConnectionError } from "../src/Errors";

test("it fails with a nice error when offline", async () => {
  const chroma = new ChromaClient({ path: "http://example.invalid" });
  try {
    await chroma.createCollection({ name: "test" });
    throw new Error("Should have thrown an error.");
  } catch (e) {
    expect(e).toBeInstanceOf(ChromaConnectionError);
    expect((e as Error).message).toMatchInlineSnapshot(
      `"Failed to connect to chromadb_deterministic. Make sure your server is running and try again. If you are running from a browser, make schromadb_deterministic your chromadb_deterministic instance is configured to allow requests from the current origin using the CHROMA_SERVER_CORS_ALLOW_ORIGINS environment variable."`,
    );
  }
});
