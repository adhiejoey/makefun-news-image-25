// Entry exporter for the news-image build.
//
// The picture itself is rendered ahead of time by gen.py and stored next
// to this file as entry.png. All this program does is carry those exact
// bytes into the directory the grader asks for, so the submitted image is
// bit-for-bit the one we reviewed.

import * as fs from "node:fs";
import * as path from "node:path";
import { fileURLToPath } from "node:url";

// The folder this script lives in, which is also where entry.png sits.
// Resolving it from the module URL keeps the program working no matter
// which directory it is launched from.
const scriptFolder = path.dirname(fileURLToPath(import.meta.url));

// Destination folder: the grader points here with MAKEFUN_OUTPUT_DIR,
// and /output is the fallback when nothing is set.
const targetFolder = process.env.MAKEFUN_OUTPUT_DIR
  ? process.env.MAKEFUN_OUTPUT_DIR
  : "/output";

const sourceFile = path.join(scriptFolder, "entry.png");
const destFile = path.join(targetFolder, "entry.png");

// Read the rendered picture into memory as raw bytes, then write those
// same bytes back out. Nothing is re-encoded, so the copy is identical.
const pictureData = fs.readFileSync(sourceFile);

fs.mkdirSync(targetFolder, { recursive: true });
fs.writeFileSync(destFile, pictureData);
