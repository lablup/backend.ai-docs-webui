# Backend.AI WebUI Documentation Style Guide

This guide defines the writing conventions for all documentation in the Backend.AI WebUI docs repository.
All contributors should follow these rules to maintain consistency across the documentation.

---

## Voice and Tone

### Procedural Content (How-to, Step-by-step)
Use **second-person imperative**:
- "Click 'Create Folder' to create a new storage folder."
- "Enter your email address in the **E-Mail** field."
- "Select the project from the dropdown menu."

### Descriptive Content (Feature overview, UI description)
Use **second-person declarative**:
- "You can view the list of active sessions on the **Sessions** page."
- "Your resource usage is displayed in the dashboard panels."

### Conceptual Definitions (Overview, Key Concepts)
Third-person is acceptable for abstract domain definitions:
- "A user is a person who connects to Backend.AI and performs work."
- "A compute session is an isolated virtual environment."

### What to Avoid
- **Passive voice**: "A user can be created by clicking..." → "Click '+Create User' to create a new user."
- **Third-person for instructions**: "Users can change the settings..." → "You can change the settings..."
- **First-person (we/our)**: "We provide..." → "Backend.AI provides..."
- **Overly casual tone**: "you need one thing" → "the following is required"

---

## UI Element References

| Element Type | Convention | Example |
|-------------|-----------|---------|
| Buttons | Single quotes | Click 'Create Folder' |
| Menu items | Single quotes | Select 'Preferences' from the menu |
| Page/Tab names | Bold | Navigate to the **Sessions** page |
| Field labels in forms | Bold | Set **Permission** to Read-Only |
| Status values | Inline code (double backtick) | The session status changes to ``RUNNING`` |
| Technical terms, code | Inline code (double backtick) | The ``model-definition.yml`` file |
| Keyboard shortcuts | Inline code (double backtick) | Press ``Ctrl-R`` to refresh |
| File paths | Inline code (double backtick) | Files are stored under ``/home/work/`` |

### Examples in RST

```rst
Click 'Start' on the **Sessions** page to launch a new compute session.
The session status will change to ``PREPARING`` and then to ``RUNNING``.
Set the **Folder name** field to your desired name (up to 64 characters).
```

---

## Heading Styles

### RST Heading Characters

| Level | Character | Usage |
|-------|-----------|-------|
| H1 (Page title) | `=` (overline + underline) | One per file |
| H2 (Major section) | `-` (underline) | Primary sections |
| H3 (Subsection) | `^` (underline) | Subsections |
| H4 (Sub-subsection) | `~` (underline) | Rarely used |

### Heading Phrasing

Use **noun phrases** or **gerund phrases** for consistency:

- **Good**: "Creating a Storage Folder", "Managing Resource Policies", "Resource Summary Panels"
- **Avoid**: "Create storage folder" (imperative), "How to create a folder" (question-like)

The underline must be at least as long as the heading text.

---

## Content Structure per Page

Each documentation page should follow this structure:

1. **Page title** (H1)
2. **Brief introduction** (1-3 sentences explaining what the feature is and when to use it)
3. **Main screenshot** showing the full page or feature
4. **Sections** with procedural steps or UI descriptions
5. **Notes and warnings** where appropriate

---

## Image Directives

### Rules
- Always include `:alt:` text describing the image content.
- Use `:width: 100%` for full-page screenshots.
- Use `:width: 400` to `:width: 700` for dialogs and partial views.
- Use `:align: center` for dialog and modal screenshots.

### Template

```rst
.. image:: screenshot_name.png
   :width: 100%
   :align: center
   :alt: Description of what the screenshot shows
```

### Screenshot Naming

Use the pattern `<page>_<feature>.png`:
- `session_page_resource_panels.png`
- `admin_user_create_dialog.png`
- `vfolder_create_modal.png`

---

## Terminology

| Term | Correct Usage | Incorrect |
|------|--------------|-----------|
| Product name | Backend.AI | BackendAI, backend.ai |
| GUI client | WebUI | Web-UI, web UI, Web UI |
| Virtual environment | compute session | session (when ambiguous) |
| Storage | storage folder | vfolder (in user-facing docs) |
| Admin types | superadmin, domain admin | super admin, Super Admin |

---

## Admonitions

Use Sphinx admonitions sparingly and consistently:

```rst
.. note::
   Additional context or tips that are helpful but not critical.

.. warning::
   Important cautions about potential issues or data loss.
```

- Use `.. note::` for supplementary information.
- Use `.. warning::` for cautions about destructive actions or potential problems.
- Do not use `.. danger::`, `.. tip::`, or `.. attention::` to keep admonition types simple.

---

## Cross-References

Use Sphinx `:ref:` for internal cross-references:

```rst
For more details, refer to :ref:`creating-a-storage-folder`.
```

Each target should be defined with a label above the heading:

```rst
.. _creating-a-storage-folder:

Creating a Storage Folder
-------------------------
```

---

## Lists

- Use bullet lists (`*` or `-`) for unordered items.
- Use numbered lists (`1.`, `2.`) for sequential steps.
- Indent nested items by 3 spaces.
- Keep parallel structure within a list (all items start with a verb, or all are noun phrases).

---

## Grammar and Spelling

- Use American English throughout.
- Avoid contractions in formal documentation (use "do not" instead of "don't").
- Spell out numbers under 10 ("three sessions"), use digits for 10+ ("15 folders").
- Use the Oxford comma in lists of three or more items.
