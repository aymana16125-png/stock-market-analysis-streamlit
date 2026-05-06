```mermaid
flowchart LR
    U((User))
    UC1[Search stock symbol]
    UC2[View current price]
    UC3[View historical prices]
    UC4[View trend chart]
    UC5[Handle invalid symbol]

    U --> UC1
    U --> UC2
    U --> UC3
    U --> UC4
    U --> UC5
```
