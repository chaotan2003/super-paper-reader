import assert from 'node:assert/strict';
import { cpSync, existsSync, mkdtempSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, isAbsolute, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { install, planInstallation } from './install.mjs';

const repo = fileURLToPath(new URL('../', import.meta.url));
const root = mkdtempSync(join(tmpdir(), 'paper-skill-install-test-'));
const home = join(root, 'home with spaces');
const env = { DSH_HOME: join(root, 'custom dsh home') };
const project = join(root, 'project with spaces');
const options = { home, env, cwd: root };
const log = () => {};
try {
  const plan = planInstallation(['--target', 'both'], options);
  assert.equal(plan.destinations[0].path, join(home, '.agents/skills/super-paper-reader'));
  assert.equal(plan.destinations[1].path, join(env.DSH_HOME, 'skills/super-paper-reader'));
  install({ ...plan, dryRun: true }, { log });
  assert.equal(existsSync(home), false, 'Dry-run must not create directories.');
  const installed = install(plan, { log });
  for (const item of installed) {
    assert.equal(readFileSync(join(item.path, 'SKILL.md'), 'utf8'), readFileSync(join(repo, 'skills/super-paper-reader/SKILL.md'), 'utf8'));
    assert.ok(existsSync(join(item.path, 'scripts/vendor/am.mjs')));
    assert.ok(existsSync(join(item.path, 'licenses/project-MIT.txt')));
    assert.equal(existsSync(join(item.path, 'references/pi0-original.md')), false);
    assert.equal(existsSync(join(item.path, '.git')), false);
  }
  assert.throws(() => install(plan, { log }), /Already exists/);
  writeFileSync(join(installed[0].path, 'local-note.txt'), 'keep this in backup');
  const updated = install({ ...plan, replace: true }, { log });
  assert.equal(readFileSync(join(updated[0].backup, 'local-note.txt'), 'utf8'), 'keep this in backup');
  assert.equal(existsSync(join(updated[0].path, 'local-note.txt')), false);

  const local = planInstallation(['--target', 'both', '--project', project], options);
  assert.equal(local.destinations[0].base, join(project, '.agents/skills'));
  assert.equal(local.destinations[1].base, join(project, '.dsh/skills'));
  install(local, { log });
  const specific = planInstallation(['--target', 'codex', '--dir', 'custom skills'], options);
  assert.equal(specific.destinations[0].base, join(root, 'custom skills'));
  assert.throws(() => planInstallation(['--target', 'both', '--dir', root], options), /single target|one target/);
  assert.throws(() => planInstallation(['--target', 'invalid'], options), /Choose/);
  assert.throws(() => planInstallation(['--target'], options), /Expected/);
  assert.throws(() => planInstallation(['--target', 'codex', '--typo'], options), /Unknown/);

  // A conflicting second destination must leave the first untouched.
  const conflictRoot = join(root, 'preflight');
  const conflict = planInstallation(['--target', 'both', '--project', conflictRoot], options);
  mkdirSync(conflict.destinations[1].path, { recursive: true });
  assert.throws(() => install(conflict, { log }), /Already exists/);
  assert.equal(existsSync(conflict.destinations[0].base), false);

  // Verify an actually installed copy can render outside this repository.
  cpSync(join(repo, 'examples/render-demo.md'), join(root, 'demo.md'));
  const rendered = spawnSync(process.execPath, [join(installed[1].path, 'scripts/render.mjs'), join(root, 'demo.md')], { cwd: root, encoding: 'utf8', windowsHide: true });
  assert.equal(rendered.status, 0, rendered.stdout + rendered.stderr);
  assert.match(readFileSync(join(root, 'demo.html'), 'utf8'), /<math[\s>]/);

  // Check shipped documentation links are self-contained, excluding external URLs.
  function inspect(dir) {
    for (const item of readdirSync(dir, { withFileTypes: true })) {
      const path = join(dir, item.name);
      if (item.isDirectory()) { if (!['.git', 'node_modules'].includes(item.name)) inspect(path); }
      else if (item.name.endsWith('.md')) {
        const text = readFileSync(path, 'utf8');
        for (const match of text.matchAll(/\]\(([^\s)]+)\)/g)) {
          const link = match[1];
          if (/^(?:[a-z]+:|#|<)/i.test(link) || link.includes('<') || link.startsWith('assets/')) continue;
          assert.ok(existsSync(resolve(dirname(path), link.split('#')[0])), `Broken local link: ${path} -> ${link}`);
        }
      }
    }
  }
  inspect(repo);
  console.log('PASS: user/project installation, DSH_HOME, spaces, dry-run, conflict protection, backups, installed rendering, and local documentation links.');
} finally {
  const child = relative(resolve(tmpdir()), resolve(root));
  if (!child || child.startsWith('..') || isAbsolute(child) || !child.startsWith('paper-skill-install-test-')) throw new Error('Unsafe temporary cleanup path.');
  rmSync(root, { recursive: true, force: true });
}
