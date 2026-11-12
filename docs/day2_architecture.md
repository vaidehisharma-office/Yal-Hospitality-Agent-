# YAL Hospitality Agent v0.1 — Architecture

## Architecture Diagram

```mermaid
flowchart TD
    A["Guest Message"] --> B["AgentRequest Validation"]
    B --> C["Gemma Intent Classifier"]
    C --> D{"Classification Successful?"}

    D -->|No| E["Return Error Response"]
    D -->|Yes| F{"Emergency?"}

    F -->|Yes| G["Return Emergency Safety Guidance"]
    F -->|No| H{"Clarification Needed?"}

    H -->|Yes| I["Ask Guest for Clarification"]
    H -->|No| J{"Select Action by Intent"}

    J -->|HOUSEKEEPING| K["Create Housekeeping Request"]
    J -->|MAINTENANCE| L["Create Maintenance Request"]
    J -->|COMPLAINT| M["Contact Front Desk"]
    J -->|INFORMATION| N["Return Information Response"]
    J -->|Other| O["Return Unsupported Request Response"]

    K --> P["Tool Result"]
    L --> P
    M --> P

    P --> Q{"Tool Successful?"}
    Q -->|Yes| R["Return Ticket ID and Confirmation"]
    Q -->|No| S["Return Failure Response"]

