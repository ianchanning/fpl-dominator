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

## 5. Registry Forensics & Consumer Gremlin Census (post-purge addendum)

### The versions API is per-manifest, not per-tag

The GHCR REST packages API (`/user/packages/container/{name}/versions`) registers **every manifest digest as its own version**: for an attested single-platform push you get 3 rows — the index manifest (holds the tag), the `linux/amd64` image manifest, and the platform-less attestation manifest. `metadata.container.tags` is an **array of tag-name strings** (jq: `index("latest")`, *not* `map(.name)`). Deleting the version that a tag references removes the tag itself.

### Downstream consumer breakage classes (the "provenance side effect" gremlins)

An attested push means the tag resolves to an OCI **index** even when single-platform. Consumers coded against "tag → one manifest" assumptions break in four documented classes:

| # | Consumer | Symptom |
| --- | --- | --- |
| 1 | `docker pull` on Docker engines < 20.10 (e.g. pinned self-hosted CI agent pools) | `no match for platform in manifest: not found` — whole pipeline red |
| 2 | Shuttle pipelines (pull → retag → push to another registry, `docker save`/`load` hops) | `vnd.docker.reference.*` annotations dropped / index mangled → downstream tag exists but is empty or fails platform match |
| 3 | Vulnerability scanners (Trivy/Grype/ACR built-in, older versions) | Resolves the platform-less attestation member → garbage/empty report → scan gate fails (or falsely green) |
| 4 | `kind` / `minikube load docker-image` | Refuses to load a tag resolving to an index |

`provenance: false` **cures** all four (artifact becomes a bare manifest, pullable by every engine). The rare reverse break — a consumer that hard-requires an index at the top — is unusual and usually `docker buildx imagetools` promotion logic, which still works with bare per-arch manifests.

### The purge incident (2026-10-24, two RUDs)

1. **jq shape RUD:** first purge run assumed `tags = [{name: …}]` → `Cannot index string with string "name"` (exit 5). Fix: treat tags as string array.
2. **Word-split RUD (Lesson 1 recurrence):** `for LINE in $IDS` on two-column lines → second iteration submitted a digest as `version_id` → `HTTP 422: version_id must be an integer`. Fix: `while read -r ID NAME; do … done <<< "$IDS"`. See RUD Ledger, entry 4.

**Final state:** all 12 pre-fix versions deleted (HTTP 204 × 12, idempotent re-runs tolerated); registry reduced to `latest` + `sha-1d8310f`, both bare `application/vnd.oci.image.manifest.v1+json`, no phantom `unknown/unknown` rows. Pre-cleanup snapshot: `wiki/raw/ghcr-tag-census-2026-10-24.json`.