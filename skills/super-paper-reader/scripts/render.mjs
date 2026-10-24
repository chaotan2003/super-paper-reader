#!/usr/bin/env node
// Thin entry point for the unmodified Answer me with HTML bundle.
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { resolve, dirname, extname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const args = process.argv.slice(2);
const usage = 'Usage: node render.mjs <draft.md> [--out <page.html>]';
if (args.length === 1 && ['--help', '-h'].includes(args[0])) {
  console.log(usage);
  process.exit(0);
}
if (![1, 3].includes(args.length) || args[0]?.startsWith('-') ||
    (args.length === 3 && args[1] !== '--out')) {
  console.error(usage);
  process.exit(2);
}
if (Number(process.versions.node.split('.')[0]) < 20) {
  console.error('Node.js 20+ is required. Install Node.js or use your agent host\'s available Node runtime.');
  process.exit(2);
}
try {
  const draft = resolve(args[0]);
  const out = args[2] ? resolve(args[2]) : draft.slice(0, -extname(draft).length) + '.html';
  if (extname(draft).toLowerCase() !== '.md' || extname(out).toLowerCase() !== '.html') {
    throw new Error('Input must be .md and output must be .html.');
  }
  if (!readFileSync(draft, 'utf8').trim()) throw new Error('Draft is empty.');
  mkdirSync(dirname(out), { recursive: true });
  // Isolate upstream state; never read or change the user's global AM_HOME.
  const state = join(dirname(out), '.paper-reading-renderer');
  mkdirSync(state, { recursive: true });
  writeFileSync(join(state, 'config.json'), JSON.stringify({
    open: false, update_check: false, close_after_reply: false,
    theme: 'paper', template: 'doc', mode: 'light', style: 'off',
  }));
  const vendor = fileURLToPath(new URL('./vendor/am.mjs', import.meta.url));
  const result = spawnSync(process.execPath, [vendor, 'render', draft, '-o', out,
    '--no-open', '--template', 'doc', '--theme', 'paper', '--mode', 'light', '--style', 'off'], {
    env: { ...process.env, AM_HOME: state, AM_NO_OPEN: '1' },
    encoding: 'utf8', windowsHide: true, maxBuffer: 8 * 1024 * 1024,
  });
  if (result.stdout) process.stdout.write(result.stdout);
  if (result.stderr) process.stderr.write(result.stderr);
  if (result.error) throw result.error;
  if (result.status !== 0) process.exit(result.status ?? 1);
  if (!existsSync(out)) throw new Error('Renderer returned success without an output file.');
  // Article presentation: keep anchor IDs and source intact, remove UI letter badges.
  const generated = readFileSync(out, 'utf8');
  const article = generated
    .replace(/<span class="am-panel-id">[^<]*<\/span>/g, '')
    .replace(/<nav class="am-toc"[\s\S]*?<\/nav>/g,
      nav => nav.replace(/(<a\b[^>]*>)[A-Z]+ · /g, '$1'));
  writeFileSync(out, article);
  console.log('Preserved Markdown: ' + draft);
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
