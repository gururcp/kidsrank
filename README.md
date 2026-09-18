# 🏅 Family Game Board

A star-award ranking board for the games you play with the kids — a different game
each day, scored live on the big screen, with a running leaderboard across all days.

No internet, no accounts, no installing anything. If you want two screens to
show the same board — one in the living room, one in somebody's pocket — there
is an optional [shared family board](#sharing-one-board-between-devices).

## How to open it

**Double-click `index.html`.** That's it. It opens in your browser and works
straight away, even with the wifi off.

Best on a laptop or TV screen so everyone can see it from the sofa. It also works
fine on a phone or tablet.

> Tip: on the day, open it and press <kbd>F11</kbd> for full screen.

## First time

1. You land on **Add players**. For each kid: type their name, tap
   **📷 Add photo** to use a real picture of them (they spot themselves much
   faster), pick a colour, and save. Add all the kids.
2. Tap **🎮 Start a game**.

## Running a game

Pick the date (defaults to today), type the game's name, and choose the type:

### 🔔 Quiz — buzzer style
Whoever answers first gets the point. **Tap a kid's card** to give them +1. The
leader wears the 👑. Most correct answers wins.

- `−` in the corner of a card takes one back off if you tapped the wrong kid.
- **↩ Undo** steps back through your last taps (up to 40 of them).
- Keyboard shortcuts: keys `1`–`9` score the 1st–9th card, `Z` undoes.
- **✖ Abort** in the header bins the whole game — nobody scores and nothing is saved.

#### Add a clock (optional)
On the setup screen you can put a countdown on a quiz to raise the tension. Three
choices — **🚫 No timer** is the default and behaves exactly as above.

| Choice | What happens |
|---|---|
| **⏳ Whole round** | One countdown for the whole quiz (say 5 minutes). Score as fast as you can; at zero the buzzer goes and no more points can be given. Tap **🏁 See results**. |
| **⚡ Per question** | A short clock (default 15s) on *every* question. Press **▶ Start question 1**, read it out — the first correct answer stops the clock and arms the next question. If nobody gets it in time the buzzer goes, and you tap **➡ Next question**. |

The clock turns amber, then red, and ticks audibly over the last few seconds.

- <kbd>Space</kbd> works the clock: start / pause / next question. So you can hold
  the laptop keyboard and never reach for the mouse.
- `−` and **↩ Undo** still work after time is up, so a mistap is always fixable.
- The clock keeps true time even if you switch tabs, pause, or refresh the page.

### ⏱️ Race — beat the clock
For "finish your lunch before the timer" games. Set the countdown, press
**▶ Start timer**, then tap **Done!** as each kid finishes — they're stamped with
their time and take the next place. Anyone still going when the clock hits zero
gets no placement stars.

- **↩ still going** un-finishes a kid if you tapped Done too early.
- **✖ Abort** ends the race with no result at all — nobody scores.
- The timer keeps proper time even if you switch tabs or refresh the page.

### Stars
Default payout is **5 / 3 / 2** stars for 1st / 2nd / 3rd, plus **1** for taking
part. You can change it for a single game on the setup screen, or change the
defaults for good in ⚙️ Settings.

When you finish, you get a results screen where the stars are still editable
before you save — then confetti, a fanfare and the winner's face. Everything
lands on the leaderboard and in History.

If a game went wrong and you would rather it never happened, **✖ Abort** (on the
game screen, or **✖ Abort — no stars** on the results screen) throws it away:
no stars for anyone, no History entry, nothing on the board.

## The rest

- **🏆 Board** — the leaderboard. Filter by All time / This month / Last 7 days /
  a single day. Tap any kid for their profile: total stars, medals, last games.
- **📅 History** — every game grouped by date. Tap a game to expand it and fix a
  name, move it to a different date, edit the stars, or delete it.
- **🧒 Kids** — add, rename, change the photo or colour. Removing a kid *retires*
  them so old games keep their name and the history stays honest.
- **⚙️ Settings** — board title, default star payout, sound on/off, and joining
  or leaving the shared family board.

## Where the data lives — please read

Everything is saved in **this browser's own storage on this computer** (one entry
called `kidsrank.v1`). Nothing is uploaded anywhere and no one else can see it.

That means, on its own, the history is lost if you:

- clear your browsing data / cookies / "site data",
- open the file in a *different* browser, or on a different computer,
- use the browser's private / incognito window.

Normal use — closing the browser, restarting the laptop, updating the browser —
is completely safe. The history survives all of that.

Photos are shrunk to 320×320 before saving (about 5–25 KB each), so a family's
worth of pictures and hundreds of games fit comfortably.

If a second device needs the same players and the same stars, that is what the
shared board below is for.

## Sharing one board between devices

Switched off out of the box. Switch it on and everybody who signs in sees **one
board**: the same players, the same games, the same running total of stars. Enter
the kids once, on one device, and they are simply there on the others.

It also means you can **score from a phone while the television shows the board**.
Tap a point on the phone and the number moves on the TV a moment later; the timer
counts down on both; when you press Finish, the confetti goes off on both.

Nothing about being offline changes. Every device keeps its own full copy in
`localStorage`, exactly as before, so the board still works with the wifi off —
taps made in a dead spot go up on their own the next time there is a signal.

### What is shared, and what stays on the device

| Shared with everyone | Stays on this device |
|---|---|
| Players — names, photos, colours | Sound on/off |
| Games, live and finished | Which screen you are looking at, filters |
| Stars and the leaderboard | Half-typed forms, and your own undo |
| Board title, default star payout | |

Sound is per device on purpose: muting your phone should not mute the television.

### It is already turned on

The published board at **https://gururcp.github.io/kidsrank/** is wired to a
Firebase project (`kidsrank-aeeee`), and the two people allowed on it are set in
`firestore.rules`.

**On each device, once:** open that URL and tap **🔗 Sign in** — in the banner at
the top, or in ⚙️ Settings. Pick the Google account, and the device stays signed
in from then on. Do the living-room screen and each phone.

**It has to be that URL**, not a copy of `index.html` opened off the disk. Google
sign-in does not work from a `file://` page, so a local copy can only ever be a
private board in that one browser. Useful as a fallback; it will not share.

The rest of this section is only needed to **change** who is on the board, or to
point a fork of this at a Firebase project of its own.

#### Who is allowed on

`firestore.rules` holds the list, and it is the only thing protecting the board.
The app is on a public URL and the Firebase config in `index.html` is public by
design — it names the project, it grants nothing. The rules grant.

To add or remove somebody, edit the list — lower-case, always — and deploy:

```sh
npx firebase-tools@latest login
npx firebase-tools@latest deploy --only firestore:rules --project kidsrank-aeeee
```

**Deploying is the step that counts.** Editing the file changes nothing until it
is deployed; until then the database is running on whatever rules it last
received. Someone signing in with an unlisted Google account is refused on every
read and write, and the board tells them so.

#### Where the Firebase config lives

Not in this repository. It sits in one place — the repository secret
`FIREBASE_CONFIG` — and `.github/inject-config.mjs` drops it into the copy of
`index.html` that gets published, on every push to `main`. That is why Pages
builds from a workflow instead of serving the branch.

Not because it is a secret. A Firebase web config is public by design: it names
the project, it grants nothing, and it is plainly readable in the published page.
It is kept out of the repository because the laptop this is written on scans
every commit for things shaped like API keys, and a Firebase `apiKey` is shaped
exactly like one. `firestore.rules` is what actually decides who may read the
board.

To change it:

```sh
gh secret set FIREBASE_CONFIG --repo gururcp/kidsrank --body '{"apiKey":"…", … }'
```

JSON, so every key quoted — not the JavaScript form the Firebase console shows.
A missing or malformed secret **fails the publish** on purpose, rather than
quietly deploying a board where sign-in never appears.

#### Pointing this at a different Firebase project

1. At [console.firebase.google.com](https://console.firebase.google.com), create
   a project. The free Spark plan is far more than a family needs, and it is not
   paused for going quiet.
2. **Build → Firestore Database → Create database**, in *production mode*.
3. **Build → Authentication → Get started → Google**, and enable it.
4. **Authentication → Settings → Authorized domains** → add the domain the board
   is served from, `gururcp.github.io`. Sign-in fails without this, and
   `localhost` is allowed from the start for testing.
5. **Project settings → Your apps → Web app** → copy the `firebaseConfig` object
   into the `FIREBASE_CONFIG` secret as above. `measurementId` is dropped even
   if you include it — that is Google Analytics, and a family scoreboard has no
   business reporting the children's activity anywhere.
6. Put the addresses in `firestore.rules` and deploy them, as above.

Deleting the `FIREBASE_CONFIG` secret turns sharing off altogether — but the
publish fails rather than silently deploying an unshared board, so to switch it
off deliberately, take the `inject-config` step out of the workflow as well. The
app then goes back to being a private board inside one browser, with no network
and no sign-in, exactly as it began.

### The first time each device signs in

- If the family board is **empty** and this device has players on it, this
  device's board becomes the family board.
- If the family board **already has** players and this device also has its own,
  you are asked which one to keep. The other is not merged — merging silently
  produces two of every child — and it is not thrown away either: the board as it
  stood is copied to a `kidsrank.v1.backup.…` entry in the same browser storage
  before anything is replaced.
- After that, the family board is simply the board.

**⚙️ Settings → Sign out of the shared board** leaves it at any time. The device
keeps everything it has; it just stops matching the others.

## Files

| File | What it is |
|---|---|
| `index.html` | The entire app — screens, scoring, storage, sharing. Nothing else needed. |
| `tailwind.js` | Tailwind CSS saved locally so it looks right with no internet. |
| `firestore.rules` | Who is allowed on the shared board. The only thing protecting it. |
| `firebase.json` | So the rules above can be deployed with one command. |
| `.github/workflows/pages.yml` | Publishes the board, config and all, on every push. |
| `.github/inject-config.mjs` | Puts the Firebase config into the published page. |
| `README.md` | This file. |

Made to be copied: put the whole folder on a USB stick or in OneDrive and it runs
anywhere. (Copying the folder does **not** copy the game history — see above.)
