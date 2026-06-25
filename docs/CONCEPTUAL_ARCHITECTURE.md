# Conceptual Architecture

```mermaid
flowchart LR
    A[Strategy signal] --> B[Market state observer]
    B --> C[Stress-regime classifier]
    C --> D[Risk governor]
    D --> E{Exposure decision}
    E -->|Allow| F[Normal execution boundary]
    E -->|Reduce| G[Reduced exposure]
    E -->|Pause| H[Cooldown / no-trade]
    E -->|Block| I[Kill switch]
    F --> J[Monitoring and evidence]
    G --> J
    H --> J
    I --> J
```

This is a conceptual research architecture. It is not an operational EA and does not imply validated performance.

## Responsibilities

- The strategy signal proposes possible participation.
- The market state observer describes current conditions.
- The stress classifier assigns a causal state.
- The risk governor maps that state into exposure decisions.
- Monitoring records what happened so the shield can be audited later.
