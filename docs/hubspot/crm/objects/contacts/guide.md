> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Contacts API

> Contact records store information about individuals. The contacts endpoints allow you to manage this data and sync it between HubSpot and other systems.

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

In HubSpot, contacts store information about the individual people that interact with your business. The contacts endpoints allow you to create and manage contact records in your HubSpot account, as well as sync contact data between HubSpot and other systems.

Learn more about objects, records, properties, and associations APIs in the [Understanding the CRM](/docs/api-reference/latest/crm/understanding-the-crm) guide. For more general information about objects and records in HubSpot, [learn how to manage your CRM database](http://knowledge.hubspot.com/contacts-user-guide).

## Create contacts

To create new contacts:

* To create one contact, make a `POST` request to `/crm/objects/2026-09/contacts`.
* To create multiple contacts, make a `POST` request to `/crm/objects/2026-09/contacts/batch/create`.

In your request, include your contact data in a [`properties`](#create-contacts-with-property-values) object. You can also add an [`associations`](#create-contacts-with-associations) object to associate your new contact with existing records (e.g., companies, deals), or activities (e.g., meetings, notes).

<Info>
  For batch create actions, you can enable multi-status errors which tell you which records were successfully created and which were not. Learn more about [setting up multi-status error handling](/docs/api-reference/error-handling#multi-status-errors).
</Info>

### Create contacts with property values

When creating a contact, you must include contact properties to store the contact's details. There are [default HubSpot contact properties](https://knowledge.hubspot.com/properties/hubspots-default-contact-properties), but you can also [create custom contact properties](https://knowledge.hubspot.com/properties/create-and-edit-properties).

For example, to create a new contact, your request may look similar to the following:

```json theme={null}
{
  "properties": {
    "email": "example@hubspot.com",
    "firstname": "Jane",
    "lastname": "Doe"
  }
}
```

When creating a new contact, it's required to include at least one of the following properties:

| Property | Type | Description |
| - | - | - |
| `email` | `string` | The contact's email address. It's recommended to always include `email`, because email address is the [primary unique identifier](https://knowledge.hubspot.com/records/deduplication-of-records#automatic-deduplication-in-hubspot) to avoid duplicate contacts in HubSpot. |
| `firstname` | `string` | The contact's first name. |
| `lastname` | `string` | The contact's last name. |

You can also include other properties as needed. Expand the section below to view a list of commonly used properties.

<Accordion title="Recommended properties">
  <ResponseField name="lifecyclestage" type="enumeration">
    The contact's [lifecycle stage](https://knowledge.hubspot.com/records/use-lifecycle-stages). Default options include `subscriber`, `lead`, `marketingqualifiedlead`, `evangelist`, `salesqualifiedlead`, `opportunity`, and `customer`.

    To retrieve custom lifecycle stage values, make a `GET` request to `crm/properties/2026-09/0-1/lifecyclestage`.
  </ResponseField>

  <ResponseField name="phone" type="string">
    The contact's phone number.
  </ResponseField>

  <ResponseField name="mobilephone" type="string">
    The contact's mobile phone number.
  </ResponseField>

  <ResponseField name="fax" type="string">
    The contact's fax number.
  </ResponseField>

  <ResponseField name="jobtitle" type="string">
    The contact's job title.
  </ResponseField>

  <ResponseField name="address" type="string">
    The contacts' street address.
  </ResponseField>

  <ResponseField name="city" type="string">
    The city in which the contact is located.
  </ResponseField>

  <ResponseField name="state" type="string">
    The state in which the contact is located,
  </ResponseField>

  <ResponseField name="country" type="string">
    The country in which the contact is located.
  </ResponseField>

  <ResponseField name="zip" type="string">
    The postal code in which the contact is located.
  </ResponseField>

  <ResponseField name="hs_timezone" type="enumeration">
    The time zone in which the contact is located. This can be set manually or automatically based on a contact's IP address.

    To retrieve all available time zone values, make a `GET` request to `crm/properties/2026-09/0-1/hs_timezone`.
  </ResponseField>
</Accordion>

To view all available contact properties in your account, make a `GET` request to `/crm/properties/2026-09/0-1`. Learn more about the [properties API](/docs/api-reference/latest/crm/properties/guide).

<Warning>
  When including enumeration properties, you must use internal names to set values. The internal name stays the same even if you've changed a default value's label.
</Warning>

### Create contacts with associations

When creating a new contact, you can also associate the contact with [existing records](https://knowledge.hubspot.com/records/associate-records) or [activities](https://knowledge.hubspot.com/records/associate-activities-with-records) by including an associations object.

In the associations object, you should include the following:

| Parameter | Description |
| - | - |
| `to` | The record or activity you want to associate with the contact, specified by its unique `id` value. |
| `types` | The type of the association between the contact and the record/activity. Include the `associationCategory`and `associationTypeId`. Default association type IDs are listed on the [associations API guide](/docs/api-reference/latest/crm/associations/associate-records/guide#association-type-id-values), or you can retrieve the value for custom association types (i.e. labels) via the [associations API](/docs/api-reference/latest/crm/associations/associate-records/guide#retrieve-association-types). |

For example, to associate a new contact with an existing company and email, your request would look like the following:

```json theme={null}
{
  "properties": {
    "email": "example@hubspot.com",
    "firstname": "Jane",
    "lastname": "Doe",
    "phone": "+18884827768",
    "company": "HubSpot",
    "website": "hubspot.com",
    "lifecyclestage": "marketingqualifiedlead"
  },
  "associations": [
    {
      "to": {
        "id": 123456
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 279
        }
      ]
    },
    {
      "to": {
        "id": 556677
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 197
        }
      ]
    }
  ]
}
```

## Retrieve contacts

You can retrieve contacts individually or in batches. You can include the following query parameters in your request URLs to retrieve certain data.

| Parameter | Description |
| - | - |
| `properties` | A comma separated list of the properties to be returned in the response. If a requested property isn't defined, it won't be included in the response. If a requested property is defined but a contact doesn't have a value, it will be returned as `null`. |
| `propertiesWithHistory` | A comma separated list of the current and historical properties to be returned in the response. If a requested property isn't defined, it won't be included in the response. If a requested property is defined but a contact doesn't have a value, it will be returned as `null`. |
| `associations` | Supported when retrieving an individual contact or all contacts, a comma separated list of objects to retrieve associated IDs for. Any specified associations that don't exist will not be returned in the response. Learn more about the [associations API.](/docs/api-reference/latest/crm/associations/associate-records/guide) |

### Retrieve an individual contact

You can retrieve individual contacts using the contact's Record ID value or their email address.

* To retrieve an individual contact by Record ID, make a `GET` request to `/crm/objects/2026-09/contacts/{recordId}`.
* To retrieve a contact by their email address, make a `GET` request to `/crm/objects/2026-09/contacts/{email}?idProperty=email`.

To retrieve contacts based on other property values, use the [search API](/docs/api-reference/latest/crm/search-the-crm).

### Retrieve all contacts

To request a list of all contacts, make a `GET` request to `/crm/objects/2026-09/contacts`.

You can retrieve up to 100 contacts in one request.

* To retrieve a specific amount under 100, add a value to the `limit` parameter. For example, `?limit=50`.
* To retrieve additional contacts in subsequent requests (i.e. the contacts after the limit was reached in your request), include the `after` parameter with the `after` value returned from the previous request. This value is the Record ID of the next contact. For example, `?after=123456`.

For example, to retrieve 50 contacts, your request URL would be `GET` `/crm/objects/2026-09/contacts?limit=50`. In your response, under the `paging` object below the list of returned contacts, the `after` value is the `id` of the next contact that would've been returned. To request 50 more contacts, starting with the next returned value, make a `GET` request to `/crm/objects/2026-09/contacts?limit=50&after={id}`.

The `after` field is highlighted in the example response below:

```json highlight={20} theme={null}
{
  "results": [
    {
      "id": "33451",
      "properties": {
        "createdate": "2022-06-01T14:31:48.469Z",
        "email": "lorelai@thedragonfly.com",
        "firstname": "Lorelai",
        "hs_object_id": "33451",
        "lastmodifieddate": "2025-07-07T20:27:17.947Z",
        "lastname": "Gilmore"
      },
      "createdAt": "2022-06-01T14:31:48.469Z",
      "updatedAt": "2025-07-07T20:27:17.947Z",
      "archived": false
    }
  ],
  "paging": {
    "next": {
      "after": "33452",
      "link": "https://api.hubspot.com/crm/objects/v3/contacts?limit=1"
    }
  }
}
```

### Retrieve a batch of contacts

When retrieving contacts in batches, you can request contacts by their Record ID (`id`), email address (`email`), or by a [custom unique identifier property](/docs/api-reference/latest/crm/properties/guide#create-unique-identifier-properties). To request a batch of contacts, make a `POST` request to `crm/objects/2026-09/contacts/batch/read`.

For the batch read endpoint, to retrieve by email or custom [unique identifier property](/docs/api-reference/latest/crm/properties/guide#create-unique-identifier-properties), you must use the  `idProperty`. By default, the `id` values in the request refer to the Record ID, so the `idProperty` parameter is not required when retrieving by Record ID, but always required when retrieving by email or a custom unique ID property.

<Warning> The batch endpoint <u>cannot</u> retrieve associations. To view associations for a specific batch of contacts, you must retrieve the contacts' `id` values first, then include them in a `GET` request to the batch read associations API endpoint. Learn how to retrieve associations with the [associations API](/docs/api-reference/latest/crm/associations/associate-records/guide#retrieve-associations).</Warning>

For example, to retrieve a batch of contacts based on their record ID values, your request could look like the following (current values only, or current and historical values):

<Tabs>
  <Tab title="Retrieve by Record ID with properties">
    ```json theme={null}
    {
      "properties": ["email", "lifecyclestage", "jobtitle"],
      "inputs": [
        {
          "id": "1234567"
        },
        {
          "id": "987456"
        }
      ]
    }
    ```
  </Tab>

  <Tab title="Retrieve by Record ID with property history">
    ```json theme={null}
    {
      "propertiesWithHistory": ["lifecyclestage", "hs_lead_status"],
      "inputs": [
        {
          "id": "1234567"
        },
        {
          "id": "987456"
        }
      ]
    }
    ```
  </Tab>
</Tabs>

To retrieve contacts based on their email address or value for a custom unique identifier property (e.g., a customer ID number unique for your business), your request would look like:

<Tabs>
  <Tab title="Retrieve by email">
    ```json theme={null}
    {
      "properties": ["email", "lifecyclestage", "jobtitle"],
      "idProperty": "email",
      "inputs": [
        {
          "id": "lgilmore@thedragonfly.com"
        },
        {
          "id": "sstjames@thedragonfly.com"
        }
      ]
    }
    ```
  </Tab>

  <Tab title="Retrieve by custom identifier property">
    ```json theme={null}
    {
      "properties": ["email", "lifecyclestage", "jobtitle"],
      "idProperty": "internalcustomerid",
      "inputs": [
        {
          "id": "12345"
        },
        {
          "id": "67891"
        }
      ]
    }
    ```
  </Tab>
</Tabs>

## Update contacts

You can update contacts individually or in batches.

<Warning>
  If updating the `lifecyclestage` property, you can only set the value <u>forward</u> in the stage order. To set the lifecycle stage backward, you'll first need to clear the record's existing lifecycle stage value. The value can be [cleared manually](https://knowledge.hubspot.com/records/update-a-property-value-for-a-record), or may be automatically cleared via a [workflow](https://knowledge.hubspot.com/records/change-record-lifecycle-stages-in-bulk) or an integration that syncs contact data.
</Warning>

### Update an individual contact

To update individual contacts, you can use Record ID (`id`) or the contact's email address (`email`).

* To update an individual contact by its Record ID, make a `PATCH` request to `/crm/objects/2026-09/contacts/{contactId}`, and include the data you want to update.
* To update an individual contact by its email, make a `PATCH` request to `/crm/objects/2026-09/contacts/{email}?idProperty=email`, and include the data you want to update.

For example:

```json theme={null}
{
  "properties": {
    "favorite_food": "burger",
    "jobtitle": "Manager",
    "lifecyclestage": "customer"
  }
}
```

### Update a batch of contacts

To update contacts in batches, you must use the contacts' Record ID values (`id`).

To update multiple contacts, make a `POST` request to `/crm/objects/2026-09/contacts/batch/update`. In your request body, include each contact's Record ID as the `id` ​and include the properties you want to update.

For example:

```json theme={null}
{
  "inputs": [
    {
      "id": "123456789",
      "properties": {
        "favorite_food": "burger"
      }
    },
    {
      "id": "56789123",
      "properties": {
        "favorite_food": "Donut"
      }
    }
  ]
}
```

## Upsert contacts

You can also batch create and update contacts at the same time using the upsert endpoint. For this endpoint, you can use `email` or a [custom unique identifier property](/docs/api-reference/latest/crm/properties/guide#create-unique-identifier-properties). Following the request, if the contacts already exist, they'll be updated and if the contacts don't exist, they'll be created.

To upsert contacts, make a `POST` request to `/crm/objects/2026-09/contacts/batch/upsert`. In your request body, include the `idProperty` parameter to identify whether you're using `email` or a custom unique identifier property. Include that property's value as the `id` ​and add the other properties you want to set or update.

<Warning>
  Partial upserts are not supported when using `email` as the `idProperty` for contacts. To complete a partial upsert, use a custom unique identifier property as the `idProperty` instead.
</Warning>

For example, your request could look like the following:

```json theme={null}
{
  "inputs": [
    {
      "properties": {
        "phone": "+18884827768"
      },
      "id": "test@test.com",
      "idProperty": "email"
    },
    {
      "properties": {
        "phone": "+18888888888"
      },
      "id": "example@hubspot.com",
      "idProperty": "email"
    }
  ]
}
```

## Merge contacts

To merge two contact records, make a `POST` request to `/crm/objects/2026-09/contacts/merge`. The remaining record combines activities, associations, and most property values from both records. For example, merge duplicate contacts to preserve historical context and consolidate their activity timelines. Learn more about [what happens when you merge HubSpot records](https://knowledge.hubspot.com/records/merge-records#what-happens-when-i-merge-records).

Include the following in your request body:

| Field | Description |
| - | - |
| `objectIdToMerge` | The record ID to merge with the primary record. |
| `primaryObjectId` | The record ID of the primary record, which is the record that will remain after the merge. |

For example, to merge the record `45678` into the record `12345`, your request would look like:

```json theme={null}
{
  "objectIdToMerge": "45678",
  "primaryObjectId": "12345"
}
```

In a successful merge response, the `id` is the record ID of the merged record.

<Warning>
  **Please note:** if an account is enrolled in the [*Primary ID Preservation for Merged Records* public beta](https://app.hubspot.com/l/product-updates/?rollout=318895), the primary (i.e., the remaining record after a merge) record's Record ID value (`primaryObjectId`) is preserved instead of generating a new one. Once enrolled, this behavior applies to all merges, including [in HubSpot](https://knowledge.hubspot.com/records/merge-records) and all versions of the API.
</Warning>

## Associate existing contacts with records or activities

To associate a contact with other CRM records or an activity, make a `PUT` request to `/crm/objects/2026-09/contacts/{contactId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.

<Info>
  To retrieve the `associationTypeId` value, refer to [this list](/docs/api-reference/latest/crm/associations/associate-records/guide#association-type-id-values) of default values, or make a `GET` request to `/crm/associations/2026-09/{fromObjectType}/{toObjectType}/labels`.
</Info>

Learn more about the [associations API.](/docs/api-reference/latest/crm/associations/associate-records/guide)

### Remove an association

To remove an association between a contact and a record or activity, make a `DELETE` request to the following URL: `/crm/objects/2026-09/contacts/{contactID}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`.

## Pin an activity on a contact record

You can [pin an activity](https://knowledge.hubspot.com/records/pin-an-activity-on-a-record) on a contact record by including the `hs_pinned_engagement_id` field in your request. In the field, include the `id` of the activity to pin, which can be retrieved via the [engagements APIs](/docs/api-reference/latest/overview). You can pin one activity per record, and the activity must already be associated with the contact prior to pinning.

To set or update a contact's pinned activity, your request could look like:

```json theme={null}
{
  "properties": {
    "hs_pinned_engagement_id": 123456789
  }
}
```

You can also create a contact, associate it with an existing activity, and pin the activity in the same request. For example:

```json theme={null}
{
  "properties": {
    "email": "example@hubspot.com",
    "firstname": "Jane",
    "lastname": "Doe",
    "phone": "+18884827768",
    "hs_pinned_engagement_id": 123456789
  },
  "associations": [
    {
      "to": {
        "id": 123456789
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 201
        }
      ]
    }
  ]
}
```

## Delete contacts

You can delete contacts individually or in batches, which will add the contact to the recycling bin in HubSpot. You can later [restore the contact within HubSpot](https://knowledge.hubspot.com/records/restore-deleted-records).

To delete an individual contact by its ID, make a `DELETE` request to `/crm/objects/2026-09/contacts/{contactId}`.

Learn more about batch deleting contacts in the [reference documentation](/docs/api-reference/latest/crm/objects/contacts/guide).

## Additional emails

Additional email addresses are used when a contact has more than one email. These can be added [manually on a contact record in HubSpot](https://knowledge.hubspot.com/records/add-multiple-email-addresses-to-a-contact) or can be added automatically following a [contact merge](https://knowledge.hubspot.com/records/merge-records#contact-merge-exceptions). Additional emails are still unique identifiers for contacts, so multiple contacts cannot have the same additional email addresses.

To view additional emails for contacts, when you retrieve all or individual contacts, include the `properties` parameter with the properties `email` and `hs_additional_emails`. A contact's primary email address will be displayed in the `email` field and additional emails will be displayed in the `hs_additional_emails` field.

## Limits

Batch operations are limited to 100 records at a time. For example, you cannot batch update more than 100 contacts in one request. There are also limits for [contacts and form submissions](https://developers.hubspot.com/docs#limits_contacts).
