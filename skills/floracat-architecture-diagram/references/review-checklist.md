# Diagram Review Checklist

Run this review after every substantial diagram edit.

## Semantics

- Confirm each node represents the correct system concept.
- Confirm each arrow direction matches the real relationship.
- Remove arrows that do not express a meaningful dependency or flow.
- Separate primary flow from support/config links.

## Layout

- Check that no text extends beyond node borders.
- Check that all node text keeps visible inner padding from every edge.
- Check that multi-line text still leaves bottom padding inside the node.
- Check that similar nodes use a consistent wrapping rhythm instead of a mix of single-line and cramped multi-line layouts.
- Check that sibling nodes align cleanly.
- Check that groups fully contain their child nodes.
- Check that headings and body content have comfortable margins.

## Arrows

- Check that all arrows terminate on node edges.
- Check that no arrow starts inside a node body.
- Check that no arrow segment passes through any node body.
- Check that arrows are visually below node bodies and do not show through fills.
- Check that parallel arrows are offset rather than overlapping.
- Check that long arrows do not create misleading visual ownership.
- Check that dashed arrows are visually lighter than primary solid arrows.
- Check that markers are small enough not to dominate the node they point to.

## Readability

- Check that labels are short and human-readable.
- Check that important concepts are in Chinese if the target audience is Chinese-speaking.
- Check that text does not sit on top of lines.
- Check that title and subtitle blocks are clearly separated inside each node.
- Check that loops and return paths are still easy to follow.

## Publication Fit

- Check that the diagram looks intentional at page scale, not only when zoomed in.
- Check that the visual style is consistent across sections.
- Check that the result feels like a presentation slide, not a raw engineering sketch.
