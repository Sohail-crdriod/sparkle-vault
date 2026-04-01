from flask import Flask, request, render_template, send_file, jsonify, redirect
import sqlite3
import os
from datetime import datetime
from fpdf import FPDF
from dotenv import load_dotenv
import requests
import json

# Load environment variables from .env file
load_dotenv()

# Get the directory containing this file for Vercel compatibility
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'templates')

# Vercel only allows writing to /tmp, so use that for uploads and database
IS_VERCEL = os.environ.get('VERCEL') == '1'
if IS_VERCEL:
    UPLOAD_DIR = '/tmp/uploads'
    DB_PATH = '/tmp/sparkle_vault.db'
else:
    UPLOAD_DIR = os.path.join(BASE_DIR, '..', 'uploads')
    DB_PATH = os.path.join(BASE_DIR, '..', 'sparkle_vault.db')

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if it doesn't exist (use /tmp on Vercel)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize OpenRouter API from environment variable
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY') or 'sk-or-v1-'  # User needs to add their key
if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == 'sk-or-v1-':
    print("WARNING: OPENROUTER_API_KEY not set. Get free key at https://openrouter.ai/keys")
    print("Set the key with: export OPENROUTER_API_KEY='your_key_here'")
else:
    print(f"✓ OpenRouter API configured successfully")

# Skeptic Agent Prompt
SKEPTIC_PROMPT = """You are the "Skeptic" - a legal auditor in a high-stakes detective game. Your ONLY job is to find Logic Leaks.

THE RULES (Axiom-Law Engine):
1. If a claim has no supporting evidence/artifact, it's UNVERIFIED
2. If dates don't match chronologically, it's a TEMPORAL PARADOX
3. If amounts don't balance (inflow vs outflow), it's an ARTIFACT MISMATCH
4. If reasoning is circular, it's a LOGIC LOOP

USER CLAIM: {claim}
EVIDENCE PROVIDED: {evidence_description}

AUDIT THE FOLLOWING:
- What facts can be verified from the evidence?
- What temporal paradoxes exist? (dates out of order)
- What artifact mismatches exist? (amounts, signatures)
- What evidence is missing to complete the proof?

OUTPUT FORMAT (be clinical, stubborn, mathematically cold):

VERIFIED FACTS:
- List each verifiable fact with its supporting evidence

LOGIC LEAKS:
- [Leak Type]: Description of the hole
- [Axiom Violated]: Which rule was broken
- [Required Artifact]: What evidence is needed to fix this

VERDICT: STRONG CASE / WEAK CASE / INSUFFICIENT EVIDENCE

CONFIDENCE SCORE: X%

DAG LOGIC MAP (Mermaid format):
Describe the proof chain as nodes and edges (e.g., A[Claim] --> B[Evidence1] --> C[Conclusion])
"""

# Database initialization
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            claim TEXT NOT NULL,
            evidence_path TEXT,
            verdict TEXT,
            confidence_score INTEGER,
            verified_facts TEXT,
            logic_leaks TEXT,
            dag_map TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'PENDING'
        )
    ''')
    conn.commit()
    conn.close()

def save_case(claim, evidence_path, verdict, confidence, verified_facts, logic_leaks, dag_map):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cases (claim, evidence_path, verdict, confidence_score, verified_facts, logic_leaks, dag_map, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (claim, evidence_path, verdict, confidence, verified_facts, logic_leaks, dag_map, 'VERIFIED' if verdict == 'STRONG CASE' else 'PENDING'))
    case_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return case_id

def analyze_with_gemini(claim, evidence_description):
    """Send claim to OpenRouter API for analysis (free tier, no quota limits)"""
    api_key = os.environ.get('OPENROUTER_API_KEY')
    
    if not api_key or api_key == 'sk-or-v1-your-key-here':
        return f"""VERIFIED FACTS:
- Claim submitted: {claim}
- Evidence attached: {evidence_description}

LOGIC LEAKS:
- [API ERROR]: OPENROUTER_API_KEY not set. Get free key at https://openrouter.ai/keys
- [Axiom Violated]: Rule 1 - No AI verification performed

VERDICT: INSUFFICIENT EVIDENCE (Manual Review Required)

CONFIDENCE SCORE: 0%

DAG LOGIC MAP:
A[User Claim] --> B[Evidence Submitted] --> C[AI Verification Failed] --> D[Manual Review Required]
"""
    
    try:
        prompt = SKEPTIC_PROMPT.format(claim=claim, evidence_description=evidence_description)
        
        print(f"Sending request to OpenRouter API...")
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5000",
                "X-Title": "Sparkle-Vault"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=60
        )
        
        print(f"API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✓ AI analysis successful")
            return result['choices'][0]['message']['content']
        else:
            error_msg = f"OpenRouter API Error {response.status_code}: {response.text}"
            print(f"✗ {error_msg}")
            return f"""VERIFIED FACTS:
- Claim submitted: {claim}
- Evidence attached: {evidence_description}

LOGIC LEAKS:
- [API ERROR]: {error_msg}
- [Axiom Violated]: Rule 1 - AI verification failed

VERDICT: INSUFFICIENT EVIDENCE (Manual Review Required)

CONFIDENCE SCORE: 0%

DAG LOGIC MAP:
A[User Claim] --> B[Evidence Submitted] --> C[API Error] --> D[Manual Review Required]
"""
    except Exception as e:
        error_msg = f"Exception during API call: {str(e)}"
        print(f"✗ {error_msg}")
        return f"""VERIFIED FACTS:
- Claim submitted: {claim}
- Evidence attached: {evidence_description}

LOGIC LEAKS:
- [API ERROR]: {error_msg}
- [Axiom Violated]: Rule 1 - AI verification failed

VERDICT: INSUFFICIENT EVIDENCE (Manual Review Required)

CONFIDENCE SCORE: 0%

DAG LOGIC MAP:
A[User Claim] --> B[Evidence Submitted] --> C[API Error] --> D[Manual Review Required]
"""


def generate_mock_analysis(claim, evidence_description):
    """Generate a realistic mock analysis for demo/testing purposes"""
    
    # Detect keywords to customize response
    claim_lower = claim.lower()
    
    if 'landlord' in claim_lower or 'deposit' in claim_lower or 'rent' in claim_lower:
        verdict = "STRONG CASE"
        confidence = 85
        verified_facts = """- Security deposit of ₹50,000 was paid on January 15, 2024 (per claim)
- Lease agreement for apartment 302 was signed (per claim)
- Tenant vacated property on December 31, 2024 (per claim)
- Move-out inspection showed no damages (per claim)
- 75+ days have passed without deposit refund (per claim)"""
        logic_leaks = """- [MINOR]: No uploaded artifact was analyzed - relying on user statement only
- [Axiom Note]: Rule 1 partially satisfied - claim exists but physical evidence not verified by AI"""
        dag_map = "A[Claim: Deposit Stolen] --> B[Lease Signed Jan 15] --> C[Payment Made ₹50K] --> D[Vacated Dec 31] --> E[No Refund After 75 Days] --> F[VERDICT: STRONG CASE]"
        
    elif 'employer' in claim_lower or 'salary' in claim_lower or 'unpaid' in claim_lower:
        verdict = "WEAK CASE"
        confidence = 45
        verified_facts = """- Employment at TechCorp from March-June 2024 (per claim)
- Salary payment issues acknowledged in emails (per claim)
- Total claimed amount: ₹1,50,000 (per claim)"""
        logic_leaks = """- [MAJOR]: No salary slips or bank statements provided to verify amounts
- [MAJOR]: No employment contract or offer letter uploaded
- [TEMPORAL]: Cannot verify exact dates of unpaid periods
- [Axiom Violated]: Rule 1 - Insufficient artifact evidence
- [Required Artifact]: Salary slips, bank statements, employment contract"""
        dag_map = "A[Claim: Unpaid Salary] --> B[Employment Claimed] --> C{Evidence?} --> D[Emails Only - Weak] --> E[VERDICT: WEAK CASE]"
        
    elif 'contractor' in claim_lower or 'renovation' in claim_lower:
        verdict = "WEAK CASE"
        confidence = 35
        verified_facts = """- Payment of ₹75,000 made to contractor (per claim)
- Completion certificate exists (per claim)
- Complaint emails sent (per claim)"""
        logic_leaks = """- [TEMPORAL PARADOX]: Completion certificate dated Jan 5, payment dated Jan 10
- [MAJOR]: Certificate signed BEFORE payment - suggests backdating/fraud
- [Axiom Violated]: Rule 2 - Dates don't match chronologically
- [Required Artifact]: Corrected completion certificate with accurate dates"""
        dag_map = "A[Claim: Contractor Fraud] --> B[Certificate Jan 5] --> C[Payment Jan 10] --> D{Date Mismatch!} --> E[TEMPORAL PARADOX] --> F[VERDICT: WEAK CASE]"
        
    else:
        verdict = "INSUFFICIENT EVIDENCE"
        confidence = 20
        verified_facts = f"""- Claim submitted: {claim[:100]}...
- Evidence description: {evidence_description}"""
        logic_leaks = """- [MAJOR]: No specific evidence artifacts uploaded
- [MAJOR]: Claim lacks verifiable documentation
- [Axiom Violated]: Rule 1 - No artifact = no fact
- [Required Artifact]: Upload receipts, contracts, photos, or official documents"""
        dag_map = "A[User Claim] --> B{Evidence?} --> C[None Found] --> D[VERDICT: INSUFFICIENT EVIDENCE]"
    
    return f"""VERIFIED FACTS:
{verified_facts}

LOGIC LEAKS:
{logic_leaks}

VERDICT: {verdict}

CONFIDENCE SCORE: {confidence}%

DAG LOGIC MAP:
{dag_map}

---
[NOTE: Running in DEMO MODE - Add valid OPENROUTER_API_KEY for real AI analysis]
"""

def parse_analysis(analysis_text):
    """Parse the AI analysis into structured components"""
    lines = analysis_text.split('\n')
    
    verified_facts = []
    logic_leaks = []
    verdict = "INSUFFICIENT EVIDENCE"
    confidence = 0
    dag_map = ""
    
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('VERIFIED FACTS:'):
            current_section = 'facts'
        elif line.startswith('LOGIC LEAKS:'):
            current_section = 'leaks'
        elif line.startswith('VERDICT:'):
            verdict = line.replace('VERDICT:', '').strip()
        elif line.startswith('CONFIDENCE SCORE:'):
            try:
                confidence = int(line.split(':')[1].strip().replace('%', ''))
            except:
                confidence = 0
        elif line.startswith('DAG LOGIC MAP:'):
            current_section = 'dag'
        elif line.startswith('A[') or line.startswith('graph'):
            dag_map = line
        elif current_section == 'facts' and line.startswith('-'):
            verified_facts.append(line[1:].strip())
        elif current_section == 'leaks' and line.startswith('-'):
            logic_leaks.append(line[1:].strip())
    
    return {
        'verified_facts': verified_facts,
        'logic_leaks': logic_leaks,
        'verdict': verdict,
        'confidence': confidence,
        'dag_map': dag_map if dag_map else "A[Claim] --> B[Evidence] --> C[Analysis]"
    }

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'SPARKLE-VAULT', 0, 1, 'C')
        self.set_font('Arial', '', 12)
        self.cell(0, 10, 'Certificate of Deterministic Proof', 0, 1, 'C')
        self.ln(10)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 0, 'C')

def sanitize_for_pdf(text):
    """Replace Unicode characters with ASCII equivalents for PDF compatibility"""
    if not text:
        return text
    # Replace Indian Rupee symbol
    text = text.replace('₹', 'Rs.')
    # Replace other common Unicode currency symbols
    text = text.replace('€', 'EUR')
    text = text.replace('£', 'GBP')
    text = text.replace('¥', 'JPY')
    text = text.replace('₹', 'INR')
    return text

def generate_pdf(case_id, claim, verdict, confidence, verified_facts, logic_leaks):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    
    # Sanitize all text for PDF
    claim = sanitize_for_pdf(claim) if claim else ""
    verdict = sanitize_for_pdf(verdict) if verdict else "INSUFFICIENT EVIDENCE"
    verified_facts = [sanitize_for_pdf(f) for f in verified_facts if f and f.strip()]
    logic_leaks = [sanitize_for_pdf(l) for l in logic_leaks if l and l.strip()]
    
    # Page width for multi_cell (accounting for margins)
    page_width = pdf.w - 2 * pdf.l_margin
    
    # Case Info
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'CASE DETAILS', 0, 1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Case ID: #{case_id}', 0, 1)
    
    # Handle claim text - truncate if too long and use multi_cell
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, 'Claim:', 0, 1)
    pdf.set_font('Arial', '', 11)
    if len(claim) > 200:
        claim = claim[:197] + "..."
    pdf.multi_cell(page_width, 8, claim)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Verdict: {verdict}', 0, 1)
    pdf.cell(0, 10, f'Confidence Score: {confidence}%', 0, 1)
    pdf.ln(5)
    
    # Verified Facts
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'VERIFIED FACTS', 0, 1)
    pdf.set_font('Arial', '', 11)
    if verified_facts:
        for fact in verified_facts[:10]:  # Limit to 10 facts
            if fact.strip():
                pdf.multi_cell(page_width, 8, f'  {fact}')
    else:
        pdf.cell(0, 8, '  No verified facts', 0, 1)
    pdf.ln(5)
    
    # Logic Leaks
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'LOGIC LEAKS (IF ANY)', 0, 1)
    pdf.set_font('Arial', '', 11)
    if logic_leaks:
        for leak in logic_leaks[:10]:  # Limit to 10 leaks
            if leak.strip():
                pdf.multi_cell(page_width, 8, f'  {leak}')
    else:
        pdf.cell(0, 8, '  None - All axioms satisfied', 0, 1)
    
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 9)
    disclaimer = 'This document was generated by Sparkle-Vault Axiom-Law Engine. It represents a mathematical analysis of the evidence provided and should be reviewed by a legal professional.'
    pdf.multi_cell(page_width, 6, disclaimer)
    
    filename = f'proof_report_{case_id}.pdf'
    pdf.output(filename)
    return filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_case():
    claim = request.form.get('claim', '')
    evidence = request.files.get('evidence')
    
    if not claim:
        return jsonify({'error': 'Claim is required'}), 400
    
    # Save evidence file if provided
    evidence_path = None
    evidence_description = "No evidence uploaded"
    if evidence and evidence.filename:
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{evidence.filename}"
        evidence_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        evidence.save(evidence_path)
        evidence_description = f"Evidence file: {evidence.filename}"
    
    # Analyze with Gemini
    analysis_text = analyze_with_gemini(claim, evidence_description)
    parsed = parse_analysis(analysis_text)
    
    # Save to database
    case_id = save_case(
        claim=claim,
        evidence_path=evidence_path,
        verdict=parsed['verdict'],
        confidence=parsed['confidence'],
        verified_facts='\n'.join(parsed['verified_facts']),
        logic_leaks='\n'.join(parsed['logic_leaks']),
        dag_map=parsed['dag_map']
    )
    
    return render_template('result.html',
                         case_id=case_id,
                         claim=claim,
                         verdict=parsed['verdict'],
                         confidence=parsed['confidence'],
                         verified_facts=parsed['verified_facts'],
                         logic_leaks=parsed['logic_leaks'],
                         dag_map=parsed['dag_map'],
                         analysis_text=analysis_text)

@app.route('/download/<int:case_id>')
def download_report(case_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute('SELECT * FROM cases WHERE id = ?', (case_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return "Case not found", 404
    
    verified_facts = row[5].split('\n') if row[5] else []
    logic_leaks = row[6].split('\n') if row[6] else []
    
    pdf_path = generate_pdf(case_id, row[1], row[3], row[4], verified_facts, logic_leaks)
    return send_file(pdf_path, as_attachment=True, download_name=f'proof_report_case_{case_id}.pdf')

@app.route('/cases')
def list_cases():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute('SELECT id, claim, verdict, confidence_score, timestamp, status FROM cases ORDER BY timestamp DESC')
    cases = cursor.fetchall()
    conn.close()
    return render_template('cases.html', cases=cases)

@app.route('/delete/<int:case_id>', methods=['POST'])
def delete_case(case_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('DELETE FROM cases WHERE id = ?', (case_id,))
    conn.commit()
    conn.close()
    return redirect('/cases')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)

# Initialize DB on module load for serverless
init_db()
