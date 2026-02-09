# Fine-Grained Personal Access Token (PAT) Setup

Cross-repo automation between `lablup/backend.ai-webui` and
`lablup/backend.ai-docs-webui` requires a PAT for `repository_dispatch`.

## Token Creation

1. Go to <https://github.com/settings/tokens?type=beta> (Fine-grained tokens)
2. Click **Generate new token**
3. Configure:
   - **Token name**: `docs-webui-automation`
   - **Expiration**: 90 days (set a calendar reminder to rotate)
   - **Resource owner**: `lablup`
   - **Repository access**: Only select repositories → `lablup/backend.ai-docs-webui`
   - **Permissions (Repository)**:
     - `Contents`: Read and write
     - `Pull requests`: Read and write
     - `Issues`: Read and write
     - `Metadata`: Read-only (auto-selected)
4. Click **Generate token** and copy the value

## Storing as GitHub Secrets

### In `lablup/backend.ai-webui`:

Settings → Secrets and variables → Actions → New repository secret:
- Name: `DOCS_WEBUI_PAT`
- Value: the token

### In `lablup/backend.ai-docs-webui`:

Settings → Secrets and variables → Actions → New repository secret:
- Name: `DOCS_WEBUI_PAT` — the same token
- Name: `OPENAI_API_KEY` — OpenAI API key for `translate_po.py`

## Token Rotation

Rotate every 90 days:
1. Generate a new token with the same permissions
2. Update `DOCS_WEBUI_PAT` in **both** repos
3. Delete the old token

## Verification

```bash
curl -s -o /dev/null -w "%{http_code}" -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <TOKEN>" \
  https://api.github.com/repos/lablup/backend.ai-docs-webui/dispatches \
  -d '{"event_type":"test-dispatch","client_payload":{"test":true}}'
```

A `204` response means the token is working correctly.
