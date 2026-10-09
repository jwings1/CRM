> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Notes API

> Use the notes engagement API to log and manage notes on CRM records.

export const ScopesList = ({scopes = [], description = "This API requires one of the following scopes:"}) => {
  if (!scopes || scopes.length === 0) {
    return null;
  }
  const sortedScopes = scopes.sort((a, b) => a.localeCompare(b));
  return <div>
      <div className="text-sm mb-2">{description}</div>
      <div>
        {sortedScopes.map((scope, index) => <div key={index}>
            <code>
              <span className="text-xs">{scope}</span>
            </code>
          </div>)}
      </div>
    </div>;
};

<Accordion title="Required Scopes" icon="key">
  <ScopesList
    scopes={[
  'crm.objects.contacts.read',
  'crm.objects.contacts.write'
]}
  />
</Accordion>

You can log notes on CRM records to add information to the record timeline or associate an attachment with a record. For example, if you need to keep track of an offline conversation you had with a contact, you can add a note to their contact record with details and documents related to the conversation. Other users in the account will then be able to view and reference that note.

You can manage notes either [in HubSpot](https://knowledge.hubspot.com/records/manually-log-activities-on-records) or through the notes API. Below, learn the basic methods of managing notes through the API.

## Create a note

To create a note, make a `POST` request to `/crm/objects/2026-09/notes`.

In the request body, add note details in a `properties` object. You can also add an `associations` object to associate your new note with an existing record (e.g., contacts, companies).

### Properties

In the properties object, you can include the following fields:

| Field | Description |
| - | - |
| `hs_timestamp` | Required. This field marks the note's time of creation and determines where the note sits on the record timeline. You can use either a Unix timestamp in milliseconds or UTC format. |
| `hs_note_body` | The note's text content, limited to 65,536 characters. |
| `hubspot_owner_id` | The [ID of the owner](/docs/api-reference/latest/crm/owners/guide) associated with the note. This field determines the user listed as the note creator on the record timeline in HubSpot. |
| `hs_attachment_ids` | The IDs of the note's attachments. Multiple attachment IDs are separated by a semi-colon. |

### Associations

To create and associate a note with existing records, include an associations object in your request. For example, to create a note and associate it with a company and deal, your request body might look similar to the following:

```json theme={null}
{
  "properties": {
    "hs_timestamp": "2021-11-12T15:48:22Z",
    "hs_note_body": "Spoke with decision maker Carla. Attached the proposal and draft of contract.",
    "hubspot_owner_id": "14240720",
    "hs_attachment_ids": "24332474034;24332474044"
  },
  "associations": [
    {
      "to": {
        "id": 301
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 190
        }
      ]
    },
    {
      "to": {
        "id": 401
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 214
        }
      ]
    }
  ]
}
```

In the associations object, you should include the following:

| Field | Description |
| - | - |
| `to` | The record you want to associate with the note, specified by its unique `id` value. |
| `types` | The type of the association between the note and the record. Include the `associationCategory`and `associationTypeId`. Default association type IDs are listed [here](/docs/api-reference/latest/crm/associations/associate-records/guide#association-type-id-values), or you can retrieve the value for custom association types (i.e. labels) via the [associations API](/docs/api-reference/latest/crm/associations/associate-records/guide#retrieve-association-types). |

Learn more about batch creating notes in the [reference documentation](/docs/api-reference/latest/crm/activities/notes/batch/create-notes).

## Retrieve notes

You can retrieve notes individually or in batches. To retrieve an individual note, make a `GET` request to `/crm/objects/2026-09/notes/{noteId}`.

To request a list of all notes, make a `GET` request to `/crm/objects/2026-09/notes`.

For both endpoints, you can include the following query parameters in the request URL:

| Parameter | Description |
| - | - |
| `properties` | A comma separated list of the properties to be returned in the response. If a requested property isn't defined, it won't be included in the response. If a requested property is defined but a note doesn't have a value, it will be returned as `null`. |
| `associations` | A comma separated list of object types to retrieve associated IDs for. Any specified associations that don't exist will not be returned in the response. Learn more about the [associations API.](/docs/api-reference/latest/crm/associations/associate-records/guide) |

For example, to retrieve notes with their text content and any associated contact IDs, your request URL might look similar to the following:

`https://api.hubapi.com/crm/objects/2026-09/notes?limit=10&properties=hs_note_body&associations=contact&archived=false`.

Learn more about retrieving a batch of notes by internal ID or unique property value in the [reference documentation](/docs/api-reference/latest/crm/activities/notes/batch/get-notes).

## Update notes

You can update notes individually or in batches. To update an individual note by its note ID, make a `PATCH` request to `/crm/objects/2026-09/notes/{noteId}`.

In the request body, include the note properties that you want to update:

```json theme={null}
{
  "properties": {
    "hs_note_body": "Spoke with decision maker Carla.",
    "hs_attachment_ids": "24332474034;24332474044"
  }
}
```

HubSpot will ignore values for read-only and non-existent properties. To clear a property value, pass an empty string for the property in the request body.

Learn more about batch updating notes in the [reference documentation](/docs/api-reference/latest/crm/activities/notes/create-note).

### Associate existing notes with records

To associate a note with other CRM records, such as a contact, make a `PUT` request to `/crm/objects/2026-09/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`. The request URL contains the following fields:

| Field | Description |
| - | - |
| `noteId` | The ID of the note. |
| `toObjectType` | The type of object that you want to associate the note with (e.g., contact or company) |
| `toObjectId` | The ID of the record that you want to associate the note with. |
| `associationTypeId` | A unique identifier to indicate the association type between the note and the other object. The ID can be represented numerically or in snake case (e.g., `note_to_contact`). You can retrieve the value through the [associations API](/docs/api-reference/latest/crm/associations/associate-records/guide). |

For example, your request URL might look similar to the following:

`https://api.hubspot.com/crm/objects/2026-09/notes/17147287858/associations/contact/581751/202`

### Remove an association

To remove an association between a note and a record, make a `DELETE` request to the same URL as above:

`/crm/objects/2026-09/notes/{noteId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

## Pin a note on a record

You can [pin a note](https://knowledge.hubspot.com/records/pin-an-activity-on-a-record) on a record so it remains on the top of the record's timeline. The note must already be associated with the record prior to pinning, and you can only pin one activity per record. To pin a note, include the note's `id` in the `hs_pinned_engagement_id` field when creating or updating a record via the object APIs. Learn more about using the [companies,](/docs/api-reference/latest/crm/objects/companies/guide#pin-an-activity-on-a-company-record)[contacts](/docs/api-reference/latest/crm/objects/contacts/guide#pin-an-activity-on-a-contact-record), [deals](/docs/api-reference/latest/crm/objects/deals/guide#pin-an-activity-on-a-deal-record), [tickets](/docs/api-reference/latest/crm/objects/tickets/guide#pin-an-activity-on-a-ticket-record), and [custom objects](/docs/api-reference/latest/crm/objects/custom-objects/guide) APIs.

## Delete notes

You can delete notes individually or in batches, which will add the note to the recycling bin in HubSpot. You can later [restore the note from the record timeline](https://knowledge.hubspot.com/records/restore-deleted-activity-in-a-record).

To delete an individual note by its note ID, make a `DELETE` request to `/crm/objects/2026-09/notes/{noteId}`.

Learn more about deleting notes in the [reference documentation](https://developers.hubspot.com/docs/api-reference/crm-notes-v3/basic/delete-crm-v3-objects-notes-noteId).
