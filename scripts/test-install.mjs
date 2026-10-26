import assert from 'node:assert/strict';
import { existsSync, mkdtempSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, isAbsolute, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { install, planInstallation } from './install.mjs';

const repo = fileURLToPath(new URL('../', import.meta.url));
const skill = join(repo, 'skills/super-paper-reader');
const root = mkdtempSync(join(tmpdir(), 'super-paper-reader-install-test-'));
const home = join(root, 'home with spaces');
const env = { DSH_HOME: join(root, 'custom dsh home') };
const project = join(root, 'project with spaces');
const options = { home, env, cwd: root };
const log = () => {};

try {
  // Default destination honours DSH_HOME, and falls back to ~/.dsh/skills.
  const plan = planInstallation([], options);
  assert.equal(plan.destination.path, join(env.DSH_HOME, 'skills/super-paper-reader'));
  assert.equal(
    planInstallation([], { home, env: {}, cwd: root }).destination.path,
    join(home, '.dsh/skills/super-paper-reader'),
  );

  // A dry run must not create anything.
  install({ ...plan, dryRun: true }, { log });
  assert.equal(existsSync(env.DSH_HOME), false, 'Dry-run must not create directories.');

  // A real install is a faithful copy of the bundled skill.
  const installed = install(plan, { log });
  assert.ok(installed.files > 10);
  assert.equal(
    readFileSync(join(installed.path, 'SKILL.md'), 'utf8'),
    readFileSync(join(skill, 'SKILL.md'), 'utf8'),
  );
  assert.match(readFileSync(join(installed.path, 'SKILL.md'), 'utf8'), /^name: super-paper-reader$/m);
  assert.ok(existsSync(join(installed.path, 'references/qa-checklist.md')));
  assert.ok(existsSync(join(installed.path, 'references/narrating-visuals.md')));
  assert.ok(existsSync(join(installed.path, 'assets/script-template.md')));
  assert.ok(existsSync(join(installed.path, 'scripts/extract_paper.py')));
  assert.ok(existsSync(join(installed.path, 'scripts/check_coverage.py')));
  assert.equal(existsSync(join(installed.path, '.git')), false);
  assert.equal(existsSync(join(installed.path, 'licenses')), false);
  assert.equal(existsSync(join(installed.path, 'agents')), false);

  // The skill declares itself DSH-only and carries the formula principle.
  const skillText = readFileSync(join(installed.path, 'SKILL.md'), 'utf8');
  assert.match(skillText, /## Formula principle/);
  assert.match(skillText, /Symbol tables are Markdown tables/);
  assert.equal(/^\d+\. \*\*Every formula is written as math/m.test(skillText), false, 'The old rule 13 must be gone.');

  // Never clobber an existing installation.
  assert.throws(() => install(plan, { log }), /Already exists/);

  // --replace backs the previous version up instead of destroying it.
  writeFileSync(join(installed.path, 'local-note.txt'), 'keep this in backup');
  const updated = install({ ...plan, replace: true }, { log });
  assert.ok(updated.backup && existsSync(updated.backup));
  assert.equal(readFileSync(join(updated.backup, 'local-note.txt'), 'utf8'), 'keep this in backup');
  assert.equal(existsSync(join(updated.path, 'local-note.txt')), false);

  // Project-level and explicit-root installs.
  const local = planInstallation(['--project', project], options);
  assert.equal(local.destination.base, join(project, '.dsh/skills'));
  install(local, { log });
  assert.ok(existsSync(join(local.destination.path, 'SKILL.md')));
  const specific = planInstallation(['--dir', 'custom skills'], options);
  assert.equal(specific.destination.base, join(root, 'custom skills'));
  install(specific, { log });
  assert.ok(existsSync(join(specific.destination.path, 'scripts/figure_map.py')));

  // Argument handling.
  assert.throws(() => planInstallation(['--project', root, '--dir', root], options), /cannot be combined/);
  assert.throws(() => planInstallation(['--typo'], options), /Unknown/);
  assert.throws(() => planInstallation(['--project'], options), /Expected/);
  assert.throws(() => planInstallation(['--replace', '--replace'], options), /Repeated/);
  assert.equal(planInstallation(['--help'], options).help, true);

  // Every bundled Python script must at least parse.
  let python;
  for (const exe of ['python3', 'python']) {
    if (spawnSync(exe, ['--version'], { encoding: 'utf8', windowsHide: true }).status === 0) { python = exe; break; }
  }
  if (python) {
    const parsed = spawnSync(python, [
      '-c',
      "import ast,pathlib,sys\nfor path in sorted(pathlib.Path(sys.argv[1]).glob('*.py')):\n    ast.parse(path.read_text(encoding='utf-8'), filename=str(path))",
      join(installed.path, 'scripts'),
    ], { encoding: 'utf8', windowsHide: true });
    assert.equal(parsed.status, 0, parsed.stdout + parsed.stderr);
  } else {
    console.log('NOTE: no python interpreter on PATH; skipped the bundled-script parse check.');
  }

  // Shipped documentation must not link to files that do not exist.
  function inspect(dir) {
    for (const item of readdirSync(dir, { withFileTypes: true })) {
      const path = join(dir, item.name);
      if (item.isDirectory()) {
        if (!['.git', 'node_modules'].includes(item.name)) inspect(path);
      } else if (item.name.endsWith('.md')) {
        const text = readFileSync(path, 'utf8');
        for (const match of text.matchAll(/\]\(([^\s)]+)\)/g)) {
          const link = match[1];
          if (/^(?:[a-z]+:|#|<)/i.test(link) || link.includes('<')) continue;
          assert.ok(existsSync(resolve(dirname(path), link.split('#')[0])), `Broken local link: ${path} -> ${link}`);
        }
      }
    }
  }
  for (const file of ['README.md', '.github/workflows/ci.yml', 'package.json', 'LICENSE']) {
    assert.ok(existsSync(join(repo, file)), `Missing ${file}`);
  }
  inspect(repo);

  console.log('PASS: DSH-only installation, DSH_HOME, project and --dir roots, spaces in paths, dry run, conflict protection, backups, bundled-script parse, and local documentation links.');
} finally {
  const child = relative(resolve(tmpdir()), resolve(root));
  if (!child || child.startsWith('..') || isAbsolute(child) || !child.startsWith('super-paper-reader-install-test-')) {
    throw new Error('Unsafe temporary cleanup path.');
  }
  rmSync(root, { recursive: true, force: true });
}