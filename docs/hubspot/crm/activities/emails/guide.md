> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Emails API

> Use the email engagement API to log and manage emails on CRM records. 

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
  'crm.objects.contacts.write',
  'sales-email-read'
]}
  />
</Accordion>

Use the email engagement API to log and manage emails on CRM records. You can log email activities either [in HubSpot](https://knowledge.hubspot.com/records/manually-log-activities-on-records) or through the emails API.

## Create an email engagement

To create an email engagement, make a `POST` request to `/crm/objects/2026-09/emails`.

In the request body, add email details in a **properties** object. You can also add an **associations** object to associate your new email with an existing record (e.g., contacts, companies).

### Properties

In the properties object, you can include the following fields:

| Field | Description |
| - | - |
| `hs_timestamp` | Required. This field marks the email's time of creation and determines where the email sits on the record timeline. You can use either a Unix timestamp in milliseconds or UTC format. |
| `hubspot_owner_id` | The [ID of the owner](/docs/api-reference/latest/crm/owners/guide) associated with the email. This field determines the user listed as the email creator on the record timeline. |
| `hs_email_direction` | The direction the email was sent in. Possible values include:`EMAIL`: the email was sent from the CRM or sent and logged to the CRM with the [BCC address.](https://knowledge.hubspot.com/connected-email/log-email-in-your-crm-with-the-bcc-or-forwarding-address)`INCOMING_EMAIL`: the email was a reply to a logged outgoing email. `FORWARDED_EMAIL`: the email was [forwarded to the CRM.](https://knowledge.hubspot.com/connected-email/log-email-in-your-crm-with-the-bcc-or-forwarding-address) |
| `hs_email_html` | The body of an email if it is sent from a CRM record. |
| `hs_email_status` | The send status of the email. The value can be `BOUNCED`, `FAILED`, `SCHEDULED`, `SENDING`, or `SENT`. |
| `hs_email_subject` | The subject line of the logged email. |
| `hs_email_text` | The body of the email. |
| `hs_attachment_ids` | The IDs of the email's attachments. Multiple attachment IDs are separated by a semi-colon. |
| `hs_email_headers` | The email's headers. The value for this property will automatically populate certain read only email properties. Learn how to [set email headers.](/docs/api-reference/latest/crm/activities/emails/guide#set-email-headers) |

Learn more about batch creating email engagements by checking out the [reference documentation](/docs/api-reference/latest/crm/activities/emails/batch/create-emails).

### Read only properties

There are also some email properties that are read only, which are automatically populated by HubSpot. The properties in the table below are all automatically populated from the `hs_email_headers` value.

| Field | Description |
| - | - |
| `hs_email_from_email` | The email address of the email's sender. |
| `hs_email_from_firstname` | The email sender's first name. |
| `hs_email_from_lastname` | The email sender's last name. |
| `hs_email_to_email` | The email addresses of the email's recipients. |
| `hs_email_to_firstname` | The first names of the email's recipients. |
| `hs_email_to_lastname` | The last names of the email recipient. |

<Warning>
  **Please note:**

  When retrieving an email header, you may notice there are values both for `From` and `Sender`. These are often the same, but because `Sender` identifies what actually submitted an email, there are scenarios where the values may differ. For example, if an email is sent from an email alias, the `From` value will refer to the user's actual email address, and the `Sender` value will refer to the email alias.
</Warning>

### Set email headers

Since headers automatically populate the read only properties, you may want to manually set the email headers. To set the `hs_email_headers` value, you can use a JSON escaped string with the following data:

```json theme={null}
//Example data
{
  "from": {
    "email": "from@domain.com",
    "firstName": "FromFirst",
    "lastName": "FromLast"
  },
  "to": [
    {
      "email": "ToFirst ToLast<to@test.com>",
      "firstName": "ToFirst",
      "lastName": "ToLast"
    }
  ],
  "cc": [],
  "bcc": []
}
```

For example, your request to create an email may look like:

```json theme={null}
//Example request body
{
  "properties": {
    "hs_timestamp": "2019-10-30T03:30:17.883Z",
    "hubspot_owner_id": "47550177",
    "hs_email_direction": "EMAIL",
    "hs_email_status": "SENT",
    "hs_email_subject": "Let's talk",
    "hs_email_text": "Thanks for your email",
    "hs_email_headers": "{\"from\":{\"email\":\"from@domain.com\",\"firstName\":\"FromFirst\",\"lastName\":\"FromLast\"},\"sender\":{\"email\":\"sender@domain.com\",\"firstName\":\"SenderFirst\",\"lastName\":\"SenderLast\"},\"to\":[{\"email\":\"ToFirst+ToLast<to@test.com>\",\"firstName\":\"ToFirst\",\"lastName\":\"ToLast\"}],\"cc\":[],\"bcc\":[]}"
  }
}
```

### Associations

To create and associate an email with existing records, include an associations object in your request. For example, to create an email and associate it with a deal and a contact, your request body might look like the following:

```json theme={null}
// Example request body
{
  "properties": {
    "hs_timestamp": "2019-10-30T03:30:17.883Z",
    "hubspot_owner_id": "11349275740",
    "hs_email_direction": "EMAIL",
    "hs_email_status": "SENT",
    "hs_email_subject": "Let's talk",
    "hs_email_text": "Thanks for your interest let's find a time to connect"
  },
  "associations": [
    {
      "to": {
        "id": 601
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 210
        }
      ]
    },
    {
      "to": {
        "id": 602
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 198
        }
      ]
    }
  ]
}
```

In the associations object, you should include the following:

| Field | Description |
| - | - |
| `to` | The record you want to associate with the email, specified by its unique `id` value. |
| `types` | The type of the association between the email and the record. Include the `associationCategory`and `associationTypeId`. Default association type IDs are listed [here](/docs/api-reference/latest/crm/associations/associate-records/guide#association-type-id-values), or you can retrieve the value for custom association types (i.e. labels) via the [associations API](/docs/api-reference/latest/crm/associations/associate-records/guide#retrieve-association-types). |

## Retrieve emails

You can retrieve emails individually or in bulk. Learn more about batch retrieval by checking out the [reference documentation](/docs/api-reference/latest/crm/activities/emails/batch/get-emails).

To retrieve an individual email by its email ID, make a `GET` request to `/crm/objects/2026-09/emails/{emailId}`. You can also include the following parameters in the request URL:

| Parameter | Description |
| - | - |
| `properties` | A comma separated list of the properties to be returned. If a requested property isn't defined, it won't be included in the response. If a requested property is defined but an email doesn't have a value, it will be returned as `null`. |
| `associations` | A comma separated list of object types to retrieve associated IDs for. Any specified associations that don't exist will not be returned in the response. Learn more about the [associations API.](/docs/api-reference/latest/crm/associations/associate-records/guide) |

To request a list of all of emails, make a `GET` request to `/crm/objects/2026-09/emails`. You can include the following parameters in the request URL:

| Parameter | Description |
| - | - |
| `limit` | The maximum number of results to display per page. |
| `properties` | A comma separated list of the properties to be returned.If a requested property isn't defined, it won't be included in the response. If a requested property is defined but an email doesn't have a value, it will be returned as `null`. |

## Update emails

You can update emails individually or in batches. To update an individual email by its email ID, make a `PATCH` request to `/crm/objects/2026-09/emails/{emailId}`.

In the request body, include the email properties that you want to update. For example, your request body might look similar to the following:

```json theme={null}
// Example request body
{
  "properties": {
    "hs_timestamp": "2019-10-30T03:30:17.883Z",
    "hubspot_owner_id": "11349275740",
    "hs_email_direction": "EMAIL",
    "hs_email_status": "SENT",
    "hs_email_subject": "Let's talk tomorrow",
    "hs_email_text": "Thanks for your interest let's find a time to connect!"
  }
}
```

HubSpot will ignore values for read-only and non-existent properties. To clear a property value, pass an empty string for the property in the request body.

Learn more about batch updating by checking out the [reference documentation](/docs/api-reference/latest/crm/activities/emails/batch/update-emails).

### Associate existing emails with records

To associate an email with records, such as a contact and its associated companies, make a `PUT` request to `/crm/objects/2026-09/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`. The request URL contains the following fields:

| Field | Description |
| - | - |
| `emailId` | The ID of the email. |
| `toObjectType` | The type of object that you want to associate the email with (e.g., contact or company) |
| `toObjectId` | The ID of the record that you want to associate the email with. |
| `associationTypeId` | A unique identifier to indicate the association type between the email and the other object. The ID can be represented numerically or in snake case (e.g., `email_to_contact`). You can retrieve the value through the [associations API](/docs/api-reference/latest/crm/associations/associate-records/guide). |

For example, your request URL might look similar to the following:

`https://api.hubspot.com/crm/objects/2026-09/emails/17691787884/associations/contact/104901/198`

### Remove an association

To remove an association between an email and a record, make a `DELETE` request to the same URL as above:

`/crm/objects/2026-09/emails/{emailId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

## Pin an email on a record

You can [pin an email](https://knowledge.hubspot.com/records/pin-an-activity-on-a-record) on a record so it remains on the top of the record's timeline. The email must already be associated with the record prior to pinning, and you can only pin one activity per record. To pin an email, include the email's `id` in the `hs_pinned_engagement_id` field when creating or updating a record via the object APIs. Learn more about using the [companies,](/docs/api-reference/latest/crm/objects/companies/guide#pin-an-activity-on-a-company-record)[contacts](/docs/api-reference/latest/crm/objects/contacts/guide#pin-an-activity-on-a-contact-record), [deals](/docs/api-reference/latest/crm/objects/deals/guide#pin-an-activity-on-a-deal-record), [tickets](/docs/api-reference/latest/crm/objects/tickets/guide#pin-an-activity-on-a-ticket-record), and [custom objects](/docs/api-reference/latest/crm/objects/custom-objects/guide) APIs.

## Delete emails

When you delete an email, it is permanently deleted and <u>cannot</u> be restored. You can delete emails individually or in batches.

To delete an individual email by its email ID, make a `DELETE` request to `/crm/objects/2026-09/emails/{emailId}`.

Learn more about deleting emails by checking out the [reference documentation](/docs/api-reference/latest/crm/activities/emails/delete-email).
