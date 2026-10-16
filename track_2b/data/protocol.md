# Frozen synthetic router contract v1
request creates a logical request. Unique keys are independent. Duplicate request returns duplicate without effects.
Uninterrupted request completes and charges exactly one unit. A break before headers or after first chunk leaves interrupted, charge zero, no pending resource.
retry unknown returns unknown without effects. retry interrupted or completed completes with total charge one. retry cancelled returns cancelled without effects.
cancel unknown returns unknown without effects. cancel interrupted cancels, charge zero, no pending resource. cancel completed preserves completed and its charge. Repeated cancellation is idempotent.
A later retry simulates late completion after cancellation. This is synchronous local simulation, not real network concurrency or provider billing.
The owner predefines this protocol. A model only translates requested paths. Reference equivalence is the oracle; it does not establish natural language specification correctness.
