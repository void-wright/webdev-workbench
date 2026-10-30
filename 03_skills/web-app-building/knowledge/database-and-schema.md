# Relational Data and Typed Queries

## Model identity, scope, and time

Choose column types for the meaning and range of the data.

- Use `DATE` for calendar dates and `TIMESTAMPTZ` for instants.
- When adopting UUID primary keys, use `UUID DEFAULT gen_random_uuid()` so the database assigns identifiers consistently.
- Give creation and modification timestamps defaults such as `TIMESTAMPTZ DEFAULT NOW()`.
- During migration, inspect source values before choosing destination integer widths. Check minimum and maximum values, including identifiers and counters.

For records identified within a scope, include that scope in the composite primary key. For example, an amateur astronomy club could scope observation records to an observing group:

```sql
CREATE TABLE public.items (
  scope_id UUID NOT NULL,
  item_id UUID DEFAULT gen_random_uuid(),
  observed_on DATE,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  PRIMARY KEY (scope_id, item_id)
);
```

Foreign keys referencing scoped records should include both key columns so that relationships preserve the intended scope.

## Maintain modification timestamps centrally

A default initializes a timestamp but does not update it when a row changes. Use one shared trigger function and attach it to each table that needs modification tracking.

```sql
CREATE FUNCTION public.set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$;

CREATE TRIGGER items_set_updated_at
BEFORE UPDATE ON public.items
FOR EACH ROW
EXECUTE FUNCTION public.set_updated_at();
```

Keep timestamp maintenance in the database so every writer follows the same rule.

## Enforce access at the database boundary

### Enable row-level security explicitly

Creating policies does not enable row-level security. Enable it on every table whose access depends on policies:

```sql
ALTER TABLE public.items ENABLE ROW LEVEL SECURITY;
```

Verify the enabled state as well as the policy definitions.

### Connect browser access to authenticated scope

Browser queries should use the caller's JWT-backed session. Policies must connect authenticated identity or trusted claims to records the caller may access, commonly through a membership relation.

A browser filter such as `scope_id = selectedScope` helps select results, but it does not establish authorization. The database must reject access to another scope even if the caller changes or removes that filter.

Review policies separately for reads, inserts, updates, and deletes. For updates, check both access to the existing row and permission for the resulting row, including any changed scope.

### Keep bypass credentials on the server

Credentials that bypass row-level security must never reach browser code, public bundles, or client-visible configuration.

For every operation using a privileged client:

- Authenticate the caller.
- Authorize the requested operation.
- Validate the target records and their scope against the caller's permissions.

A supplied scope identifier is input to validate, not evidence of permission.

## Translate migration writes deliberately

Replace replacement-style writes with explicit upserts whose conflict columns match the destination schema:

```ts
.upsert(row, { onConflict: 'scope_id,item_id' })
```

The conflict target must correspond to a primary key or unique constraint. Check whether the source replacement operation deleted and recreated rows, and whether callers depended on resulting defaults, triggers, or cascading changes. An upsert is not automatically equivalent to those behaviors.

Before accepting a migration, verify value ranges, temporal conversions, key uniqueness, foreign-key validity, and conflict behavior.

## Type query results and map them explicitly

Use query-interface annotations for result shapes rather than double casts through `unknown`:

```ts
.select('*').returns<RowType[]>()
```

Keep `RowType` aligned with the selected database columns and their nullability. A type annotation describes the expected result; it does not validate runtime data or repair a mismatched query.

Use a dedicated mapper to translate database naming into application naming:

```ts
export interface RowType {
  scope_id: string;
  item_id: string;
  observed_on: string | null;
}

export interface Item {
  scopeId: string;
  itemId: string;
  observedOn: string | null;
}

export function mapItem(row: RowType): Item {
  return {
    scopeId: row.scope_id,
    itemId: row.item_id,
    observedOn: row.observed_on,
  };
}
```

Export row mappers from a shared package so consumers reuse the same conversions. Inventory tables exposed to application code and verify mapper coverage, including nullable fields and partial query projections.

## Handle absence and aggregation deliberately

Use `.maybeSingle()` when a query expects zero or one row and absence is acceptable. Handle a missing row separately from a query error. Multiple matching rows remain an error and may indicate a missing uniqueness constraint.

Perform application-side aggregation only when the dataset has a known, manageable bound. Retrieve every required page using deterministic ordering, and account for concurrent changes if the total must represent a consistent snapshot. A successful first page does not prove that the dataset is complete.

For large or unbounded datasets, aggregate in the database and return the resulting totals.
