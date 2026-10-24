// Run with: node scripts/test-render.mjs. No third-party test dependencies.
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, cpSync, existsSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve, relative, isAbsolute } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import assert from 'node:assert/strict';

const root = mkdtempSync(join(tmpdir(), 'paper-explainer-test-'));
try {
  const skill = join(root, 'copied skill');
  cpSync(fileURLToPath(new URL('../', import.meta.url)), skill, { recursive: true });
  const work = join(root, 'unrelated cwd');
  mkdirSync(work);
  const assets = join(work, 'assets');
  mkdirSync(assets);
  writeFileSync(join(assets, 'pixel.png'), Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jA1EAAAAASUVORK5CYII=', 'base64'));
  const draft = join(work, 'paper with spaces.md');
  const global = join(root, 'user global settings');
  mkdirSync(global);
  const untouched = '{"theme":"blueprint","open":true}';
  writeFileSync(join(global, 'config.json'), untouched);
  const run = (...args) => spawnSync(process.execPath, [join(skill, 'scripts/render.mjs'), ...args], {
    cwd: work, env: { ...process.env, AM_HOME: global }, encoding: 'utf8', windowsHide: true,
  });
  const content = `---\ntitle: Test\nlang: zh\n---\n\n## 路线\n\nOnly local resources.\n\n## 方法\n\n![pixel](assets/pixel.png)\n\n$$\ny=W x\n$$\n\n<details>\n<summary>补充</summary>\n\nHidden **bold** and $x^2$.\n\n</details>\n\n\`\`\`flow\n输入 -> 输出: 计算\n\`\`\`\n\n## 证据\n\nPartial evidence.\n`;
  writeFileSync(draft, content);
  const result = run(draft);
  assert.equal(result.status, 0, result.stdout + result.stderr);
  const html = readFileSync(draft.replace(/\.md$/, '.html'), 'utf8');
  assert.match(html, /class="am-toc"/);
  assert.ok(!html.includes('<span class="am-panel-id">'), 'Letter badges must be absent.');
  const toc = html.match(/<nav class="am-toc"[\s\S]*?<\/nav>/)?.[0];
  assert.ok(toc && !/<a\b[^>]*>[A-Z]+ · /.test(toc), 'TOC must show chapter names without letter prefixes.');
  assert.ok([...toc.matchAll(/href="#([^"]+)"/g)].every(m=>html.includes(`id="${m[1]}"`)), 'Internal navigation anchors must remain valid.');
  assert.match(html, /<math[\s>]/);
  assert.match(html, /data:image\/png;base64,/);
  assert.match(html, /<details>[\s\S]*<strong>bold<\/strong>[\s\S]*<\/details>/);
  assert.ok(html.includes('<main class="am-doc">'), 'Single-column document template must be used.');
  assert.equal(readFileSync(draft, 'utf8'), content);
  assert.equal(readFileSync(join(global, 'config.json'), 'utf8'), untouched);
  const explicit = join(work, 'nested output', 'chosen.html');
  assert.equal(run(draft, '--out', explicit).status, 0);
  assert.ok(existsSync(explicit));
  const missing = join(work, 'missing-image.md');
  writeFileSync(missing, '---\ntitle: Missing\n---\n## Method\n![missing](absent.png)\n');
  assert.notEqual(run(missing).status, 0);
  assert.equal(existsSync(missing.replace('.md', '.html')), false);
  assert.notEqual(run(join(work, 'no-source.md')).status, 0);
  assert.notEqual(run(draft, '--out', draft).status, 0);
  const invalid = join(work, 'bad-flow.md');
  writeFileSync(invalid, '---\ntitle: Invalid\n---\n## Method\n```flow\n[unclosed -> B\n```\n');
  assert.notEqual(run(invalid).status, 0);
  console.log('PASS: relocated skill, independent cwd, spaced paths, custom output, source preservation, isolated settings, embedded math/image, folding markup, and error handling.');
} finally {
  // Delete only the uniquely created test directory under the OS temporary root.
  const child = relative(resolve(tmpdir()), resolve(root));
  if (!child || child.startsWith('..') || isAbsolute(child) || !child.startsWith('paper-explainer-test-')) {
    throw new Error('Refusing to remove a path outside the test temporary directory.');
  }
  rmSync(root, { recursive: true, force: true });
}
