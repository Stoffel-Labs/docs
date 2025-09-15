# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the official documentation repository for Stoffel, a framework for building privacy-first applications using secure Multi-Party Computation (MPC). The documentation is built using mdBook and deployed to GitHub Pages.

## Architecture

The repository follows a standard mdBook structure:
- `src/` - Contains all documentation source files in Markdown
- `book.toml` - mdBook configuration file
- `book/` - Generated output directory (not version controlled)

Key documentation sections:
- **Introduction** - Overview of Stoffel VM, MPC concepts, and project status
- **Getting Started** - Installation, quick start, and basic usage guides
- **Architecture** - Technical details about the register-based VM design with separate clear/secret registers

## Development Commands

### Building the Documentation
```bash
mdbook build
```

### Serving Locally for Development
```bash
mdbook serve
```

### Testing
```bash
mdbook test
```

## Deployment

The documentation is automatically deployed to GitHub Pages via GitHub Actions when changes are pushed to the `main` branch. The workflow uses mdBook v0.4.36 and deploys the built site from the `./book` directory.

## Content Guidelines

- Documentation is actively being developed and marked as "Work in Progress"
- Use proper Markdown formatting and maintain consistent structure
- Follow the existing navigation structure defined in `src/SUMMARY.md`
- The project focuses on MPC (Multi-Party Computation) concepts and the Stoffel VM architecture