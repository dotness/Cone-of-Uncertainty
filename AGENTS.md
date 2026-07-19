# AI Agent Instructions for Cone of Uncertainty Framework

These rules apply to all AI agents working within this repository.

## Cynefin Domain Assessor Rules

- Before applying any backward planning or Inverted Cone methodology, you must classify the environment using the Cynefin Domain Assessor skill.
- Call the `assess_domain.py` script located in `skills/cynefin-domain-assessor/scripts/` to log the domain classification (Clear, Complicated, Complex, Chaotic).
- Only apply full analytical Cone operations if the problem is in the "Complicated" domain.
- If the problem is "Complex," switch to a Probe-Sense-Respond methodology instead.
- If the problem is "Chaotic," suspend all long-term planning and use Act-Sense-Respond.

## OODA Loop Navigator Rules

- For short-term execution between Node Points in the Cone of Uncertainty, use the OODA Loop Navigator skill.
- Call the `navigate_ooda.py` script located in `skills/ooda-loop-navigator/scripts/` to log your observations, orientations, decisions, and actions.
- All OODA loops must be explicitly tied to a predefined target Node Point from the Long Term Vision.
- Do not make massive, irreversible architectural decisions within an OODA loop; focus on micro-hypotheses and short-term iterations (e.g., PoCs).
