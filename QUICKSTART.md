# Sparkle-Vault Quick Reference

## Quick Commands (Copy-Paste Ready)

### Run the App
```bash
cd /home/sohail/sparkle-vault
export GEMINI_API_KEY="AIzaSyCUxhLxB8s919a0Gg1_gukqqXIrXtRzcmI"
python app.py
```

### Open in Browser
```
http://localhost:5000
```

---

## Demo Test Cases

### Test 1: STRONG CASE (Landlord)

**Claim:**
```
My landlord Mr. Sharma took a security deposit of ₹50,000 from me on January 15, 2024 when I signed the lease for apartment 302. I paid via bank transfer. I vacated the apartment on December 31, 2024 in good condition with no damages. The landlord promised to return the deposit within 15 days but has not returned it despite 3 months passing. I have the lease agreement, bank transfer receipt, and move-out inspection report showing no damages.
```

**Evidence:** Upload `demo/demo_evidence_landlord.txt`

**Expected:** STRONG CASE (90%+ confidence)

---

### Test 2: WEAK CASE (Employer)

**Claim:**
```
My employer owes me 3 months of unpaid salary totaling ₹1,50,000. I worked for TechCorp from March 2024 to June 2024. They stopped paying me in April. I have some emails where I asked about payment.
```

**Evidence:** Upload `demo/demo_evidence_employer.txt`

**Expected:** WEAK CASE (40-60% confidence)

---

### Test 3: INSUFFICIENT EVIDENCE

**Claim:**
```
My business partner stole money from our company bank account. He took out ₹2,00,000 without telling me. I know he did it because he was acting suspicious.
```

**Evidence:** None (or any random file)

**Expected:** INSUFFICIENT EVIDENCE (0-20% confidence)

---

### Test 4: LOGIC LEAK (Contractor Date Fraud)

**Claim:**
```
I paid my contractor ₹75,000 on January 10, 2024 for home renovation work. The contractor signed a completion certificate dated January 5, 2024 stating all work was done. The work was actually never completed and now the contractor has disappeared with my money.
```

**Evidence:** Upload `demo/demo_evidence_contractor.txt`

**Expected:** WEAK CASE / LOGIC LEAK (catches the Jan 5 vs Jan 10 date paradox)

---

## GitHub Push (One-Time Setup)

```bash
# 1. Check git status
git status

# 2. If not initialized:
git init

# 3. Add all files
git add .

# 4. Commit
git commit -m "Initial: Sparkle-Vault Axiom-Law Engine"

# 5. Create repo on https://github.com/new
#    Name: sparkle-vault
#    Don't initialize with README

# 6. Push
git remote add origin https://github.com/YOUR_USERNAME/sparkle-vault.git
git branch -M main
git push -u origin main
```

---

## API Test with curl

```bash
curl -X POST \
  -F "claim=My landlord stole my deposit of 50000" \
  -F "evidence=@demo/demo_evidence_landlord.txt" \
  http://localhost:5000/submit
```

---

## File Locations

| File | Path |
|------|------|
| Main app | `/home/sohail/sparkle-vault/app.py` |
| Homepage | `/home/sohail/sparkle-vault/templates/index.html` |
| Results page | `/home/sohail/sparkle-vault/templates/result.html` |
| Demo tests | `/home/sohail/sparkle-vault/demo/README.md` |
| Database | `/home/sohail/sparkle-vault/sparkle_vault.db` |
| Uploads | `/home/sohail/sparkle-vault/uploads/` |
| PDF Reports | Current directory (proof_report_*.pdf) |

---

## What to Expect

### STRONG CASE (Green)
- All evidence chain complete
- No logic leaks
- 80-100% confidence
- PDF ready for court

### WEAK CASE (Yellow)
- Some evidence missing
- Logic leaks detected
- 40-70% confidence
- Shows what's needed to fix

### INSUFFICIENT EVIDENCE (Red)
- Missing critical evidence
- Too many logic leaks
- 0-30% confidence
- Needs more proof
