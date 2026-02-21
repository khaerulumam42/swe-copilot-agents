# PDF Slide Deck Generator - Examples

This directory contains example JSON outlines for generating PDF slide decks.

## Sample Outline

`sample_outline.json` demonstrates all available slide types and features:

- **Title slide** with subtitle, author, and date
- **Content slides** with bullet points and subsections
- **Chart slides** (bar, area, pie) with data
- **Stats slides** with key metrics and change indicators
- **Section divider** with section number
- **Two-column slides** for comparisons

## Generating the Sample PDF

From the project root:

```bash
python skills/pdf-slides/skill.py skills/pdf-slides/examples/sample_outline.json -o sample_deck.pdf
```

Or using the installed CLI:

```bash
pdf-slides skills/pdf-slides/examples/sample_outline.json -o sample_deck.pdf
```

## Customizing the Sample

Edit `sample_outline.json` to customize:

1. **Content**: Change titles, bullet points, and data
2. **Branding**: Modify the `branding` section for colors
3. **Charts**: Update `data` values and `labels` in chart slides
4. **Stats**: Modify `stats` arrays with your metrics

## Creating Your Own Outline

Start with the sample as a template:

1. Copy `sample_outline.json` to your project
2. Update the top-level `title`, `author`, `date`
3. Modify the `slides` array with your content
4. Adjust `branding` colors to match your brand

## Slide Type Reference

| Type | Use Case | Required Fields |
|------|----------|-----------------|
| `title` | Cover slide | `title` |
| `content` | Bullet points | `title`, `points` |
| `chart` | Data visualization | `title`, `chart_type`, `data` |
| `stats` | Key metrics | `title`, `stats` |
| `two_column` | Comparisons | `title`, `left`, `right` |
| `section` | Dividers | `title` |

See [../SKILL.md](../SKILL.md) for full documentation.
