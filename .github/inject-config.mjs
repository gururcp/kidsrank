/* Puts the Firebase config into index.html at publish time.
   ---------------------------------------------------------------------------
   The config is not in this repository. It lives in one place, the repository
   secret FIREBASE_CONFIG, and this script drops it into the copy of index.html
   that gets published. Nothing is written back into git.

   Not because the config is a secret — it is public by design, it names the
   Firebase project and grants nothing on its own, and it is plainly visible in
   the published page. It is kept out of the repository because the laptop this
   is written on scans every commit for things shaped like API keys, and a
   Firebase apiKey is shaped exactly like one. What actually decides who may
   read the board is firestore.rules.

   This script fails the build rather than publishing a board that quietly does
   not share. A missing secret would otherwise deploy a page where sign-in never
   appears, which looks like a bug in the app and is very hard to guess at. */

import fs from 'fs';

const FILE   = 'index.html';
const MARKER = 'const FIREBASE_CONFIG = null;';
const NEEDED = ['apiKey', 'authDomain', 'projectId', 'appId'];

const die = msg => { console.error('✗ ' + msg); process.exit(1); };

const raw = (process.env.FIREBASE_CONFIG || '').trim();
if (!raw) {
  die('The FIREBASE_CONFIG secret is empty or not set.\n' +
      '  Set it with:  gh secret set FIREBASE_CONFIG --repo <owner>/<repo>\n' +
      '  The value is the firebaseConfig object as JSON, from the Firebase\n' +
      '  console: Project settings -> Your apps -> Web app.');
}

let cfg;
try {
  cfg = JSON.parse(raw);
} catch (e) {
  die('FIREBASE_CONFIG is not valid JSON: ' + e.message + '\n' +
      '  It wants JSON, so every key quoted: {"apiKey":"...","authDomain":"..."}\n' +
      '  not the JavaScript form the Firebase console shows.');
}
if (!cfg || typeof cfg !== 'object' || Array.isArray(cfg)) die('FIREBASE_CONFIG is not an object.');

const missing = NEEDED.filter(k => !cfg[k]);
if (missing.length) die('FIREBASE_CONFIG is missing: ' + missing.join(', '));

/* Google Analytics, which a scoreboard for two children has no business
   feeding. Dropped here too, so it cannot creep back in through the secret. */
delete cfg.measurementId;

const html = fs.readFileSync(FILE, 'utf8');
const hits = html.split(MARKER).length - 1;
if (hits !== 1) {
  die('Expected exactly one "' + MARKER + '" in ' + FILE + ', found ' + hits + '.\n' +
      '  If that line was edited, this script and index.html have drifted apart.');
}

const block = 'const FIREBASE_CONFIG = ' + JSON.stringify(cfg, null, 2) + ';';
fs.writeFileSync(FILE, html.replace(MARKER, block));

console.log('✓ Firebase config written into ' + FILE +
            ' (project ' + cfg.projectId + ', ' + Object.keys(cfg).length + ' keys)');
