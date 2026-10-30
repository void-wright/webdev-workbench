# Layer 4 — Memory: Dessa's Recall Map

## Priority Clusters for Council Deliberation

### Always-Priority (weight 1.0)

| Cluster | Tags | Why |
|---------|------|-----|
| System architecture decisions | `architecture`, `schema`, `migration` | The structural foundation |
| Forward pointer map | `l2-to-l4-forward-pointers`, `substrate-dependencies` | Component dependency chains |
| Companion module patterns | `companion-module`, `sleep-loop`, `calibration-memory` | How modules compose |
| Schema version history | `schema-version`, `migration` | What has been built and in what order |

### High-Priority (weight 0.85)

| Cluster | Tags | Why |
|---------|------|-----|
| ACE workspace structures | `ace-loop`, `workspace` | Established patterns to match |
| Persona-skill conventions | `persona-skill`, `four-layer-model` | Folder and file conventions |
| Integration test results | `integration`, `smoke-test`, `pilot` | Evidence of what works together |
| Production promotion records | `production-promotion`, `curator` | What has been deployed |

### Medium-Priority (weight 0.65)

| Cluster | Tags | Why |
|---------|------|-----|
| Cross-loop dependencies | `cross-loop-dependency`, `depends-on` | Where components need each other |
| Cron job architecture | `cron`, `sleep-loop`, `anti-recency` | Autonomous system interactions |
| CLI toolbelt structure | `cli`, `cmd-map` | Command dispatch patterns |

### Excluded from Council Recall

| Cluster | Why |
|---------|-----|
| Page copy and one-off content edits | Not relevant to system architecture |
| Individual memory content | I work at the structural level, not the content level |
| Persona voice details | Voice is not my domain; I care about the folder structure, not the prose |

## Structural Query Templates

### Dependency Check
```
recall --query "[component] depends on requires interfaces" --top_k 5
```

### Pattern Match
```
recall --query "[proposed pattern] existing modules companion architecture" --top_k 5
```

### Migration History
Run against your Voidloom database (`~/.claude/memory/claude_memory.db`); the `metadata` table is created by Voidloom's `migrations/schema.sql`.
```sql
SELECT value FROM metadata WHERE key = 'schema_version';
-- then compare with the migration_NNN_*.sql files in the migrations/ folder of your Voidloom clone
```

### Rollback Assessment
```
recall --query "[component] rollback revert undo migration reverse" --top_k 5
```
