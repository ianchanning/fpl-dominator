# GHCR Provenance Attestation Gremlin (The `unknown/unknown` Phantom)

## 1. The Sovereign Law

**A registry row labelled `unknown/unknown` under a tag that was pushed by `docker buildx --push` is almost never a second OS/architecture — it is the platform-less SLSA provenance attestation manifest that BuildKit ≥ 0.13 (Docker 25+) bundles by default into the pushed OCI index, and registry web UIs flatten index members into "platform" rows.**

## 2. Formulation & Trigger Context

Symptom: the GHCR package "Tags" page lists *two* `docker pull` rows for one tag — e.g. `sha-26966c6` → `linux/amd64` (`sha256:7fa1dfe…`) and `unknown/unknown` (`sha256:b6784a7…`). The human brain reads "two rows" as "multi-arch misconfiguration"; the truth is a **single** OCI index (`application/vnd.oci.image.index.v1+json`) whose member list is:

| Member | Digest | Platform | Role |
| --- | --- | --- | --- |
| image manifest | `sha256:7fa1dfe…` | `linux/amd64` | the actual image |
| attestation manifest | `sha256:b6784a7…` (838 B) | `unknown/unknown` | SLSA build provenance, annotated `vnd.docker.reference.type: attestation-manifest`, `vnd.docker.reference.digest: <image digest>` |

Chain of causation for the fpl-dominator runner image:

1. `.github/workflows/docker_publish.yml` → `docker/build-push-action@v7` with `push: true` and no `provenance:` input.
2. BuildKit on the runner (Docker 25+) defaults push to `--provenance=true` → it publishes an index of `{image, attestation}` instead of a bare manifest.
3. GitHub's package UI enumerates index members, labels the platform-less member `unknown/unknown`, and renders one "pull row" per member.

## 3. Dynamic Chaos vs. Typed Mathematical Truth

| ❌ WRONG (naive reading) | ✅ RIGHT (manifest-verified reading) |
| --- | --- |
| "Two rows ⇒ two architectures ⇒ someone pushed from two different OSes" | Rows = index members; check the index, not the UI |
| "Something double-pushed the same tag; dedupe the workflows" | A single `buildx --push` emits the pair atomically in one operation |
| "Pulls are broken / mixed-OS image" | `docker pull <tag>` resolves the index → picks `linux/amd64`; only tooling that naively consumes *every* index member (old skopeo, hand-rolled registry clients) stumbles on the attestation |

## 4. The Pattern

### Dissection Protocol (verify before you "fix")

```bash
# 1. Anonymous pull token (works for public packages)
TOKEN=$(curl -s "https://ghcr.io/token?scope=repository:<owner>/<image>:pull" \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['token'])")

# 2. Fetch the tag's manifest (accept index + manifest media types)
curl -s -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.oci.image.index.v1+json, application/vnd.docker.distribution.manifest.v2+json" \
  "https://ghcr.io/v2/<owner>/<image>/manifests/<tag>"
```

Read the verdict off the JSON:
- `mediaType` is an **index** and one member carries `vnd.docker.reference.type: attestation-manifest` with platform `unknown/unknown` ⇒ **provenance gremlin**, not a dual-arch push.
- The tag resolves to two *different top-level* digests only after two genuinely distinct pushes ⇒ real double-push misconfiguration (different beast).

Cross-check locally: `docker buildx imagetools inspect <image>:<tag>` prints the attestation provenance (source ref, build args) next to the platform list.

### ❌ WRONG (anti-pattern)

```yaml
# no provenance input → inherits BuildKit default (ON for push since Docker 25)
uses: docker/build-push-action@v7
with:
  push: true
  tags: ${{ steps.meta.outputs.tags }}
```

### ✅ RIGHT (surgical, one line)

```yaml
uses: docker/build-push-action@v7
with:
  push: true
  tags: ${{ steps.meta.outputs.tags }}
  # Single-platform amd64 CI image: attestations add no supply-chain value,
  # they only spawn a phantom `unknown/unknown` row on the GHCR page.
  provenance: false
```

### Decision Matrix

| Situation | `provenance` |
| --- | --- |
| Single-platform internal CI runner image (this repo) | `false` — clean page, identical pull behavior |
| Multi-platform public image where consumers verify build lineage | `true` (keep the index; consumers use `buildx imagetools`) |
| Legacy tooling in the pull chain that cannot handle index members without platforms | `false`, or pin/skip the attestation client-side |

### Legacy Tag Hygiene

Already-pushed attested tags are immutable content: per-commit `sha-*` tags keep their index until explicitly deleted (`DELETE /v2/<image>/manifests/<digest>` with a `write`-scoped token, or GitHub's package-version REST API). Leaving them is functionally harmless; subsequent pushes under the same tag (e.g. `latest`) re-point to the clean bare manifest.

---
*Forge date: 2026-10-24 · Verified live against `ghcr.io/ianchanning/fpl-dominator-runner:sha-26966c6` (index digest members `7fa1dfe…` + `b6784a7…`).* `(⊕)`