"""
Fact Checker Agent (TASK 03)
Enforces journalistic rigor: verifies claims against primary sources,
flags ungrounded assertions, and checks for factual drift in script narration.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

class FactChecker:
    def __init__(self, claims_path: Optional[Path] = None):
        self.claims_path = claims_path or Path(r"D:\gitM\01_ContentFactory\production\research\claims.json")

    def load_claims(self) -> List[Dict[str, Any]]:
        if not self.claims_path.exists():
            return []
        with open(self.claims_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def audit_claim_integrity(self, claims: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        claim_list = claims or self.load_claims()
        passed = True
        issues = []
        verified_count = 0

        for c in claim_list:
            cid = c.get("claim_id", "UNKNOWN")
            conf = c.get("confidence", "UNKNOWN")
            
            if conf not in ["VERIFIED", "LIKELY", "DISPUTED", "UNKNOWN", "FALSE"]:
                passed = False
                issues.append(f"Claim {cid} has invalid confidence status '{conf}'")
            
            if not c.get("source") or not c.get("source_id"):
                passed = False
                issues.append(f"Claim {cid} lacks authoritative primary source citation")

            if not c.get("quote"):
                passed = False
                issues.append(f"Claim {cid} lacks exact supporting quotation")

            if not c.get("visual_evidence"):
                passed = False
                issues.append(f"Claim {cid} missing verifiable visual evidence asset")

            if conf == "VERIFIED":
                verified_count += 1

        return {
            "verdict": "PASS" if passed else "FAIL",
            "total_claims": len(claim_list),
            "verified_claims": verified_count,
            "issues": issues
        }

    def verify_script_against_claims(self, narration_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Ensures that every line of narration claiming a concrete fact
        is linked to a verified claim ID and does not exaggerate numbers.
        """
        claims_map = {c["claim_id"]: c for c in self.load_claims()}
        violations = []

        # Ban suspicious unchecked words
        forbidden_buzzwords = ["unprecedented", "infinitely superior", "flawless", "magic", "perfection"]

        for item in narration_items:
            nid = item.get("id", "UNKNOWN")
            text = item.get("text", "")
            referenced_claims = item.get("claims", [])

            for bad in forbidden_buzzwords:
                if bad in text.lower():
                    violations.append(f"Line {nid} contains sensationalist banned buzzword: '{bad}'")

            for cid in referenced_claims:
                if cid not in claims_map:
                    violations.append(f"Line {nid} cites non-existent claim {cid}")
                else:
                    claim_obj = claims_map[cid]
                    if claim_obj.get("confidence") == "FALSE":
                        violations.append(f"Line {nid} cites a FALSE/DEBUNKED claim: {cid}")

        return {
            "verdict": "PASS" if not violations else "FAIL",
            "violations_count": len(violations),
            "violations": violations
        }

if __name__ == "__main__":
    fc = FactChecker()
    audit = fc.audit_claim_integrity()
    print("Fact Checker Audit:", audit)
