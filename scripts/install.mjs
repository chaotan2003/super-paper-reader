#!/usr/bin/env node
import { cpSync, existsSync, lstatSync, mkdirSync, readFileSync, readdirSync, renameSync } from 'node:fs';
import { homedir } from 'node:os';
import { basename, dirname, isAbsolute, join, relative, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const name = 'super-paper-reader';
const source = fileURLToPath(new URL('../skills/super-paper-reader/', import.meta.url));
const usage = `Usage: node scripts/install.mjs [options]

  --project <root>  Install for one project (use its Git repository root).
  --dir <root>      Explicit skills root, i.e. the parent directory of the skill.
  --replace         Back up an existing installation before replacing it.
  --dry-run         Print the destination without writing anything.
  --help            Show this help.

Super Paper Reader installs into DeepSeek Harness only.
Default: $DSH_HOME/skills, or ~/.dsh/skills when DSH_HOME is unset.
Project: <project root>/.dsh/skills.
No downloads, no global settings changes, no background services.`;

export function planInstallation(args, { home = homedir(), env = process.env, cwd = process.cwd() } = {}) {
  const options = {};
  for (let i = 0; i < args.length; i++) {
    const key = args[i];
    if (['--replace', '--dry-run', '--help'].includes(key)) {
      if (options[key]) throw new Error(`Repeated option: ${key}`);
      options[key] = true;
    } else if (['--project', '--dir'].includes(key)) {
      if (options[key] || !args[i + 1] || args[i + 1].startsWith('--')) throw new Error(`Expected one value for ${key}`);
      options[key] = args[++i];
    } else throw new Error(`Unknown argument: ${key}`);
  }
  if (options['--help']) return { help: true };
  if (options['--project'] && options['--dir']) throw new Error('--project and --dir cannot be combined.');
  const project = options['--project'] && resolve(cwd, options['--project']);
  const base = options['--dir']
    ? resolve(cwd, options['--dir'])
    : project
      ? join(project, '.dsh', 'skills')
      : join(env.DSH_HOME ? resolve(cwd, env.DSH_HOME) : join(home, '.dsh'), 'skills');
  return {
    destination: { base, path: join(base, name) },
    replace: !!options['--replace'],
    dryRun: !!options['--dry-run'],
  };
}

function filesIn(root, prefix = '') {
  return readdirSync(join(root, prefix), { withFileTypes: true })
    .flatMap(entry => {
      const path = join(prefix, entry.name);
      if (entry.isSymbolicLink()) throw new Error(`Symlink inside skill bundle: ${path}`);
      return entry.isDirectory() ? filesIn(root, path) : [path];
    })
    .sort();
}

export function install(plan, { skillSource = source, log = console.log } = {}) {
  if (plan.help) { log(usage); return null; }
  if (!existsSync(join(skillSource, 'SKILL.md'))) {
    throw new Error('Missing bundled SKILL.md; keep the repository layout intact.');
  }
  const files = filesIn(skillSource);
  const destination = plan.destination;
  if (basename(destination.path) !== name || dirname(destination.path) !== destination.base) {
    throw new Error('Invalid installation destination.');
  }
  if (existsSync(destination.path) && lstatSync(destination.path).isSymbolicLink()) {
    throw new Error(`Destination is a symlink; manage it manually: ${destination.path}`);
  }
  if (existsSync(destination.path) && !plan.replace && !plan.dryRun) {
    throw new Error(`Already exists: ${destination.path}\nUse --replace to back it up and install this version.`);
  }
  // Avoid installing the bundle into itself or a child of itself.
  const child = relative(resolve(skillSource), resolve(destination.path));
  if (!child || (!isAbsolute(child) && child !== '..' && !child.startsWith('..' + (process.platform === 'win32' ? '\\' : '/')))) {
    throw new Error('Destination must be outside the source skill.');
  }
  if (plan.dryRun) {
    log(`[dry-run] DeepSeek Harness: ${destination.path}`);
    return { ...destination, files: files.length };
  }
  mkdirSync(destination.base, { recursive: true });
  // Stage and verify every file before replacing an existing installation.
  const stage = join(destination.base, `.${name}.staging-${process.pid}-${Date.now()}`);
  cpSync(skillSource, stage, { recursive: true, errorOnExist: true, force: false });
  for (const file of files) {
    if (!readFileSync(join(skillSource, file)).equals(readFileSync(join(stage, file)))) {
      throw new Error(`Copy verification failed: ${file}`);
    }
  }
  let backup;
  if (existsSync(destination.path)) {
    backup = join(
      dirname(destination.base),
      '.super-paper-reader-backups',
      `${new Date().toISOString().replace(/[:.]/g, '-')}-${process.pid}`,
    );
    mkdirSync(dirname(backup), { recursive: true });
    renameSync(destination.path, backup);
  }
  try { renameSync(stage, destination.path); }
  catch (error) {
    if (backup && !existsSync(destination.path)) renameSync(backup, destination.path);
    throw error;
  }
  log(`Installed Super Paper Reader for DeepSeek Harness: ${destination.path}`);
  log(`Skill files: ${files.length}`);
  if (backup) log(`Previous version: ${backup}`);
  return { ...destination, files: files.length, backup };
}

if (process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url) {
  try {
    if (Number(process.versions.node.split('.')[0]) < 20) throw new Error('Node.js 20+ is required.');
    install(planInstallation(process.argv.slice(2)));
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}