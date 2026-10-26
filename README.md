# Voxora

**Your Voice. Your Workflow.**

> **Voxora** is a multilingual, voice-enabled desktop productivity assistant designed to help users manage tasks, find files, set reminders, and control supported laptop functions through an AI-powered workflow.

Dial your dedicated phone number, speak in Hindi, English, Telugu, or any natural mix, and your laptop executes your commands in real time. And when a deadline is imminent or your battery is critically low, Voxora phones you.

```
                 ┌─────────── You dial Voxora ───────────┐
Your Phone ◀────▶ Sarvam Phone Line ◀──▶ Sarvam Voice Agent (Saaras · Sarvam-105B · Bulbul)
     ▲                                            │ HTTPS tool call: Bearer token + Caller Hash
     │                                            ▼
     │                      cloudflared tunnel ──▶ server.js on your laptop ──▶ 22 Safe Actions
     │                                                     │
     └──── Voxora calls you (Sarvam Outbounds) ◀───────────┤ monitor: Deadlines, Battery, Focus Timer
                                                           └─▶ Voxora Console (http://localhost:3710)
```

---

## Key Capabilities

### 1. Document & File Discovery ("Find My File")
- *"Mera EM5120 assignment kholo"* / *"Find project proposal PDF"*
- Voxora searches your local `Desktop`, `Documents`, `Downloads`, `OneDrive`, and `Pictures` directories.
- Course codes and keywords are verified with intelligent ranking, matching course codes (e.g. `EM5120` will never match an unrelated report).
- The index of over 7,000+ documents updates incrementally in the background and is instantly searchable via voice or the Voxora web dashboard.

### 2. Focus Sessions & Deep Work Sprints
- *"25 minute focus session for my DBMS assignment"*
- Automatically opens matching reference materials or documents on your laptop.
- Launches ambient focus music (YouTube Lo-Fi stream) and starts the session timer.
- Announces completion over laptop speakers and triggers an urgent phone follow-up when the session concludes.

### 3. Automated Deadlines & Proactive Voice Calls
- *"Remind me, DBMS project due tomorrow 5 pm"*
- Stored safely in local persistent storage (`deadlines.json`).
- Voxora phones you through Sarvam's Outbound Call API at strategic intervals:
  - 24 hours, 3 hours, 1 hour, and 15 minutes before due time.
  - At the due moment if the assignment is still unsubmitted.
  - When your laptop unplugged battery drops below 15%.
- Say *"Submitted"* or click "✓ Submitted" on the dashboard to cancel subsequent reminders.
- **Safety guardrails**: Rate-limited to max 1 call per 10 minutes, max 8 calls per day, with quiet hours strictly enforced between 11 PM and 7 AM unless due within 2 hours.

---

## Voice Commands Reference

| What You Say | What Voxora Does |
|---|---|
| *"Mera EM5120 assignment kholo"* | Finds and opens matching document with default viewer |
| *"25 minute focus session for my assignment"* | Opens document, plays focus stream, tracks session, and calls you |
| *"Remind me, DBMS project due tomorrow 5 pm"* | Creates a tracked deadline and schedules phone reminders |
| *"What's due?"* / *"DBMS submitted"* | Spoken summary of pending deadlines / marks deadline finished |
| *"YouTube pe Arijit Singh ke gaane chalao"* | Searches and launches song on YouTube |
| *"IRCTC kholo"* / *"open Gmail"* | Safely opens the designated website |
| *"Work mode on karo"* | Launches VS Code, Gmail, and Google Calendar |
| *"5 minute ka timer lagao chai ke liye"* | Sets a timer announced out loud via laptop speakers |
| *"Laptop se bolo, hello team"* | Windows text-to-speech speaks the sentence |
| *"Volume kam karo"* / *"next song"* | Media key controls (volume up/down, mute, play/pause, skip) |
| *"Take a screenshot"* | Captures entire virtual screen to `Pictures/Jarvis` |
| *"Draft an email to … about …"* | Pre-populates Gmail draft (never sends automatically) |
| *"Directions to Charminar"* / *"weather in Hyderabad"* | Opens Google Maps / Google Weather |
| *"Note karo …"* / *"mere notes padho"* | Appends timestamped note to `Documents/Jarvis Notes.md` / reads aloud |
| *"Battery kitni hai?"* | Checks CIM battery percentage, charging state, date & time |
| *"Lock my laptop"* | Prompts for confirmation, then safely invokes Windows screen lock |

---

## Security & Safety Model

Running an agent that can interact with your desktop requires strict isolation:

- **Strict Allowlist of 22 Fixed Actions**: No arbitrary terminal/shell access. Callers cannot pass commands, execute scripts, or delete files.
- **Document-Only Indexing**: The file index strictly includes documents and media (`.pdf`, `.docx`, `.pptx`, `.xlsx`, `.txt`, `.md`, `.png`, `.jpg`). Executables, scripts (`.exe`, `.bat`, `.ps1`, `.sh`), and binaries are excluded.
- **Command Injection Prevention**: Text passed to PowerShell (spoken sentences, file paths) travels solely in sanitized environment variables, never interpolated in execution strings.
- **Constant-Time Bearer Token Auth**: Inbound requests from the Sarvam Voice Agent require a secret `JARVIS_TOKEN` matched via `crypto.timingSafeEqual`.
- **Owner Caller-ID Lockdown**: The server verifies the incoming caller against the owner's phone number or hashed caller ID. Non-owner callers are refused with HTTP 401.
- **Local Console Isolation**: Dashboard and local management endpoints (`/monitor/*`, `/api/*`) verify that incoming requests are not arriving from the public Cloudflare tunnel (`cf-connecting-ip` check). The public tunnel exposes only `/action` and `/tools/*`.
- **Burst De-duplication**: Repeated requests within 10 seconds are de-duplicated to prevent double actions during conversational bursts.

---

## Installation & Setup

### Prerequisites
- Windows 10/11
- Node.js 18+
- [Cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) (for exposing the webhook to Sarvam)

### Step 1: Clone & Configure
```bash
# Navigate to directory
cd arrc

# Copy sample configuration
cp .env.example .env
```

Edit `.env`:
```env
PORT=3710
JARVIS_TOKEN=your_random_secret_token_here
OWNER_NUMBER=919876543210
ALLOW_NO_CALLER=true
JARVIS_PHONE=+91XXXXXXXXXX
```

### Step 2: Start Voxora Server
```bash
npm start
# or: node server.js
```
The server will start on `http://localhost:3710`.

### Step 3: Start Cloudflare Tunnel
```bash
cloudflared tunnel --url http://localhost:3710
```
Copy the printed `https://<random>.trycloudflare.com` address. This is your public webhook URL for the Sarvam agent tools.

### Step 4: Open the Voxora Dashboard
Open `http://localhost:3710` in any web browser to view the Voxora console:
- **Dashboard**: System telemetry, owner lock status, quick action buttons, and live engine status.
- **File Finder**: Search 7,000+ local documents with category filters and 1-click open.
- **Focus Sessions**: Interactive Pomodoro timer with ambient music and speech completion.
- **Reminders**: Visual deadline manager with "Mark Submitted" and urgent call testing.
- **Activity Log**: Real-time event audit feed with success/refused filtering.
- **Settings**: Configuration inspection with zero secret leakage.

For configuring the Sarvam AI Voice Agent (Saaras, Sarvam-105B, Bulbul), refer to [AGENT-SETUP.md](AGENT-SETUP.md).

---

## Configuration Requirements & Integrations

| Feature | Requirement | Fallback / Behavior if Missing |
|---|---|---|
| **Local Dashboard & Actions** | None (Node.js built-ins) | Always active on `http://localhost:3710` |
| **File Search & Open** | Local Desktop/Documents/Downloads | Uses cached file index from local directories |
| **Voice Inbound Agent** | Sarvam Voice Agent + `cloudflared` | Dashboard can still test actions locally |
| **Outbound Urgent Phone Calls** | `SARVAM_WORKSPACE_KEY`, `SARVAM_ORG_ID`, `SARVAM_WORKSPACE_ID`, `ARRC_APP_ID` in `.env` | Operates in **Dry-Run Mode**; logs simulated calls safely without dialing |
| **Owner Verification** | `OWNER_NUMBER` in `.env` | If left empty, allows local/test calls |

---

## Known Limitations

1. **Operating System**: Laptop actions utilize native Windows utilities (`powershell.exe`, `explorer.exe`, `taskmgr.exe`, `rundll32.exe`). Running on macOS or Linux requires platform-specific action handlers.
2. **Dynamic Quick Tunnel Addresses**: Cloudflare quick tunnels generate a new hostname when restarted; use a named Cloudflare tunnel or fixed domain for permanent deployments.
3. **Outbound Calling Quota**: Sarvam outbound calls are rate-limited to avoid excessive dialing (max 8 per day, quiet hours 11 PM to 7 AM).
4. **Email Drafting**: Gmail actions open a draft composer window in the browser. Out of safety, emails are never dispatched automatically.

---

## Historical Attribution & License

- **Current Application**: Voxora ("Your Voice. Your Workflow.")
- **Upstream Project & Origin**: Originally designed and created as **ARRC** for the **Sarvam AI Hackathon, October 2026**.
- **Authorship**: All original upstream architecture, prompts, and safety design are preserved under the original project attribution.
- **License**: MIT License. See project files for details.
