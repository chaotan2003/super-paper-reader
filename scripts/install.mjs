#!/usr/bin/env node
import { cpSync, existsSync, lstatSync, mkdirSync, readFileSync, readdirSync, renameSync } from 'node:fs';
import { homedir } from 'node:os';
import { basename, dirname, isAbsolute, join, relative, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const name = 'super-paper-reader';
const source = fileURLToPath(new URL('../skills/super-paper-reader/', import.meta.url));
const usage = `Usage: node scripts/install.mjs --target codex|dsh|both [options]

  --project <root>  Install only for this project (use its Git repository root).
  --dir <root>      Explicit skills root; single target only.
  --replace         Back up an existing installation before replacing it.
  --dry-run         Print destinations without writing anything.
  --help            Show this help.

Defaults: Codex ~/.agents/skills; DSH $DSH_HOME/skills or ~/.dsh/skills.
Project: Codex <root>/.agents/skills; DSH <root>/.dsh/skills.
No downloads, global settings changes, or background services.`;

export function planInstallation(args, { home = homedir(), env = process.env, cwd = process.cwd() } = {}) {
  const options = {};
  for (let i = 0; i < args.length; i++) {
    const key = args[i];
    if (['--replace', '--dry-run', '--help'].includes(key)) {
      if (options[key]) throw new Error(`Repeated option: ${key}`);
      options[key] = true;
    } else if (['--target', '--project', '--dir'].includes(key)) {
      if (options[key] || !args[i + 1] || args[i + 1].startsWith('--')) throw new Error(`Expected one value for ${key}`);
      options[key] = args[++i];
    } else throw new Error(`Unknown argument: ${key}`);
  }
  if (options['--help']) return { help: true };
  const target = options['--target'];
  if (!['codex', 'dsh', 'both'].includes(target)) throw new Error('Choose --target codex, dsh, or both.');
  if (options['--dir'] && (options['--project'] || target === 'both')) throw new Error('--dir requires one target and cannot be combined with --project.');
  const project = options['--project'] && resolve(cwd, options['--project']);
  const targets = target === 'both' ? ['codex', 'dsh'] : [target];
  const destinations = targets.map(host => {
    const base = options['--dir'] ? resolve(cwd, options['--dir']) : project
      ? join(project, host === 'codex' ? '.agents' : '.dsh', 'skills')
      : host === 'codex' ? join(home, '.agents', 'skills') : join(env.DSH_HOME ? resolve(cwd, env.DSH_HOME) : join(home, '.dsh'), 'skills');
    return { host, base, path: join(base, name) };
  });
  return { destinations, replace: !!options['--replace'], dryRun: !!options['--dry-run'] };
}

function filesIn(root, prefix = '') {
  return readdirSync(join(root, prefix), { withFileTypes: true }).flatMap(entry => {
    const path = join(prefix, entry.name);
    if (entry.isSymbolicLink()) throw new Error(`Symlink inside skill bundle: ${path}`);
    return entry.isDirectory() ? filesIn(root, path) : [path];
  }).sort();
}

export function install(plan, { skillSource = source, log = console.log } = {}) {
  if (plan.help) { log(usage); return []; }
  if (!existsSync(join(skillSource, 'SKILL.md'))) throw new Error('Missing bundled SKILL.md; keep the repository layout intact.');
  const files = filesIn(skillSource);
  // Check every destination before changing the first one.
  for (const item of plan.destinations) {
    if (basename(item.path) !== name || dirname(item.path) !== item.base) throw new Error('Invalid installation destination.');
    if (existsSync(item.path) && lstatSync(item.path).isSymbolicLink()) throw new Error(`Destination is a symlink; manage it manually: ${item.path}`);
    if (existsSync(item.path) && !plan.replace && !plan.dryRun) throw new Error(`Already exists: ${item.path}\nUse --replace to back it up and install this version.`);
    // Avoid installing the bundle into itself or a child of itself.
    const child = relative(resolve(skillSource), resolve(item.path));
    if (!child || (!isAbsolute(child) && child !== '..' && !child.startsWith('..' + (process.platform === 'win32' ? '\\' : '/')))) throw new Error('Destination must be outside the source skill.');
  }
  return plan.destinations.map(item => {
    if (plan.dryRun) { log(`[dry-run] ${item.host}: ${item.path}`); return item; }
    mkdirSync(item.base, { recursive: true });
    // Stage and verify all content before replacing an existing installation.
    const stage = join(item.base, `.${name}.staging-${process.pid}-${Date.now()}`);
    cpSync(skillSource, stage, { recursive: true, errorOnExist: true, force: false });
    for (const file of files) {
      if (!readFileSync(join(skillSource, file)).equals(readFileSync(join(stage, file)))) throw new Error(`Copy verification failed: ${file}`);
    }
    let backup;
    if (existsSync(item.path)) {
      backup = join(dirname(item.base), '.super-paper-reader-backups', `${new Date().toISOString().replace(/[:.]/g, '-')}-${item.host}-${process.pid}`);
      mkdirSync(dirname(backup), { recursive: true });
      renameSync(item.path, backup);
    }
    try { renameSync(stage, item.path); }
    catch (error) {
      if (backup && !existsSync(item.path)) renameSync(backup, item.path);
      throw error;
    }
    log(`Installed for ${item.host}: ${item.path}`);
    if (backup) log(`Previous version: ${backup}`);
    return { ...item, backup };
  });
}

if (process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url) {
  try {
    if (Number(process.versions.node.split('.')[0]) < 20) throw new Error('Node.js 20+ is required.');
    install(planInstallation(process.argv.slice(2)));
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}
