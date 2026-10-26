# Voxora: Sarvam Voice Agent Setup

**Your Voice. Your Workflow.**

Set up a Sarvam Voice Agent that answers an Indian phone line (via Vobiz), accepts commands in Hindi, English, Telugu or a mix, and executes workflows on your laptop through Voxora.

```
Your phone ──call──▶ Sarvam phone number ──▶ Sarvam Voice Agent
                                              Saaras listens · Sarvam-105B decides · Bulbul speaks
                                                     │ HTTPS tool call (Bearer token + caller hash)
                                                     ▼
                                cloudflared tunnel ──▶ Voxora server.js on the laptop
                                                        fixed allowlist of 22 actions, console at :3710
```

---

## 1. Run the Laptop Side

```bash
# In the project directory
node server.js
```

In a separate terminal:
```bash
cloudflared tunnel --url http://localhost:3710
```

`cloudflared` prints a `https://<random>.trycloudflare.com` address. This is your `TUNNEL` URL below.
Open `http://localhost:3710` to view the **Voxora Dashboard**.

Before going live, set `OWNER_NUMBER` in `.env` to your mobile number (e.g. `919876543210`). Calls from other numbers will be refused with "Not authorised."

---

## 2. Agent Setup (indus.sarvam.ai → Build → Agents → Create from Scratch)

**Name:** `Voxora`

**Greeting:** `Hi, Voxora here. What should I do on your laptop?`

**Settings → Language personalisation:**
- Starting language: English
- *Switch language during call*: **ON**
- Allowed languages: Hindi, English, Telugu, Tamil, Kannada, Marathi, Bengali, Gujarati

**Instructions (system prompt):**

```
You are Voxora, an AI productivity assistant that controls the owner's laptop over a phone call.
The owner speaks Hindi, English, Telugu or a mix. Always reply in the language they used last, in short, clear spoken sentences.

You can do ONLY these actions, each through its corresponding tool:
- open_website: open a website by name or URL (YouTube, Gmail, IRCTC, LinkedIn, GitHub, etc.)
- web_search: search Google on the laptop and show the results on screen
- play_youtube: play a song or video on YouTube
- open_app: open an application (notepad, calculator, chrome, vs code, file explorer, downloads, paint, camera, settings, task manager, word, excel, powerpoint)
- find_file: search documents and open the matching file (PDFs, Word docs, spreadsheets, slides, notes)
- focus_session: start a focus session with topic, timer, and ambient focus music
- add_deadline: set a deadline or reminder for an assignment or project
- list_deadlines: tell the owner what deadlines are pending
- finish_deadline: mark a deadline as submitted or completed
- take_note: write down a note the owner dictates
- read_notes: read the owner's recent notes aloud
- show_notes: open the notes document in Notepad
- system_status: tell the current time, date, and laptop battery level
- lock_screen: lock the laptop screen. Always ask for confirmation first ("Should I lock your screen?") and execute only after a clear affirmative.
- media_control: play/pause, volume up/down, mute, next/previous track
- run_routine: activate work mode, study mode, chill mode, news mode, or demo mode

Rules:
- When the owner asks for a supported action, call the tool immediately.
- Pass the owner's words for the item to open, search, play or note as the tool input (translated to English if it is a search or title).
- Confirm the action only after the tool returns its response. Speak the tool result in the owner's language.
- If the tool responds with "Not authorised", reply: "Sorry, I can only take orders from my owner's phone." and end the call.
- If asked to perform unsupported tasks (sending money, deleting files, running terminal scripts), politely state that Voxora cannot do that yet.
- Keep every voice reply under two spoken sentences. Avoid markdown or bulleted lists.
```

---

## 3. Tools Setup (indus.sarvam.ai → Build → Tools → API tool)

Create API tools for the actions you wish to expose.

Common configuration for every tool:
- **Method:** `POST`
- **URL:** `<TUNNEL>/tools/<tool_name>` (e.g. `https://xyz-def.trycloudflare.com/tools/find_file`)
- **Auth:** `Bearer Token` (value matches `JARVIS_TOKEN` in your `.env`)
- **Headers:** `Content-Type: application/json`
- **Body:** `{"input": "<what the owner asked for>", "caller": "@User Identifier"}` (type `@` and select *User Identifier*)
- **Response template:** `{{result}}`
- **Max wait:** `10s`
- **Error message:** `Sorry, I couldn't reach your laptop.`

### Core Tool Allowlist

| Tool Name | Tool Description (for LLM) | Input Field |
|---|---|---|
| `find_file` | Find and open a file on the laptop. Input: document or assignment name. | file name / query |
| `focus_session` | Start a focus session. Input: duration in minutes and topic. | duration and topic |
| `add_deadline` | Add a deadline or reminder. Input: title and due time separated by pipe, e.g. "DBMS project \| tomorrow 5 pm". | title and time |
| `list_deadlines` | List pending deadlines and due dates. | none |
| `finish_deadline` | Mark a deadline submitted. Input: deadline title or id. | title |
| `open_website` | Open a website by name or URL. | site name or URL |
| `web_search` | Search Google and show results on screen. | search query |
| `play_youtube` | Play song or video on YouTube. | song / video query |
| `open_app` | Open a desktop application. | app name |
| `take_note` | Append a timestamped note to notes file. | note text |
| `read_notes` | Read recent notes aloud. | none |
| `show_notes` | Open the notes file on the laptop screen. | none |
| `system_status` | Check laptop battery, charging state, date and time. | none |
| `lock_screen` | Secure and lock the Windows session. | none |
| `media_control` | Control volume or playback (play, pause, next, volume up). | media command |
| `run_routine` | Run a preconfigured routine (work, study, chill, news). | mode name |

---

## 4. Deploy Phone Number

1. Go to **Deploy → Phone Numbers** in the Indus console.
2. Select your rented Sarvam Vobiz phone number.
3. Under **Inbound Calls**, assign the number to **Voxora**.
4. Call your number from your registered phone.

---

## Attribution

Originally designed as the ARRC project for the Sarvam AI Hackathon, October 2026. Preserved and updated for Voxora.
