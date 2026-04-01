# Sparkle-Vault

**Axiom-Law Engine (ALE) - Legal Lie Detector**

Sparkle-Vault is a "Truth-as-a-Service" platform that uses AI to mathematically audit legal claims. It implements the Axiom-Based Engineering (ABE) framework to provide deterministic redress - if the evidence holds up, the system generates a court-ready proof certificate.

## Core Philosophy

- **No Artifact, No Fact**: Every claim must be backed by verifiable evidence
- **Zero Circular Logic**: DAG (Directed Acyclic Graph) ensures logical consistency
- **Skeptic-First**: The AI's job is to find Logic Leaks, not validate assumptions
- **Deterministic Outcomes**: Same evidence = Same verdict, every time

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   User      │────▶│   Nanobot    │────▶│   Skeptic   │
│   Claim     │     │   Scraper    │     │   Agent     │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                       ┌──────────────────────────┘
                       ▼
              ┌─────────────────┐
              │   Verifiable    │
              │   Fact Table    │
              │   (SQLite)      │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   DAG Logic     │
              │   Map           │
              │   (Mermaid.js)  │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Certificate    │
              │  of Deterministic│
              │  Proof (PDF)      │
              └─────────────────┘
```

## Tech Stack

| Component | Tool | Purpose |
|-----------|------|---------|
| Frontend | HTML + Tailwind CSS | Zero-setup UI |
| Backend | Python + Flask | API & routing |
| AI Brain | Gemini 1.5 Flash API | Skeptic Agent reasoning |
| Database | SQLite | Evidence locker (VFT) |
| Logic Map | Mermaid.js | DAG visualization |
| Reports | FPDF2 | PDF certificate generation |

## Quick Start

### 1. Clone & Setup

```bash
git clone <your-repo-url>
cd sparkle-vault
pip install -r requirements.txt
```

### 2. Configure Gemini API

Get a free API key from [Google AI Studio](https://aistudio.google.com):

```bash
export GEMINI_API_KEY="your_api_key_here"
```

Or edit line 16 in `app.py` and replace `YOUR_GEMINI_API_KEY_HERE`.

### 3. Run the App

```bash
python app.py
```

### 4. Open Browser

Navigate to: **http://localhost:5000**

## Testing with Demo Cases

The `demo/` folder contains 4 test scenarios:

1. **STRONG CASE** - Landlord deposit fraud (complete evidence chain)
2. **WEAK CASE** - Employment salary dispute (missing payslips)
3. **INSUFFICIENT EVIDENCE** - Business theft claim (no proof)
4. **LOGIC LEAK** - Contractor fraud (date paradox)

### Test Case 5: VERY STRONG CASE (Investment Fraud with Complete Documentation)

**Claim:**
```
I invested ₹5,00,000 with ABC Investment Company on March 1, 2023 through a registered broker Mr. Rajesh Kumar. The company promised 12% annual returns with monthly payouts. I received payments for 6 months (April-September 2023) totaling ₹30,000 as documented in my bank statements. From October 2023, all payments stopped. The company's office is now shut, phone disconnected, and the broker has disappeared. I have the original investment contract with company seal, broker's ID proof, all 6 months of payment receipts, bank transfer proof of initial investment, and an email from the company CEO dated August 2023 promising continued payments.
```

**Evidence to Upload:** Create a combined PDF with:
- Signed investment contract with company seal
- Broker's government ID photocopy
- 6 months of bank credit receipts (₹5,000 each month)
- Original bank transfer receipt for ₹5,00,000
- Email printout from CEO
- Recent photo of closed office

**Expected Verdict:** STRONG CASE (95%+ confidence)

**Why it should pass:**
- ✓ Original signed contract (Artifact #1)
- ✓ Broker identity verified (Artifact #2)
- ✓ Proof of initial payment (Artifact #3)
- ✓ 6 months of successful payouts proving business was operational (Artifacts #4-9)
- ✓ Written promise from CEO (Artifact #10)
- ✓ Proof of business closure (Artifact #11)
- ✓ Clear timeline with no temporal paradoxes
- ✓ All amounts balance (₹5L out, ₹30K returned, ₹4.7L outstanding)

This is the ideal case - complete documentation chain from investment to fraud.

See `demo/README.md` for claim text and expected verdicts.

## How It Works

1. **User submits claim** + evidence artifact
2. **Skeptic Agent** audits for:
   - Missing evidence (No Artifact = No Fact)
   - Temporal paradoxes (dates out of order)
   - Artifact mismatches (amounts don't balance)
   - Circular reasoning
3. **DAG Logic Map** renders the proof chain
4. **Verdict generated**: STRONG CASE / WEAK CASE / INSUFFICIENT EVIDENCE
5. **PDF Certificate** available for download

## Project Structure

```
sparkle-vault/
├── app.py                  # Flask backend + Skeptic Agent
├── requirements.txt        # Dependencies
├── sparkle_vault.db        # SQLite database (auto-created)
├── uploads/                # Evidence storage (auto-created)
├── templates/
│   ├── index.html          # Submission form
│   ├── result.html         # Analysis results
│   └── cases.html          # Case history
└── demo/
    ├── README.md           # Test case instructions
    ├── demo_evidence_landlord.txt
    ├── demo_evidence_employer.txt
    └── demo_evidence_contractor.txt
```

## GitHub Push Commands

### First Time Setup (if you haven't pushed before):

```bash
# 1. Initialize git (if not already done)
git init

# 2. Add all files
git add .

# 3. Commit with a message
git commit -m "Initial commit: Sparkle-Vault Axiom-Law Engine"

# 4. Create repository on GitHub (via web interface)
#    - Go to https://github.com/new
#    - Name: sparkle-vault
#    - Make it public or private
#    - Do NOT initialize with README (you already have one)
#    - Click "Create repository"

# 5. Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/sparkle-vault.git
git branch -M main
git push -u origin main
```

### For Subsequent Updates:

```bash
# Check what changed
git status

# Add specific files or all
git add app.py                    # Add specific file
git add .                         # Add all changes

# Commit the changes
git commit -m "Description of what you changed"

# Push to GitHub
git push origin main
```

### Useful Git Commands:

```bash
# Check commit history
git log --oneline

# See differences before committing
git diff

# Pull latest changes (if working on multiple machines)
git pull origin main

# Create a branch for experiments
git checkout -b experiment-branch

# Switch back to main
git checkout main
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google AI Studio API key | `YOUR_GEMINI_API_KEY_HERE` |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main submission form |
| `/submit` | POST | Submit case (claim + evidence) |
| `/download/<id>` | GET | Download PDF certificate |
| `/cases` | GET | View all case history |

## The Skeptic Prompt

The core intelligence is in the `SKEPTIC_PROMPT` (see `app.py` line 20). It instructs Gemini to:

- Be "clinical, stubborn, mathematically cold"
- Find Logic Leaks (temporal paradoxes, mismatches, circular loops)
- Never assume - require artifact IDs for every fact
- Output structured: VERIFIED FACTS → LOGIC LEAKS → VERDICT → CONFIDENCE

## Deployment Options

### Free Deployment on Render:
```bash
# 1. Create account at render.com
# 2. Click "New Web Service"
# 3. Connect your GitHub repo
# 4. Set build command: pip install -r requirements.txt
# 5. Set start command: gunicorn app:app
# 6. Add environment variable: GEMINI_API_KEY
# 7. Deploy (free tier available)
```

### Free Deployment on PythonAnywhere:
```bash
# 1. Create account at pythonanywhere.com
# 2. Open Bash console
# 3. git clone your repo
# 4. pip install -r requirements.txt
# 5. Go to Web tab, create Flask app
# 6. Point WSGI to your app.py
```

## License

MIT License - Feel free to use this for legal tech projects.

## Credits

- **Axiom-Based Engineering (ABE)** by the user
- **Gemini API** by Google
- **Flask, Tailwind, Mermaid.js** - Open source community

---

**Sparkle-Vault: Truth-as-a-Service**
