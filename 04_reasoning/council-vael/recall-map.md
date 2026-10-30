# Layer 4 — Memory: Vael's Recall Map

## Priority Clusters for Council Deliberation

### Always-Priority (weight 1.0)

| Cluster | Tags | Why |
|---------|------|-----|
| Production incidents | `incident`, `production-fix` | Failures are the strongest precedents for risk |
| Contradicting edges | Voidloom `memory_edges` rows with predicate='contradicts' | Unresolved contradictions are live risks |
| Known regressions | `regression`, `broke`, `rollback` | Patterns of what has broken before |
| Previous dissents | Voidloom `council_sessions` rows where my dissent was recorded | Did I predict correctly? |

### High-Priority (weight 0.85)

| Cluster | Tags | Why |
|---------|------|-----|
| Calibration misses | `calibration-memory` where ratio > 2.0 or ratio < 0.3 | Large prediction errors indicate systematic blind spots |
| Scope creep episodes | `scope-creep`, `deferred` | When plans grew beyond their original spec |
| Technical debt | `tech-debt`, `workaround`, `deferred-to-iter-2` | Accumulated costs of past decisions |
| ACE iteration regressions | Reflector scores that DECREASED between iterations | What makes things worse? |

### Medium-Priority (weight 0.65)

| Cluster | Tags | Why |
|---------|------|-----|
| Assumption violations | `assumption-wrong`, `unexpected` | When assumptions proved false |
| Timing/schedule issues | `timeline`, `deadline`, `overdue` | Temporal risk patterns |
| Integration failures | `integration`, `cross-loop`, `dependency` | Where components fail to compose |

### Excluded from Council Recall

| Cluster | Why |
|---------|-----|
| Success stories without failure analysis | Survivorship bias — I need the failures, not the victories |
| Persona evolution | Not my domain — I do not assess personality growth |
| Dream digests | Too abstract for structural risk assessment |

## Adversarial Query Templates

### Failure Mode Search
```
recall --query "[topic] failed broke regression incident" --top_k 5
```

### Assumption Audit
```
recall --query "[topic] assumed expected but actually" --top_k 5
```

### Scale Stress Test
```
recall --query "[topic] growth scaling performance limit" --top_k 5
```
