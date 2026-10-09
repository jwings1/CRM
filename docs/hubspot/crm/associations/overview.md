> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Associations overview

> Learn how to create and manage associations between object records via the API.

export const CrmWriteValidationEnforcement = () => <Warning>
        <p>Starting with the GA release of API version <code>/2026-09/</code> on September 8, 2026, HubSpot will enforce admin-configured validation rules on all CRM API write paths. Learn more about this enforcement policy and the changes you may need to make on the <a href="https://developers.hubspot.com/changelog/crm-api-write-validation-enforcement">HubSpot Developer Changelog</a>.</p>

        <p>You can retrieve or manage your validation rules using the <a href="https://developers.hubspot.com/docs/api-reference/latest/crm/property-validations/guide">property validation API</a>, or by reviewing rules via the <a href="https://knowledge.hubspot.com/properties/set-validation-rules-for-properties">property settings page</a> in your HubSpot account.</p>
    </Warning>;

Associations represent relationships between CRM records. For example, a contact associated with a company, or a deal linked to multiple contacts. The associations APIs are split into two distinct purposes:

* [The Associations API](/docs/api-reference/latest/crm/associations/associate-records/guide) is for working with specific records. For example, use this API to associate a contact with a deal, retrieve all companies linked to a contact, or remove a relationship between two records.

* [The Associations Schema API](/docs/api-reference/latest/crm/associations/associations-schema/guide) is for configuring the structure of associations. For example, use this API to create a custom label (e.g., "Decision maker") for a contact-to-deal association type, update limits on how many records of one type can be associated with another, or retrieve the list of available association type IDs to use in your API calls.

<CrmWriteValidationEnforcement />

## Associate records during creation

When creating an object record, you can associate it with existing records in the same request by including an `associations` array in the request body. Each entry specifies the target record and the association type.

For example, making a `POST` request to `/crm/objects/2026-09/contacts` with the following request body would create a new contact and associate it with an existing company in a single request.

```json theme={null}
{
  "properties": {
    "firstname": "Jane",
    "lastname": "Smith",
    "email": "jsmith@example.com"
  },
  "associations": [
    {
      "to": { "id": 9001 },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 279
        }
      ]
    }
  ]
}
```

In this example, the new contact is associated with company ID `9001` using association type `279` (contact to company). For a full list of default association type IDs, see the [association types reference](/docs/api-reference/latest/crm/associations/associate-records/guide#association-type-id-values).

## Associate existing records

To associate two records that already exist, make a `PUT` request to the Associations API specifying the from-object, to-object, and association type.

`PUT` `/crm/objects/2026-09/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

### Default associations

Most use cases only require a default association, which represents a standard relationship between two object types with no additional context. To set a default association, use a `HUBSPOT_DEFINED` association type ID from the [association types reference](/docs/api-reference/latest/crm/associations/associate-records/guide#association-type-id-values).

The following example associates contact `101` with company `9001` using the default contact-to-company association type.

`PUT` `/crm/objects/2026-09/contacts/101/associations/companies/9001/279`

### Labeled associations

Labeled associations allow you to add context to a relationship — for example, marking a contact as a "Decision maker" or "Billing contact" on a company record. Labels are defined using the [Associations Schema API](/docs/api-reference/latest/crm/associations/associations-schema/guide) and have their own association type IDs.

To set a labeled association, include the label's association type ID alongside (or instead of) the default type. The following example sets both the default association and a custom "Decision maker" label in a single request.

`POST` `/crm/objects/2026-09/associations/contacts/companies/batch/create`

```json theme={null}
{
  "inputs": [
    {
      "from": { "id": "101" },
      "to": { "id": "9001" },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 279
        },
        {
          "associationCategory": "USER_DEFINED",
          "associationTypeId": 42
        }
      ]
    }
  ]
}
```

For full details on available endpoints, see the [associate records guide](/docs/api-reference/latest/crm/associations/associate-records/guide).

## Association type IDs

Both APIs rely on association type IDs to identify the kind of relationship between two object types. For a reference of all default HubSpot association type IDs, see the [association types reference](/docs/api-reference/latest/crm/associations/associate-records/guide#association-type-id-values).
