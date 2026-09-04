"""
Phase-0 Research Engine: Source Discovery, Claim Extraction, Evidence Mapping, and Research QA.
Ensures every documentary concept is backed by verified factual claims, verifiable sources, and concrete visual evidence before writing begins.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

class SourceDiscovery:
    """Manages the catalog of vetted documentary research sources."""
    def __init__(self, sources_path: Optional[Path] = None):
        if sources_path:
            self.sources_path = sources_path
        else:
            base = Path(__file__).parents[1]
            candidates = [base / "research" / "sources.json", base / "sources.json"]
            self.sources_path = next((c for c in candidates if c.exists()), base / "sources.json")
        self.sources = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        if self.sources_path.exists():
            with open(self.sources_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("sources", [])
        return []

    def get_source(self, source_id: str) -> Optional[Dict[str, Any]]:
        for s in self.sources:
            if s.get("source_id") == source_id:
                return s
        return None

class ClaimExtractor:
    """Manages fact claims with strict importance, confidence, and source citations."""
    def __init__(self, claims_path: Optional[Path] = None):
        if claims_path:
            self.claims_path = claims_path
        else:
            base = Path(__file__).parents[1]
            candidates = [
                base / "research" / "claims.json",
                base / "claims.json",
                base / "claims" / "claims.json"
            ]
            self.claims_path = next((c for c in candidates if c.exists()), base / "claims" / "claims.json")
        self.claims = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        if self.claims_path.exists():
            with open(self.claims_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("claims", [])
        return []

    def get_claim(self, claim_id: str) -> Optional[Dict[str, Any]]:
        for c in self.claims:
            if c.get("claim_id") == claim_id:
                return c
        return None

    def get_all_claim_ids(self) -> List[str]:
        return [c["claim_id"] for c in self.claims if "claim_id" in c]

class EvidenceMapper:
    """Maps claims to tangible visual evidence types (documents, archival, charts, diagrams)."""
    def __init__(self, evidence_path: Optional[Path] = None):
        if evidence_path:
            self.evidence_path = evidence_path
        else:
            base = Path(__file__).parents[1]
            candidates = [
                base / "research" / "evidence.json",
                base / "evidence.json",
                base / "evidence" / "evidence.json"
            ]
            self.evidence_path = next((c for c in candidates if c.exists()), base / "evidence" / "evidence.json")
        self.evidence = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        if self.evidence_path.exists():
            with open(self.evidence_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("evidence_catalog", [])
        return []

    def get_evidence_for_claim(self, claim_id: str) -> List[Dict[str, Any]]:
        return [e for e in self.evidence if e.get("claim_id") == claim_id]

class ResearchQA:
    """Quality assurance for Phase 0: Verifies source credibility, claim grounding, and visual evidence."""
    def __init__(self, phase0_dir: Optional[Path] = None):
        self.phase0_dir = phase0_dir or Path(__file__).parents[1]
        self.sources = SourceDiscovery(self.phase0_dir / "sources.json")
        self.claims = ClaimExtractor(self.phase0_dir / "claims.json" if (self.phase0_dir / "claims.json").exists() else self.phase0_dir / "claims" / "claims.json")
        self.evidence = EvidenceMapper(self.phase0_dir / "evidence.json" if (self.phase0_dir / "evidence.json").exists() else self.phase0_dir / "evidence" / "evidence.json")

    def run_qa(self) -> Dict[str, Any]:
        results = {
            "sources_count": len(self.sources.sources),
            "claims_count": len(self.claims.claims),
            "evidence_count": len(self.evidence.evidence),
            "unsupported_claims": [],
            "claims_missing_visual_evidence": [],
            "schema_violations": [],
            "research_files_verified": [],
            "verdict": "PASS"
        }

        # Check required Section 2 research files
        required_research_files = [
            "sources.json", "claims.json", "evidence.json",
            "timeline.json", "entities.json", "research-report.json"
        ]
        res_sub = self.phase0_dir / "research"
        for rf in required_research_files:
            found = (res_sub / rf).exists() or (self.phase0_dir / rf).exists()
            if found:
                results["research_files_verified"].append(rf)
            else:
                results["schema_violations"].append(f"Missing Section 2 research file: {rf}")

        source_ids = {s["source_id"] for s in self.sources.sources if "source_id" in s}

        for claim in self.claims.claims:
            cid = claim.get("claim_id", "UNKNOWN")
            
            # Check Section 2 mandatory fields
            for req_field in ["claim_id", "claim", "importance", "source_ids", "confidence", "visual_evidence"]:
                if req_field not in claim or not claim[req_field]:
                    results["schema_violations"].append(f"Claim {cid} missing mandatory Section 2 field '{req_field}'")

            c_sources = claim.get("source_ids", []) or ([claim.get("primary_source")] if claim.get("primary_source") else [])
            
            # Check source grounding
            missing_sources = [sid for sid in c_sources if sid not in source_ids]
            if missing_sources or not c_sources:
                results["unsupported_claims"].append({
                    "claim_id": cid,
                    "missing_sources": missing_sources or ["NO_SOURCES_ASSIGNED"]
                })

            # Check visual evidence mapping
            ev_list = self.evidence.get_evidence_for_claim(cid)
            has_visual = len(ev_list) > 0 or len(claim.get("visual_evidence", [])) > 0
            if not has_visual:
                results["claims_missing_visual_evidence"].append(cid)

        if results["unsupported_claims"] or results["claims_missing_visual_evidence"] or results["schema_violations"]:
            results["verdict"] = "FAIL"

        return results

if __name__ == "__main__":
    qa = ResearchQA()
    res = qa.run_qa()
    print("Research QA Report:", json.dumps(res, indent=2))
