"""Mock bank data for Phase 1. Phase 2: replace function bodies, keep signatures."""

# Mock KPI data for two cooperative banks
_MOCK_BANK_DATA = {
    "bank_a": {
        "total_assets_meur":  1240.5,
        "tier1_capital_pct":  14.2,
        "cost_income_ratio":  62.4,
        "npl_ratio":           1.8,
        "roe_pct":             7.3,
        "branch_count":        24,
        "member_count":      18500,
    },
    "bank_b": {
        "total_assets_meur":   890.2,
        "tier1_capital_pct":  15.8,
        "cost_income_ratio":  67.1,
        "npl_ratio":           2.1,
        "roe_pct":             5.9,
        "branch_count":        18,
        "member_count":      12300,
    },
}

_DEFAULT_SYNERGY_WEIGHTS = {
    "cost_reduction":       0.5,
    "revenue_enhancement":  0.5,
    "capital_optimization": 0.5,
    "it_consolidation":     0.5,
    "member_retention":     0.5,
}

def get_bank_data(bank_key: str) -> dict:
    """Return KPI dict for bank_key ('bank_a' or 'bank_b').
    Phase 2: replace with real data fetch. Signature stays the same.
    """
    return _MOCK_BANK_DATA.get(bank_key, {})

def get_synergy_weights() -> dict:
    """Return default synergy weights.
    Phase 2: may pull from analyst profile or prior session.
    """
    return _DEFAULT_SYNERGY_WEIGHTS.copy()

def get_mock_verdict() -> dict:
    """Return mock GO/NO-GO verdict for Results screen.
    Phase 2: replace with LLM-generated analysis.
    """
    return {
        "verdict": "GO",
        "confidence": 0.82,
        "rationale": "Placeholder: AI-generated rationale will appear here in Phase 2.",
    }
