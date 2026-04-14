---
name: floracat-architecture-diagram
description: Create or revise standalone HTML/SVG architecture diagrams, runtime flow diagrams, sequence diagrams, and PPT-like technical visuals. Use when a user wants human-readable publication-ready diagrams instead of Mermaid, or wants help improving node layout, arrow accuracy, spacing, overlap handling, Chinese labels, or overall visual style for architecture and flow charts.
---

# Architecture Diagram HTML/SVG

Use this skill to produce standalone HTML files with embedded SVG diagrams that feel like clean presentation slides rather than code-first diagrams.

## Output Form

- Default to a standalone HTML file with embedded SVG.
- Prefer sectioned “deck” structure when there are multiple diagrams on one page.
- Use SVG, not Mermaid, for final publication-quality layout control.
- Make the result readable without zooming and understandable by non-engineers.

## Visual Style

- Use a PPT-like information design style: warm background, panel cards, soft shadows, rounded nodes, restrained colors.
- Prefer clear Chinese labels when the audience is Chinese-speaking; keep only essential English technical terms.
- Use a small set of semantic colors and keep them consistent across sections.
- Keep arrowheads understated; do not make lines or markers visually aggressive.
- Favor balanced spacing over dense packing. The page should feel edited, not auto-generated.

## Diagram Building Workflow

1. Identify the user-facing purpose of each diagram.
2. Reduce the system into a few layers or stages before drawing.
3. Choose the simplest SVG structure that fits:
   - layered architecture
   - runtime flow
   - sequence/timing flow
   - subsystem drill-down
4. Place groups first, then nodes, then arrows, then notes.
5. After layout is stable, localize labels and tighten wording.
6. Do a dedicated arrow and overlap review before finishing.

## Node Rules

- Give every node one clear responsibility.
- Keep titles short; if a title is long, widen the node before shrinking text.
- Use subtitle lines for detail; keep them short and scannable.
- Avoid mixing multiple abstraction levels inside one node.
- Align sibling nodes rigorously.
- Treat text fitting as a hard constraint, not a cosmetic preference.
- Prefer expanding node width or height before reducing font size.
- Keep explicit inner padding so text never touches the node border.
- If a label is still too long, split it into multiple lines instead of forcing a single line.
- Keep title and subtitle blocks vertically separated; do not let subtitle lines crowd the title baseline.

## Text Fitting Guardrails

- Titles should usually fit within 1 to 2 lines.
- Subtitle/detail text should usually fit within 1 to 3 short lines.
- If a node needs more than 3 detail lines, simplify the wording or enlarge the node.
- Use centered `text-anchor="middle"` only when the node is visually symmetric; otherwise use left-aligned text with consistent left padding.
- For multi-line text, use explicit `tspan` line breaks and check the last line against the bottom padding.
- Never solve overflow by aggressively shrinking text first. The preferred order is:
  1. shorten wording
  2. widen or heighten the node
  3. split into lines
  4. only then reduce font size slightly

## Overflow Prevention Procedure

Use this procedure whenever a node contains more than a very short label.

1. Decide the node's usable text width first.
   - Reserve horizontal padding on both sides before placing any text.
   - As a default heuristic, keep at least 18 to 24px padding on each side for medium cards.
2. Estimate whether the label is likely to overflow.
   - If the text is more than roughly one short phrase in Chinese, assume wrapping will be needed.
   - If the node title or detail sentence feels visually dense, wrap proactively rather than waiting for collision.
3. Split long text into semantic chunks, not arbitrary character fragments.
   - Break at phrase boundaries such as commas, pauses, or logical halves.
   - Avoid a final orphan line with only a few characters unless the wording makes that unavoidable.
4. Increase node height to match the wrapped text block.
   - Add height for every extra line.
   - Preserve top padding, line spacing, and bottom padding after wrapping.
5. Re-check surrounding arrows.
   - A taller node changes routing. After resizing, reroute nearby arrows so they still terminate cleanly on the edge.

## Default Node Text Layout

When there is no better local reason to do otherwise, use this rhythm:

- Title block near the top with clear top padding
- 8 to 14px vertical gap between title and first detail line
- Detail lines spaced evenly with explicit `tspan`
- Bottom padding large enough that the last line does not feel trapped

If a node contains both a title and multiple detail lines, prefer a slightly taller node over a cramped compact node.

## Arrow Rules

- Every arrow must start and end on a node edge, not inside a node.
- Prefer straight lines first. Add bends only to avoid collisions or ambiguity.
- When two arrows connect the same pair of areas, offset them vertically or horizontally.
- Use solid lines for primary runtime/data flow.
- Use dashed lines only for support, configuration, feedback, optional linkage, or on-demand reads.
- If arrows are long, shorten or reroute them so the direction remains obvious.
- Do not let text sit on top of an arrow.
- Do not let an arrow run through a node body, even briefly.
- Route arrows around nodes with a clear gap instead of clipping through corners.
- When an arrow passes near a label, move the label or reroute the arrow; do not rely on luck.
- Keep arrow stems visually outside the node fill area. The first visible segment should begin at the border, not under the node.
- If an arrow and a node are close, shorten the arrow and move the marker closer to the target edge instead of drawing a long intrusive line.

## SVG Layering Rules

- Draw large background groups first.
- Draw arrows beneath nodes whenever possible.
- Draw node fills and borders above arrows.
- Draw text above both nodes and arrows.
- If an arrow must pass behind a node, the node should fully mask the line so no segment appears inside the node body.

## Editing Rules

- When refining an existing SVG, inspect coordinates instead of making semantic guesses.
- If a user reports overlap, fix geometry directly: move nodes, widen boxes, reroute paths, or adjust text anchors.
- If a user questions arrow meaning, verify the actual system relationship in code/docs first, then correct the line.
- Prefer explicit labels over decorative complexity.
- After every substantial change, do one dedicated pass only for text overflow and node padding.
- After that, do a separate pass only for arrow routing and line-node collisions.
- If multiple nodes have long text, standardize the wrapping style across the whole diagram instead of fixing only one offending node.

## Diagram-Specific Guidance

### Overall Architecture

- Separate access surfaces, control plane/runtime, capability subsystems, and state/config areas.
- Use enclosing groups to show ownership or subsystem boundaries.
- Keep cross-group arrows sparse and precise.

### Runtime Flow

- Emphasize the main path first.
- Put configuration, session state, and plugin/runtime support below the main path as supporting layers.
- Use wording that reads like product behavior, not source code names, unless the source name is important.

### Sequence Diagram

- Reduce participants to the minimum needed to explain the flow.
- Name participants by role, not by file/module, unless implementation detail is the point.
- Use loops only where a real repeated interaction exists.
- Move loop labels close to the loop arrow.

## Final Review Checklist

Before finishing, read [references/review-checklist.md](references/review-checklist.md) and verify every item.
