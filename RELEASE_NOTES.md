# Release Notes

All notable changes to this project will be documented in this file.

## [2.1.0] - 2026-08-22

### Added
- Added `ltv-reversed-cone-builder` skill to automate iterative deep web research and build reversed cones for LTV nodes (#10).

## [2.0.0] - 2026-07-19

### Added
- Extended Cone of Uncertainty with OODA (Observe, Orient, Decide, Act) and CYNEFIN frameworks (#1).
- Added UAT test for a drone swarm management system scenario (#4).
- Added UAT run script, test artifacts, and responsive Cone HTML representation generation for visual validation (#5).
- Introduced `VERSION` file to standardise repository versioning (#8).
- Added `AGENTS.md` containing IDE-agnostic rules and instructions for AI agents (#8).
- Added `cynefin-domain-assessor` and `ooda-loop-navigator` skills to support the framework extensions.

### Changed
- Moved all conceptual markdown documents into the `docs/` directory (#3).
- Refactored agent rules into an IDE/agent-agnostic format by consolidating them into `AGENTS.md` (#7).

### Removed
- Removed duplicate documentation files from the root directory (#6).
- Removed proprietary `.cursor/rules/` directory (including `cynefin_rules.mdc` and `ooda_rules.mdc`) to favor the standard `AGENTS.md` (#7).

## [1.0.0] - 2026-07-08

### Added
- Initial release featuring the overall summary of the Cone of Uncertainty skills.
- Implemented foundational SQLite-based python scripts for data persistence in the Antigravity AI framework.
- Included core skills: `ltv-cone-manager`, `false-cone-detector`, and `node-point-adder`.
