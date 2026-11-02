#!/usr/bin/env node
// Test MMS English alignment on granny narration (same system as kashmir_audio,
// English adapter instead of sa-IN).
const fs = require("fs");
const { execSync } = require("child_process");
const { createAligner, alignNative } = require("mms-forced-align");

async function main() {
  const [wav, wordsJson] = process.argv.slice(2);
  const f32 = "/tmp/mms_eng_test.f32";
  execSync(`ffmpeg -y -v error -i "${wav}" -ar 16000 -ac 1 -f f32le "${f32}"`);
  const buf = fs.readFileSync(f32);
  const waveform = new Float32Array(buf.buffer, buf.byteOffset, buf.byteLength / 4);
  const words = JSON.parse(fs.readFileSync(wordsJson, "utf8"));
  console.error("creating aligner (fp32)...");
  const aligner = await createAligner({ quantized: false });
  const t0 = Date.now();
  const timings = await alignNative(aligner, waveform, 16000, words, "en-IN");
  let scores = [];
  for (const t of timings) scores.push(t.score);
  scores.sort((a, b) => a - b);
  const mean = scores.reduce((s, x) => s + x, 0) / scores.length;
  console.error(`words=${timings.length} mean=${mean.toFixed(3)} min=${scores[0].toFixed(3)} p10=${scores[Math.floor(scores.length * 0.1)].toFixed(3)} ${(Date.now() - t0) / 1000}s`);
  // monotonic check
  let nonmono = 0;
  for (let i = 1; i < timings.length; i++) {
    if (timings[i].start < timings[i - 1].start) nonmono++;
  }
  console.error(`nonmono=${nonmono} first="${words[0]}"@${timings[0].start.toFixed(2)} last="${words[words.length-1]}"@${timings[timings.length-1].start.toFixed(2)}`);
  fs.writeFileSync("/tmp/mms_eng_out.json", JSON.stringify(timings.map((t, i) => ({ w: words[i], t_on: +t.start.toFixed(3), t_off: +t.end.toFixed(3), mms: +t.score.toFixed(3) }))));
  console.error("wrote /tmp/mms_eng_out.json");
  await aligner.dispose();
}
main().catch(e => { console.error(e); process.exit(1); });
