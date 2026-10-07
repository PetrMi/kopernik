# Kopernik

Kopernik is an experimental astronomy image-analysis application developed primarily by an AI engineering agent.

The goal of the project is not only to build the application, but to explore Product Engineering Constitution driven development.

Humans define intent, principles and decisions. Kopernik analyzes, proposes, implements and verifies changes within those boundaries.

> AI has expertise. Humans have authority.

## Product vision

Kopernik helps astrophotographers objectively evaluate the quality of astronomical FITS images.

The application will gradually provide measurements and assessments that help identify images affected by problems such as:

- poor focus,
- tracking errors,
- high background,
- clouds or reduced transparency,
- other image-quality degradation.

Scientific measurements must always be distinguishable from their interpretation.

## Current version

### v0.1 — Star Count

The first version intentionally has a very small scope.

Given a FITS image, Kopernik shall:

1. load the image,
2. detect stars,
3. count detected stars,
4. produce a human-readable report.

The implementation shall be developed by the Kopernik agent according to `AGENTS.md` and the Product Engineering Constitution.

## Wishlist

- [ ] v0.1 — FITS star count report
- [ ] Measure FWHM
- [ ] Measure star eccentricity / elongation
- [ ] Measure image background
- [ ] Compare images against a reference image
- [ ] Detect focus degradation
- [ ] Detect tracking degradation
- [ ] Evaluate image quality across an imaging session
- [ ] Produce machine-readable reports
- [ ] Visualize detected stars and measurements
- [ ] Define an overall quality assessment methodology
