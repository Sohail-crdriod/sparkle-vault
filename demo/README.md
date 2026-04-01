# Sparkle-Vault Demo Test Cases

## Test Case 1: STRONG CASE (Landlord Deposit Fraud)

### Claim Text (copy-paste this):
```
My landlord Mr. Sharma took a security deposit of ₹50,000 from me on January 15, 2024 when I signed the lease for apartment 302. I paid via bank transfer. I vacated the apartment on December 31, 2024 in good condition with no damages. The landlord promised to return the deposit within 15 days but has not returned it despite 3 months passing. I have the lease agreement, bank transfer receipt, and move-out inspection report showing no damages.
```

### Evidence to Upload:
- Use: `demo_evidence_landlord.pdf` (in this folder)
- Or: Any screenshot of a fake bank transfer

### Expected Verdict: STRONG CASE
### Why: Complete evidence chain - lease → payment → move-out → missing refund

---

## Test Case 2: WEAK CASE (Missing Timeline)

### Claim Text (copy-paste this):
```
My employer owes me 3 months of unpaid salary totaling ₹1,50,000. I worked for TechCorp from March 2024 to June 2024. They stopped paying me in April. I have some emails where I asked about payment.
```

### Evidence to Upload:
- Use: `demo_evidence_employer.pdf` (in this folder)
- Or: Any screenshot of text file

### Expected Verdict: WEAK CASE
### Why: No salary slips, no termination letter, emails don't prove amount owed

---

## Test Case 3: INSUFFICIENT EVIDENCE (No Proof)

### Claim Text (copy-paste this):
```
My business partner stole money from our company bank account. He took out ₹2,00,000 without telling me. I know he did it because he was acting suspicious.
```

### Evidence to Upload:
- None (or upload a random photo)

### Expected Verdict: INSUFFICIENT EVIDENCE
### Why: Suspicion is not evidence. No bank records, no proof of unauthorized withdrawal

---

## Test Case 4: LOGIC LEAK (Date Problem)

### Claim Text (copy-paste this):
```
I paid my contractor ₹75,000 on January 10, 2024 for home renovation work. The contractor signed a completion certificate dated January 5, 2024 stating all work was done. The work was actually never completed and now the contractor has disappeared with my money.
```

### Evidence to Upload:
- Use: `demo_evidence_contractor.txt` (in this folder)

### Expected Verdict: WEAK CASE / LOGIC LEAK
### Why: Temporal Paradox - completion certificate dated BEFORE payment date

---

## Test Case 5: VERY STRONG CASE (Investment Fraud with Complete Documentation)

### Claim Text (copy-paste this):
```
I invested ₹5,00,000 with ABC Investment Company on March 1, 2023 through a registered broker Mr. Rajesh Kumar. The company promised 12% annual returns with monthly payouts. I received payments for 6 months (April-September 2023) totaling ₹30,000 as documented in my bank statements. From October 2023, all payments stopped. The company's office is now shut, phone disconnected, and the broker has disappeared. I have the original investment contract with company seal, broker's ID proof, all 6 months of payment receipts, bank transfer proof of initial investment, and an email from the company CEO dated August 2023 promising continued payments.
```

### Evidence to Upload:
- Use: `demo_evidence_investment.txt` (in this folder) - contains all supporting documents
- Documents included:
  - Investment contract with company seal (Artifact #1)
  - Broker's government ID proof (Artifact #2)
  - Bank transfer receipt for ₹5,00,000 (Artifact #3)
  - 6 months of payment receipts (Artifacts #4-9)
  - CEO email promising payments (Artifact #10)
  - Photo of closed office (Artifact #11)

### Expected Verdict: STRONG CASE (95%+ confidence)

### Why it should pass:
- ✓ Complete documentation chain from investment to fraud
- ✓ All amounts balance (₹5L invested - ₹30K returned = ₹4.7L loss)
- ✓ No temporal paradoxes - dates align correctly
- ✓ Multiple independent artifacts supporting the claim
- ✓ Clear evidence of business operations followed by closure

### Downloadable Evidence:
**[Download Demo Evidence File](/home/sohail/sparkle-vault/demo/demo_evidence_investment.txt)**

This is the ideal test case demonstrating what a bulletproof legal claim looks like.

---

## How to Test Each Case:

1. Start the app: `python app.py`
2. Open browser: `http://localhost:5000`
3. Copy the claim text above
4. Upload the matching PDF or any dummy file
5. Click "Audit My Case"
6. Check the result page for:
   - Verdict (STRONG/WEAK/INSUFFICIENT)
   - Confidence Score
   - Verified Facts (green)
   - Logic Leaks (red)
   - Logic Map diagram
   - PDF download button

---

## Quick Test Command (No Browser):

You can also test via curl:

```bash
# Test Case 1 - Strong Case
curl -X POST -F "claim=My landlord took 50000 deposit and never returned it" -F "evidence=@demo/demo_evidence_landlord.pdf" http://localhost:5000/submit
```
