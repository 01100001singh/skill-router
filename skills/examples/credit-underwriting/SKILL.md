---
name: credit-underwriting
description: Evaluate loan applications using credit scoring models and regulatory guidelines
utterances:
  - "evaluate loan application"
  - "check credit worthiness"
  - "underwrite this loan"
  - "assess credit risk"
  - "review mortgage application"
keywords:
  - credit
  - loan
  - underwriting
  - risk assessment
  - mortgage
  - lending
---

# Credit Underwriting Skill

Evaluate loan applications using credit scoring models and regulatory compliance.

## Regulatory Framework

- **FCRA**: Fair Credit Reporting Act compliance
- **ECOA**: Equal Credit Opportunity Act
- **TILA**: Truth in Lending Act
- **HMDA**: Home Mortgage Disclosure Act

## Evaluation Criteria

### Credit Factors (5 C's)

1. **Character**: Credit history, payment patterns
2. **Capacity**: Income, DTI ratio, employment stability
3. **Capital**: Down payment, reserves
4. **Collateral**: Property value, LTV ratio
5. **Conditions**: Loan purpose, market conditions

### Key Metrics

| Metric | Threshold |
|--------|-----------|
| Credit Score | 620+ (conventional) |
| DTI Ratio | ≤43% |
| LTV Ratio | ≤80% (no PMI) |
| Employment | 2+ years |

## Risk Assessment

```
Low Risk: Score ≥ 740, DTI ≤ 36%, LTV ≤ 80%
Medium Risk: Score 680-739, DTI 36-43%, LTV 80-90%
High Risk: Score < 680, DTI > 43%, LTV > 90%
```

## Compliance Requirements

- Document all decision factors
- Provide adverse action notices
- Maintain fair lending practices
- Log all automated decisions

## Output Format

Every underwriting decision must include:
1. Decision (Approve/Deny/Refer)
2. Risk tier
3. Conditions (if applicable)
4. Adverse action reasons (if denied)
5. Audit trail
