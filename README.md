# Meeting copilot

A small window for in-person meetings. Your laptop's built-in microphone listens, Whisper turns the speech into text (Arabic and English), and Claude suggests one thing to **SAY**, one question to **ASK**, and one thing to **FLAG** (a risk, a contradiction, or a topic nobody has covered yet). It aims at the goal in your brief, not just the last thing someone said.

Speech-to-text has three options (see Settings):
- **Groq (recommended):** runs the large Whisper model on Groq's servers. Fast, better with Arabic than the laptop can manage, free tier. Needs a free Groq key.
- **Whisper on this laptop:** free and the audio never leaves the laptop, but slower and less accurate. Used automatically when there is no Groq key, and as a fallback if Groq's free limit runs out mid-meeting.
- **Soniox:** paid cloud service that also labels speakers.

Claude itself can't take audio through its API, so a speech-to-text step is always needed.

## One-time setup

1. Install the packages:
   ```
   pip install -r requirements.txt
   ```
2. Get a free Groq key: sign up at console.groq.com, then API Keys, Create API Key.
3. Copy `.env.example` to `.env` and paste the key into `GROQ_API_KEY`.
4. Pick how it reaches Claude:
   - **Your Claude subscription (default):** nothing to set up if you are logged in to Claude Code on this laptop. The copilot runs Claude Code in the background, and its calls count toward your plan's usage limits.
   - **Claude API key:** create one at console.anthropic.com and put it in `ANTHROPIC_API_KEY`. It's faster and billed per use, separate from the subscription.
5. Let desktop apps use the microphone: Windows Settings, Privacy and security, Microphone, turn on "Let desktop apps access your microphone".
6. Make the shortcuts (Desktop, Start menu, and a sample one in this folder):
   ```
   python make_shortcuts.py
   ```
   To pin it: open Start, type "Meeting Copilot", right-click it, **Pin to taskbar**. Windows doesn't let apps pin themselves, so this step is yours.
7. Check the right mic is picked:
   ```
   python copilot.py --devices
   ```
   The `*` is the one it will use. To use another, put its number in `MIC_DEVICE` in `.env`.

## Before each meeting

Open the app and click **Edit brief** (or open `brief.md` yourself). Fill in the purpose, desired outcome, your role, who is attending, key facts, and topics that must come up, then save. Start the file with a line like `# Vendor review` so the app shows the meeting's name. The app rereads the brief when you press Start. Better briefs give better suggestions, and the attendee names help Whisper spell them right. To keep one brief per meeting, start it from a terminal with `--brief`:
```
python copilot.py --brief briefs/vendor-review.md
```

## In the meeting

Click the pinned **Meeting Copilot** icon (or run `python copilot.py`). The grey line under the suggestions says which speech engine and which Claude it is using.

1. **Tell the room** you are running a live transcription copilot and get a yes. Then press **Start**.
2. The **HEARD** box at the bottom shows the transcript as it comes in. Words type in like a streamed AI reply, and the box scrolls to follow them. If you scroll up to reread something, it stays where you are until you scroll back down.
3. Whisper can't tell voices apart, so lines have no speaker name. After you speak and your line appears, press **F8** to mark it as yours ("Me:"). Claude then knows what you already said.
4. Suggestions appear on their own after someone finishes speaking, at most every 45 seconds. Press **F9** any time for help right now (uses the stronger model).
5. When you want to speak, press **F10** or click **Draft speech**. Claude writes 70 to 120 words you can read aloud (under a minute): a link to what was just said, two or three points toward the meeting's goal, and a closing question or next step. It streams in from the top. Press **F10** again for another version, **Copy** to paste it somewhere, and **Esc** or **Back** to return to the suggestions. Suggestions that arrive while you're reading don't replace the speech; the grey line tells you one is waiting.
6. **Pause** stops listening, for the off-the-record parts.
7. Close the window when the meeting ends. It offers to write meeting notes (decisions, action items, open questions) to `summary.md`.

The keys work even when another app is in front. They also reach that app, though: F10 opens the menu bar in some programs. To use different keys, set `SPEECH_HOTKEY`, `HELP_HOTKEY` or `ME_HOTKEY` in `.env`.

**Timing:** with Groq, a line appears about 1 to 2 seconds after the speaker stops (about 1 second of that is the app waiting to be sure they paused). With Whisper on the laptop it's about 5 seconds. A suggestion takes about 4 to 5 seconds more.

The window states: green dot means listening, amber means loading, paused or reconnecting, red means something needs fixing (the text says what). The bar next to the button shows the mic level, so you can see it is hearing the room. While someone talks, the end of the HEARD box shows "Hearing speech..." and then "Transcribing...". If Windows animations are turned off (Settings, Accessibility, Visual effects), lines appear whole instead of typing in.

## Getting good audio from the laptop mic

- Put the laptop in the middle of the table, screen facing you, lid fully open.
- Don't type during the meeting. The keyboard sits right next to the mic and drowns out voices.
- If the bar barely moves when people talk, raise the input volume: Windows Settings, System, Sound, Input, Volume 80 to 100.
- One laptop mic hears near voices well and far voices poorly.

## Arabic

Test before a real meeting: press Start, talk for a minute mixing Arabic and English, and read the lines it writes. Groq runs Whisper large-v3, which Groq recommends for accurate multilingual work and which handles Arabic far better than the laptop's "small" model. Whisper can still write a mixed sentence entirely in one language. If Arabic is still poor, Soniox (`STT_ENGINE=soniox` plus `SONIOX_API_KEY`) is the next step up.

Whisper can occasionally invent a short line from background noise. The app drops the common ones ("Thank you for watching" and similar).

## Consent and data

In Qatar, recording a conversation in a private place without consent is an offence (Penal Code Article 333), and live transcription counts. Announce it and get a yes every time.

With Groq, each spoken line is sent to Groq's servers in the United States. Groq says it doesn't keep inference data by default, except logs kept up to 30 days when investigating errors or abuse; you can turn on Zero Data Retention in Groq's console under Settings, Data Controls. For work meetings, get your company's approval before sending meeting content to Groq and Anthropic.

## Files it writes

Each meeting gets a folder in `meetings/`, named by date and time:
- `transcript.txt`: everything it heard, with the time
- `suggestions.txt`: every suggestion it gave
- `brief.md`: the brief you used
- `summary.md`: the notes, if you chose to write them

`.env`, `brief.md`, `briefs/` and `meetings/` are in `.gitignore`, so your keys, briefs and transcripts never go to GitHub. On first run, `brief.md` is created from `brief.example.md`.

To write notes later for a saved meeting:
```
python copilot.py --summarize meetings/2026-11-02_140500
```

## Try it without a meeting

Double-click **Meeting Copilot (sample)** in this folder. It plays a sample Arabic and English meeting instead of using the mic. The sample has a launch date that contradicts the brief and a missing Arabic-support topic, so FLAG has something to catch. The same from a terminal:
```
python copilot.py --replay sample_meeting.txt --brief sample_brief.md
```

If the app ever fails to open from a shortcut, the reason is in `error.log` in this folder.

## Settings (`.env`)

| Setting | Default | What it does |
|---|---|---|
| `GROQ_API_KEY` | blank | Your Groq key. When set, Groq is the speech engine |
| `STT_ENGINE` | `groq` if a Groq key is set, else `whisper` | `groq`, `whisper` (on this laptop) or `soniox` (needs `SONIOX_API_KEY`) |
| `GROQ_MODEL` | `whisper-large-v3` | `whisper-large-v3-turbo` is a bit faster and less accurate |
| `WHISPER_MODEL` | `small` | Laptop model. `medium` is more accurate but falls behind on this laptop |
| `LANGUAGES` | `ar,en` | Languages spoken in the room |
| `OUTPUT_LANGUAGE` | `English` | Language of the suggestions and notes |
| `AUTO_NUDGE_SECONDS` | `45` | Minimum gap between automatic suggestions. `0` = only on F9 |
| `MIC_DEVICE` | Windows default | Microphone number from `--devices` |
| `HELP_HOTKEY`, `ME_HOTKEY`, `SPEECH_HOTKEY` | `<f9>`, `<f8>`, `<f10>` | Keys, in pynput format (e.g. `<ctrl>+<alt>+h`) |
| `CLAUDE_BACKEND` | blank | Blank = API if a key is set, else subscription. Force with `api` or `subscription` |
| `NUDGE_MODEL` | `claude-haiku-5-5` | Automatic suggestions (fast and cheap) |
| `HELP_MODEL` | `claude-sonnet-5-5` | F9 suggestions and F10 speech drafts |
| `SUMMARY_MODEL` | `claude-opus-5-5` | Meeting notes |

With an API key, the Sonnet and Opus calls have Claude's server-side fallback turned on: if a safety check wrongly declines a request, another model answers instead of you getting nothing.

## Cost and limits

- **Groq:** free tier. Groq's docs show limits of 20 requests a minute, 2 hours of audio an hour and 8 hours a day for its Whisper models, but label them as the Developer plan; your account's real limits are on console.groq.com under Settings, Limits. Each line counts as at least 10 seconds of audio, so short lines use the allowance faster. If the limit runs out mid-meeting, the app switches to Whisper on the laptop and says so. On the paid plan, large-v3 is listed at 0.111 USD per hour of audio.
- **Whisper on the laptop:** free.
- **Claude subscription:** no extra charge; calls count toward your plan's usage limits. Automatic suggestions use Haiku, which uses little of your limit. If you hit the limit mid-meeting, the window says so.
- **Claude API key:** Claude calls for a one-hour meeting at these settings come to well under 1 USD (rough estimate).
- **Soniox (optional):** bills per hour of audio; check their pricing page.

Subscription mode is for your own use on your own login. Anthropic doesn't allow apps that let other people sign in with their Claude subscription, so don't share it as a product.
