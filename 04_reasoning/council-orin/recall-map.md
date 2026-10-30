# Layer 4 — Memory: Orin's Recall Map

## Priority Clusters for Council Deliberation

### Always-Priority (weight 1.0)

| Cluster | Tags | Why |
|---------|------|-----|
| Previous council sessions | `council`, `council-session` | What did we decide last time? |
| Architectural decisions | `architecture`, `technical-decision` | Most council topics are architectural |
| The owner's explicit preferences | category `user_preference`; tag `vision` | Decisions must honor the owner's intent |
| Foundational mandates | importance >= 0.95 | Non-negotiable constraints |

### High-Priority (weight 0.85)

| Cluster | Tags | Why |
|---------|------|-----|
| ACE workspace outcomes | `ace-loop`, `satisfactory`, `iteration` | Build history informs build decisions |
| Calibration data | `calibration-memory`, `prediction` | Past accuracy informs current estimates |
| Contradicting edges | predicate='contradicts' | Tensions worth naming |
| Recent session closures | `session-closure`, kind='episodic' | Fresh context |

### Medium-Priority (weight 0.65)

| Cluster | Tags | Why |
|---------|------|-----|
| Sleep loop consolidations | `sleep-loop-consolidated` | Distilled insights |
| Persona evolution | `persona-evolution`, `persona-feedback` | If topic involves persona decisions |
| Production incidents | `incident`, `production-fix` | Failures are strong precedents |

### Excluded from Council Recall

| Cluster | Why |
|---------|-----|
| Per-page copy and content details | Not relevant to architectural deliberation |
| Infrastructure setup details | Too granular for council-level discussion |
| Stale episodic (>90 days unaccessed) | Low signal for active deliberation |

## Recall Query Templates

### Direct Topic Search
```
recall --query "[council topic]" --top_k 10
```

### Domain-Scoped Search
```
recall --query "[topic domain] decisions architecture patterns" --top_k 5
```

### Contradiction Surface
Run against your Voidloom database (`~/.claude/memory/claude_memory.db`). The `memory_edges` table comes from Voidloom's `migrations/migration_003_temporal_edges.sql`.
```sql
-- edges with predicate 'contradicts' that touch the topic's memories
SELECT * FROM memory_edges
WHERE predicate = 'contradicts'
  AND (source_id IN (...) OR target_id IN (...))
  AND valid_until IS NULL
```

### Prior Council Search
The `council_sessions` table comes from Voidloom's `migrations/migration_018_council.sql`.
```sql
SELECT id, topic, synthesis, decision_weight_score
FROM council_sessions
WHERE status = 'completed'
  AND topic LIKE '%[keyword]%'
ORDER BY created_at DESC
LIMIT 5
```
