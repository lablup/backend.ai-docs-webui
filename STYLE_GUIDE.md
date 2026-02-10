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
| Status values | Inline code | The session status changes to `RUNNING` |
| Technical terms, code | Inline code | The `model-definition.yml` file |
| Keyboard shortcuts | `<kbd>` tag or inline code | Press <kbd>Ctrl</kbd>+<kbd>R</kbd> to refresh |
| File paths | Inline code | Files are stored under `/home/work/` |

### Examples

```markdown
Click 'Start' on the **Sessions** page to launch a new compute session.
The session status will change to `PREPARING` and then to `RUNNING`.
Set the **Folder name** field to your desired name (up to 64 characters).
```

---

## Heading Styles

### Markdown Heading Levels

| Level | Syntax | Usage |
|-------|--------|-------|
| H1 | `#` | Page title — one per file |
| H2 | `##` | Major section |
| H3 | `###` | Subsection |
| H4 | `####` | Sub-subsection (rarely used) |

### Heading Phrasing

Use **noun phrases** or **gerund phrases** for consistency:

- **Good**: "Creating a Storage Folder", "Managing Resource Policies", "Resource Summary Panels"
- **Avoid**: "Create storage folder" (imperative), "How to create a folder" (question-like)

### Heading Rules
- Leave one blank line before and after each heading.
- Do not skip heading levels (e.g., do not jump from `##` to `####`).
- Do not add trailing punctuation to headings.

---

## Content Structure per Page

Each documentation page should follow this structure:

1. **Page title** (H1)
2. **Brief introduction** (1-3 sentences explaining what the feature is and when to use it)
3. **Main screenshot** showing the full page or feature
4. **Sections** with procedural steps or UI descriptions
5. **Notes and warnings** where appropriate

---

## Images

### Rules
- Always include alt text describing the image content.
- Place images on their own line (not inline with text).
- Use HTML `<img>` tag when you need to control width or alignment.

### Markdown Syntax

```markdown
![Description of what the screenshot shows](images/screenshot_name.png)
```

For size control:

```html
<p align="center">
  <img src="images/screenshot_name.png" alt="Description" width="100%">
</p>
```

| Image Type | Width |
|-----------|-------|
| Full-page screenshot | `width="100%"` |
| Dialog / modal | `width="400"` to `width="700"` |
| Small icon or button | `width="200"` or less |

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

## Callouts (Notes and Warnings)

Use blockquote-based callouts with emoji prefixes:

```markdown
> **Note:** Additional context or tips that are helpful but not critical.

> **Warning:** Important cautions about potential issues or data loss.
```

If the documentation framework supports GitHub-style alerts (e.g., MkDocs with appropriate plugin):

```markdown
> [!NOTE]
> Additional context or tips that are helpful but not critical.

> [!WARNING]
> Important cautions about potential issues or data loss.
```

- Use **Note** for supplementary information.
- Use **Warning** for cautions about destructive actions or potential problems.
- Keep callout types simple — avoid using Tip, Danger, or Attention.

---

## Links and Cross-References

### Internal Links (within docs)

```markdown
For more details, see [Creating a Storage Folder](storage/create-folder.md).
```

### Anchor Links (within the same page)

```markdown
See the [Resource Summary Panels](#resource-summary-panels) section below.
```

Markdown auto-generates anchors from headings by lowercasing and replacing spaces with hyphens.

### External Links

```markdown
Refer to the [Backend.AI documentation](https://docs.backend.ai) for server-side details.
```

---

## Lists

- Use bullet lists (`-`) for unordered items.
- Use numbered lists (`1.`, `2.`) for sequential steps.
- Indent nested items by 2 spaces.
- Keep parallel structure within a list (all items start with a verb, or all are noun phrases).

---

## Code Blocks

Use fenced code blocks with language identifiers:

````markdown
```bash
pip install backend.ai-client
```

```yaml
model-definition:
  name: my-model
  runtime: python
```
````

For inline code, use single backticks: `config.toml`.

---

## Tables

Use standard Markdown tables with header separators:

```markdown
| Column A | Column B | Column C |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
```

- Align pipes for readability (optional but recommended).
- Use inline code in table cells when showing technical values.

---

## Grammar and Spelling

- Use American English throughout.
- Avoid contractions in formal documentation (use "do not" instead of "don't").
- Spell out numbers under 10 ("three sessions"), use digits for 10+ ("15 folders").
- Use the Oxford comma in lists of three or more items.
