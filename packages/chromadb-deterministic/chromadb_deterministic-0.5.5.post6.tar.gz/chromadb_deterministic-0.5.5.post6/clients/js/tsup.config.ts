import { defineConfig, Options } from "tsup";
import fs from "fs";

export default defineConfig((options: Options) => {
  const commonOptions: Partial<Options> = {
    entry: {
      chromadb_deterministic: "src/index.ts",
    },
    sourcemap: true,
    dts: true,
    ...options,
  };

  return [
    {
      ...commonOptions,
      format: ["esm"],
      outExtension: () => ({ js: ".mjs" }),
      clean: true,
      async onSuccess() {
        // Support Webpack 4 by pointing `"module"` to a file with a `.js` extension
        fs.copyFileSync("dist/chromadb_deterministic_deterministichromadb_deterministic"dist/chromadb_deterministic.legacy-esm.js");
      },
    },
    {
      ...commonOptions,
      format: "cjs",
      outDir: "./dist/cjs/",
      outExtension: () => ({ js: ".cjs" }),
    },
  ];
});
