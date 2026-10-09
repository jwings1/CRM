> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Calls API

> Use the calls engagement API to log and manage calls on CRM records. 

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

Use the calls engagement API to log and manage calls on CRM records and on the [calls index page](https://knowledge.hubspot.com/records/view-and-filter-records). You can log calls either [in HubSpot](https://knowledge.hubspot.com/records/manually-log-activities-on-records) or through the calls API. Below, learn the basic methods of managing calls through the API.

## Create a call engagement

To create a call engagement, make a `POST` request to `/crm/objects/2026-09/calls`.

In the request body, add call details in a **properties** object. You can also add an **associations** object to associate your new call with an existing record (e.g.,contacts, companies).

### Properties

Below is a list of HubSpot default calling properties that you can include in the properties object. You can also create custom properties using the [properties API](/docs/api-reference/latest/crm/properties/guide).

| Field | Description |
| - | - |
| `hs_timestamp` | Required. This field marks the call's time of creation and determines where the call sits on the record timeline. You can use either a Unix timestamp in milliseconds or UTC format. |
| `hs_call_body` | The description of the call, including any notes that you want to add. |
| `hs_call_callee_object_id` | The ID of the HubSpot record associated with the call. This will be the recipient of the call for `OUTBOUND` calls, or the dialer of the call for `INBOUND` calls. |
| `hs_call_callee_object_type` | The type of the object to which the call's associated record belongs (e.g., specifies if the record is a contact or company). This will be the object of the recipient for `OUTBOUND`calls, or the object of the dialer for `INBOUND` calls. |
| `hs_call_direction` | The direction of the call from the perspective of the HubSpot user. If the user is the call recipient, the direction should be set to `INBOUND`. If the user initiated the call, the direction should be set to `OUTBOUND`. |
| `hs_call_disposition` | The outcome of the call. To set the call disposition, you need to use the internal GUID value. If your account has set up [custom call outcomes](https://knowledge.hubspot.com/calling/create-custom-call-and-meeting-outcomes), you can find their disposition GUIDs using [this API](/docs/api-reference/latest/crm/objects/communications/guide#get-call-engagement-dispositions). The default HubSpot outcome labels and their internal values are:<ul><li>Busy: `9d9162e7-6cf3-4944-bf63-4dff82258764`</li><li>Connected: `f240bbac-87c9-4f6e-bf70-924b57d47db7`</li><li>Left live message: `a4c4c377-d246-4b32-a13b-75a56a4cd0ff`</li><li>Left voicemail: `b2cf5968-551e-4856-9783-52b3da59a7d0`</li><li>No answer: `73a0d17f-1163-4015-bdd5-ec830791da20`</li><li>Wrong number: `17b47fee-58de-441e-a44c-c6300d46f273`</li></ul> |
| `hs_call_duration` | The duration of the call in milliseconds. |
| `hs_call_from_number` | The phone number that the call was made from. |
| `hs_call_recording_url` | The URL that stores the call recording. URLS to .mp3 or .wav files can be played back on CRM records. Only HTTPS, secure URLs will be accepted. |
| `hs_call_status` | The status of the call. The statuses are `BUSY`, `CALLING_CRM_USER`, `CANCELED`, `COMPLETED`, `CONNECTING`, `FAILED`, `IN_PROGRESS`, `NO_ANSWER`, `QUEUED`, and `RINGING`. |
| `hs_call_title` | The title of the call. |
| `hs_call_source` | The source of the call. This is not required, but it is required to leverage the [recording and transcriptions pipeline](/docs/api-reference/latest/crm/extensions/calling-extensions/recordings-and-transcriptions#log-a-call-with-your-app-s-endpoint-using-the-engagements-api). If the property is set, it must be set to `INTEGRATIONS_PLATFORM`. |
| `hs_call_to_number` | The phone number that received the call. |
| `hubspot_owner_id` | The [ID of the owner](/docs/api-reference/latest/crm/owners/guide) associated with the call. This field determines the user listed as the call creator on the record timeline. |
| `hs_activity_type` | The type of call. The options are based on the [call types set in your HubSpot account.](https://knowledge.hubspot.com/meetings-tool/how-do-i-create-and-use-call-and-meeting-types) |
| `hs_attachment_ids` | The IDs of the call's attachments. Multiple attachment IDs are separated by a semi-colon. |

### Associations

To create and associate a call with existing records, include an associations object in your request. For example, to create a call and associate it with a contact and a ticket, your request body might look similar to the following:

```json theme={null}
{
  "properties": {
    "hs_timestamp": "2021-03-17T01:32:44.872Z",
    "hs_call_title": "Support call",
    "hubspot_owner_id": "11349275740",
    "hs_call_body": "Resolved issue",
    "hs_call_duration": "3800",
    "hs_call_from_number": "(857) 829 5489",
    "hs_call_to_number": "(509) 999 9999",
    "hs_call_recording_url": "https://api.twilio.com/2010-04-01/Accounts/TWILIO_ACCOUNT_SID_PLACEHOLDER/Recordings/RE3079ac919116b2d22",
    "hs_call_status": "COMPLETED"
  },
  "associations": [
    {
      "to": {
        "id": 500
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 194
        }
      ]
    },
    {
      "to": {
        "id": 1234
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 220
        }
      ]
    }
  ]
}
```

In the associations object, you should include the following:

| Field | Description |
| - | - |
| `to` | The record you want to associate with the call, specified by its unique `id` value. |
| `types` | The type of the association between the call and the record. Include the `associationCategory`and `associationTypeId`. Default association type IDs are listed [here](/docs/api-reference/latest/crm/associations/associate-records/guide#association-type-id-values), or you can retrieve the value for custom association types (i.e. labels) via the [associations API](/docs/api-reference/latest/crm/associations/associate-records/guide#retrieve-association-types). |

Learn more about batch creating calls by checking out the [reference documentation](/docs/api-reference/latest/crm/activities/calls/batch/create-calls).

## Retrieve calls

You can retrieve calls individually or in bulk. Learn more about batch retrieval by checking out the [reference documentation](/docs/api-reference/latest/crm/activities/calls/batch/get-calls).

To retrieve an individual call by its call ID, make a `GET` request to `/crm/objects/2026-09/calls/{callId}`. You can include the following parameters in the request URL:

| Parameter | Description |
| - | - |
| `properties` | A comma separated list of the [properties](#call-properties-1) to be returned. If a requested property isn't defined, it won't be included in the response. If a requested property is defined but a call doesn't have a value, it will be returned as `null`. |
| `associations` | A comma separated list of object types to retrieve associated IDs for. Any specified associations that don't exist will not be returned in the response. Learn more about the [associations API.](/docs/api-reference/latest/crm/associations/associate-records/guide) |

To request a list of all of calls, make a `GET` request to `/crm/objects/2026-09/calls`. You can include the following parameters in the request URL:

| Parameter | Description |
| - | - |
| `limit` | The maximum number of results to display per page. |
| `properties` | A comma separated list of the [properties](#call-properties-1) to be returned. If a requested property isn't defined, it won't be included in the response. If a requested property is defined but a call doesn't have a value, it will be returned as `null`. |

When you make a successful request, the response will include the `callId` which you can use to retrieve, update, and delete the call.

## Identify voicemails vs. recorded calls

For recorded calls and voicemails, a recording is stored in the `hs_call_recording_url` property. If your account has access to [inbound calling](https://knowledge.hubspot.com/calling/receive-calls-in-hubspot), to differentiate between calls that were completed and recorded vs. inbound calls with a voicemail, include the following properties in your request: `hs_call_status` and `hs_call_has_voicemail`.

If a call has a voicemail, the `hs_call_status` value will be `missed`, and the `hs_call_has_voicemail` value will be `true`. The `hs_call_has_voicemail` value will be `false` for an inbound call where no voicemail was left, or `null` if the call has a status other than missed.

## Update calls

You can update calls individually or in batches. To update an individual call by its call ID, make a `PATCH` request to `/crm/objects/2026-09/calls/{callId}`.

In the request body, include the call properties that you want to update:

```json theme={null}
//Example PATCH request to https://api.hubspot.com/crm/objects/2026-09/calls/{callID}
{
  "properties": {
    "hs_timestamp": "2021-03-17T01:32:44.872Z",
    "hs_call_title": "Discovery call",
    "hubspot_owner_id": "11349275740",
    "hs_call_body": " Decision maker out, will call back tomorrow",
    "hs_call_duration": "3800",
    "hs_call_from_number": "(857) 829 5489",
    "hs_call_to_number": "(509) 999 9999",
    "hs_call_recording_url": "https://api.twilio.com/2010-04-01/Accounts/TWILIO_ACCOUNT_SID_PLACEHOLDER/Recordings/RE3079ac919116b2d22",
    "hs_call_status": "COMPLETED"
  }
}'
```

HubSpot will ignore values for read-only and non-existent properties. To clear a property value, pass an empty string for the property in the request body.

Learn more about batch updating by checking out the [reference documentation](/docs/api-reference/latest/crm/activities/calls/batch/update-calls).

### Associate existing calls with records

To associate a call with records, such as a contact and its associated companies, make a `PUT` request to `/crm/objects/2026-09/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`. The request URL contains the following fields:

| Field | Description |
| - | - |
| `callId` | The ID of the call. |
| `toObjectType` | The type of object that you want to associate the call with (e.g., contact or company) |
| `toObjectId` | The ID of the record that you want to associate the call with. |
| `associationTypeId` | A unique identifier to indicate the association type between the call and the other object. The ID can be represented numerically or in snake case (e.g., `call_to_contact`). You can retrieve the value through the [associations API](/docs/api-reference/latest/crm/associations/associate-records/guide). |

For example, your request URL might look similar to the following:

`https://api.hubspot.com/crm/objects/2026-09/calls/17591596434/associations/contact/104901/194`

### Remove an association

To remove an association between a call and a record, make a `DELETE` request to the same URL as above:

`/crm/objects/2026-09/calls/{callId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

## Pin a call on a record

You can [pin a call](https://knowledge.hubspot.com/records/pin-an-activity-on-a-record) on a record so it remains on the top of the record's timeline. The call must already be associated with the record prior to pinning, and you can only pin one activity per record. To pin a call, include the call's `id` in the `hs_pinned_engagement_id` field when creating or updating a record via the object APIs. Learn more about using the [companies,](/docs/api-reference/latest/crm/objects/companies/guide#pin-an-activity-on-a-company-record)[contacts](/docs/api-reference/latest/crm/objects/contacts/guide#pin-an-activity-on-a-contact-record), [deals](/docs/api-reference/latest/crm/objects/deals/guide#pin-an-activity-on-a-deal-record), [tickets](/docs/api-reference/latest/crm/objects/tickets/guide#pin-an-activity-on-a-ticket-record), and [custom objects](/docs/api-reference/latest/crm/objects/custom-objects/guide) APIs.

## Delete calls

You can delete calls individually or in batches, which will add the call to the recycling bin in HubSpot. You can later [restore the call from the record timeline](https://knowledge.hubspot.com/records/restore-deleted-activity-in-a-record).

To delete an individual call by its call ID, make a `DELETE` request to `/crm/objects/2026-09/calls/{callId}`.

Learn more about deleting calls by checking out the [reference documentation](/docs/api-reference/latest/crm/activities/calls/delete-call).
