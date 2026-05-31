# Contrats de données - TP8

## OrderRequest

{
  "customer_id": "C001",
  "city": "Fes",
  "items": [
    {
      "product_id": "P001",
      "quantity": 2
    }
  ],
  "created_at": "2026-05-31T12:00:00"
}

## OrderEvent

{
  "event_id": "evt-001",
  "order_id": "ord-001",
  "event_type": "order_created",
  "city": "Fes",
  "status": "created",
  "timestamp": "2026-05-31T12:00:00"
}

## Règles de validation

- customer_id est obligatoire ;
- city est obligatoire ;
- items ne doit pas être vide ;
- quantity doit être positive ;
- timestamp doit être valide ;
- event_type doit appartenir à la liste autorisée.
