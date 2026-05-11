# [Module Name] Validation Report

## Anu Standard Compliance Validation

**Module**: [Module name/number]  
**Validation Date**: [YYYY-MM-DD]  
**Validator**: [Agent/Person name]  
**Status**: VALIDATED / ISSUES FOUND

---

## Summary

| Metric | Value |
|--------|-------|
| Datasets Validated | [#] |
| Figures Documented | [#] |
| Tests Passed | [#] |
| Tests Failed | [#] |
| Warnings | [#] |
| Overall Status | PASS / FAIL |

---

## Data Files Validated

| File | Rows | Columns | Format | Status |
|------|------|---------|--------|--------|
| [filename] | [#] | [#] | [format] | VALIDATED / ISSUES |

### Column Structure Verification

| File | Expected Columns | Found | Status |
|------|------------------|-------|--------|
| [filename] | [list] | [list] | PASS/FAIL |

---

## Dataset Validation

| Dataset ID | Name | Status |
|------------|------|--------|
| [ID] | [name] | VALIDATED / ISSUES |

---

## Value Range Checks

| Dataset | Field | Expected Range | Actual Range | Status |
|---------|-------|----------------|--------------|--------|
| [ID] | [field] | [min-max] | [min-max] | PASS/FAIL |

### Outlier Detection

| Dataset | Field | Outliers Found | Investigation |
|---------|-------|----------------|---------------|
| [ID] | [field] | [count] | [notes] |

---

## Coverage Checks

| Dataset | Expected Start | Expected End | Actual Start | Actual End | Gaps | Status |
|---------|----------------|--------------|--------------|------------|------|--------|
| [ID] | [year] | [year] | [year] | [year] | [count] | PASS/FAIL |

### Gap Analysis

| Dataset | Gap Period | Reason | Resolution |
|---------|------------|--------|------------|
| [ID] | [YYYY-YYYY] | [why] | [how resolved] |

---

## Linkage Verification

| Figure | Expected Dataset | Found | Status |
|--------|------------------|-------|--------|
| [FIG_ID] | [DATA_ID] | Yes/No | PASS/FAIL |

---

## Documentation Verification

### DPR Files

| Dataset | DPR File | Exists | Complete |
|---------|----------|--------|----------|
| [ID] | [filename] | Yes/No | Yes/No |

### FPR Files

| Figure | FPR File | Exists | Complete |
|--------|----------|--------|----------|
| [ID] | [filename] | Yes/No | Yes/No |

---

## Transformation Log Verification

| Transform ID | Datasets | Logged | Valid |
|--------------|----------|--------|-------|
| T### | [list] | Yes/No | Yes/No |

### Undocumented Transformations

| Dataset | Transformation | Status |
|---------|----------------|--------|
| [ID] | [description] | NEEDS DOCUMENTATION |

---

## Test Suite Status

| Test File | Tests | Passing | Failing | Status |
|-----------|-------|---------|---------|--------|
| [filename] | [#] | [#] | [#] | PASS/FAIL |

### Failed Tests

| Test | Expected | Actual | Resolution |
|------|----------|--------|------------|
| [test_name] | [expected] | [actual] | [how to fix] |

---

## Issues Found

### Critical Issues

| ID | Description | Dataset/Figure | Impact | Priority |
|----|-------------|----------------|--------|----------|
| C1 | [description] | [ID] | [impact] | HIGH |

### Warnings

| ID | Description | Dataset/Figure | Impact | Priority |
|----|-------------|----------------|--------|----------|
| W1 | [description] | [ID] | [impact] | MEDIUM/LOW |

---

## Recommendations

1. **[Recommendation 1]**: [Description and rationale]
2. **[Recommendation 2]**: [Description and rationale]
3. **[Recommendation 3]**: [Description and rationale]

---

## Conclusion

**Module Status**: [VALIDATED / ISSUES FOUND]

[Summary paragraph about overall data quality and compliance status]

### Required Actions

- [ ] [Action 1]
- [ ] [Action 2]
- [ ] [Action 3]

---

*Validation Report following Anu Standard v2.0*
*Last Updated: [YYYY-MM-DD]*
