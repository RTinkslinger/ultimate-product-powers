#!/usr/bin/env node
import { v0 } from 'v0-sdk';
import { writeFileSync, mkdirSync, readFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { parseArgs } from 'util';

const { values: args } = parseArgs({
  options: {
    prompt: { type: 'string' },
    mood: { type: 'string', default: '' },
    'tailwind-config': { type: 'string', default: '' },
    components: { type: 'string', default: '' },
    output: { type: 'string' },
  },
});

if (!args.prompt || !args.output) {
  console.error('Usage: v0-generate.mjs --prompt "..." --output ./path/');
  console.error('Required: --prompt, --output');
  console.error('Optional: --mood, --tailwind-config, --components');
  process.exit(1);
}

if (!process.env.V0_API_KEY) {
  console.error('V0_API_KEY not set. Get key from v0.dev/chat/settings/keys');
  process.exit(1);
}

let tailwindContext = '';
if (args['tailwind-config'] && existsSync(args['tailwind-config'])) {
  const config = readFileSync(args['tailwind-config'], 'utf-8');
  const themeMatch = config.match(/theme\s*:\s*\{[\s\S]*?\n\s*\}/);
  if (themeMatch) tailwindContext = `\nTailwind theme:\n${themeMatch[0]}`;
}

const fullPrompt = [
  args.prompt,
  args.mood ? `\nVisual direction: ${args.mood}` : '',
  args.components ? `\nInstalled shadcn components: ${args.components}` : '',
  tailwindContext,
  '\nUse Next.js App Router, shadcn/ui, and Tailwind CSS.',
  '\nUse real, representative content — not lorem ipsum.',
].filter(Boolean).join('');

try {
  const chat = await v0.chats.create({ message: fullPrompt });
  const files = chat.latestVersion?.files || [];

  if (files.length === 0) {
    console.error('v0 returned no files. Prompt may be too vague.');
    process.exit(1);
  }

  mkdirSync(args.output, { recursive: true });

  const written = [];
  for (const file of files) {
    const filePath = join(args.output, file.name);
    mkdirSync(dirname(filePath), { recursive: true });
    writeFileSync(filePath, file.content);
    written.push(file.name);
  }

  const result = {
    files: written,
    chatId: chat.id || null,
    tokensUsed: chat.latestVersion?.tokensUsed || null,
  };

  console.log(JSON.stringify(result, null, 2));
} catch (err) {
  if (err.status === 429) {
    console.error('v0 rate limit hit. Daily limit: 1K messages. Try again later or use v0.dev directly.');
    process.exit(1);
  }
  console.error(`v0 API error: ${err.message}`);
  process.exit(1);
}
