> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Meetings API

> Use the meetings engagement API to log and manage meetings on CRM records. 

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

Use the meetings engagement API to log and manage meetings on CRM records. You can log meeting activities either [in HubSpot](https://knowledge.hubspot.com/records/manually-log-activities-on-records) or through the meetings API. You can retrieve, update, or delete meeting engagements that are manually logged on a record, scheduled using the [meetings tool](https://knowledge.hubspot.com/meetings-tool/use-meetings), or [scheduled using the Google Calendar or Office 365 calendar integration](https://knowledge.hubspot.com/meetings-tool/schedule-a-meeting-on-a-record).

## Create a meeting

To create a meeting engagement, make a `POST` request to `/crm/objects/2026-09/meetings`.

In the request body, add meeting details in a **properties** object. You can also add an **associations** object to associate your new meeting with an existing record (e.g., contacts, companies).

### Properties

In the properties object, you can include the following fields:

| Field | Fieldtype | Description |
| - | - | - |
| `hs_timestamp` | Date | Required. This field marks the date and time that the meeting occurred. You can use either a Unix timestamp in milliseconds or UTC format. When the property value is missing, the value will default to `hs_meeting_start_time.` |
| `hs_meeting_title` | String | The title of the meeting. |
| `hubspot_owner_id` | Number | The [ID of the owner](/docs/api-reference/latest/crm/owners/guide) associated with the meeting. This field determines the user listed as the meeting creator on the record timeline. |
| `hs_meeting_body` | Textarea | The meeting description. |
| `hs_internal_meeting_notes` | Text | The internal notes you take for your team during a meeting that are not included in the attendee meeting description. |
| `hs_meeting_external_url` | String | The external URL for the calendar event. For example, this could be a Google calendar link or a Microsoft Outlook calendar link. |
| `hs_meeting_location` | Text | Where the meeting takes place. The value could be a physical address, a conference room, a videoconference link, or a phone number. This appears on the calendar invite on the attendee's calendar. |
| `hs_meeting_start_time` | Datetime | The date and time when the meeting starts. The value for this property should match the value for `hs_timestamp`. |
| `hs_meeting_end_time` | Datetime | The date and time when the meeting ends. |
| `hs_meeting_outcome` | Enumeration | The outcome of the meeting. The outcome values are scheduled, completed, rescheduled, no show, and canceled. |
| `hs_activity_type` | Enumeration | The type of meeting. The options are based on the [meeting types set in your HubSpot account.](https://knowledge.hubspot.com/meetings-tool/how-do-i-create-and-use-call-and-meeting-types) |
| `hs_attachment_ids` | Enumeration | The IDs of the meeting's attachments. Multiple attachment IDs are separated by a semi-colon. |
| `hs_meeting_notetaker_selection` | Enumeration | If [notetaker](https://knowledge.hubspot.com/meetings-tool/record-and-take-notes-in-meetings-with-meeting-notetaker) is turned on/off for the meeting. The values are `enabled`, `disabled`, and `deferred`. |
| `hs_has_meeting_transcript` | Boolean | Whether the meeting has a generated transcript. The values are `Yes` and `No` |
| `hs_meeting_transcript` | Number | The transcript ID used to fetch the transcript via API. |
| `hs_meeting_recording_url` | String | The URL for the meeting recording. |
| `hs_meeting_capture_source` | Enumeration | The source that captured the meeting. The values are: `ZOOM`, `MEET`, `TEAMS`, `IN_PERSON_NOTETAKER`, and `MEETING_NOTETAKER`. |
| `hs_meeting_notetaker_id` | String | The ID of the notetaker bot that will join. |
| `hs_meeting_notetaker_source` | Enumeration | How the notetaker was invited or joined. The values are: `EMAIL_INVITE`, `MANUAL_TOGGLE`, `AUTO_JOIN`, and `LIVE_INVITE`. |
| `hs_notetaker_attendance_duration` | Number | The time in milliseconds the notetaker bot was present. |
| `hs_meeting_summary` | Textarea | The AI-generated summary of the transcript. |
| `hs_meeting_transcript_tracked_terms` | Enumeration | The [tracked terms](https://knowledge.hubspot.com/reports/report-on-tracked-terms-in-call-transcripts) found in the transcript. |
| `hs_meeting_owner_talk_time` | Number | The meeting owner's talk time. |
| `hs_meeting_owner_talk_speed` | Number | The meeting owner's words per minute talk speed. |
| `hs_meeting_owner_talk_time_percentage` | Number | The meeting owner's percentage of talk time. |
| `hs_meeting_owner_longest_monologue` | Number | The meeting owner's longest uninterrupted talk time. |
| `hs_meeting_longest_customer_story` | Number | The contact's longest uninterrupted talk time. |
| `hs_meeting_patience` | Number | The meeting owner's patience metric. |
| `hs_meeting_interactivity` | Number | The number of times per hour the conversation switched from the meeting owner to the contact. |

### Associations

To create and associate a meeting with existing records, include an associations object in your request. For example, to create and associate a meeting with contacts, your request may look similar to the following:

```json theme={null}
{
  "properties": {
    "hs_timestamp": "2021-03-23T01:02:44.872Z",
    "hubspot_owner_id": "11349275740",
    "hs_meeting_title": "Intro meeting",
    "hs_meeting_body": "The first meeting to discuss options",
    "hs_internal_meeting_notes": "These are the meeting notes",
    "hs_meeting_external_url": "https://Zoom.com/0000",
    "hs_meeting_location": "Remote",
    "hs_meeting_start_time": "2021-03-23T01:02:44.872Z",
    "hs_meeting_end_time": "2021-03-23T01:52:44.872Z",
    "hs_meeting_outcome": "SCHEDULED"
  },
  "associations": [
    {
      "to": {
        "id": 101
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 200
        }
      ]
    },
    {
      "to": {
        "id": 102
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 200
        }
      ]
    }
  ]
}
```

The associations object should include:

| Field | Description |
| - | - |
| `to` | The record you want to associate with the meeting, specified by its unique `id` value. |
| `types` | The type of the association between the meeting and the record. Include the `associationCategory`and `associationTypeId`. Default association type IDs are listed [here](/docs/api-reference/latest/crm/associations/associate-records/guide#association-type-id-values), or you can retrieve the value for custom association types (i.e. labels) via the [associations API](/docs/api-reference/latest/crm/associations/associate-records/guide#retrieve-association-types). |

Learn more about batch creating meetings by checking out the [reference documentation](/docs/api-reference/latest/crm/activities/meetings/batch/create-meetings).

## Retrieve meetings

You can retrieve meetings individually or in bulk. Learn more about batch retrieval by checking out the [reference documentation](/docs/api-reference/latest/crm/activities/meetings/batch/get-meetings).

To retrieve an individual meeting by its meeting ID, make a `GET` request to `/crm/objects/2026-09/meetings/{meetingId}`. You can also include the following parameters in the request URL:

| Parameter | Description |
| - | - |
| `properties` | A comma separated list of the properties to be returned. If a requested property isn't defined, it won't be included in the response. If a requested property is defined but a meeting doesn't have a value, it will be returned as `null`. |
| `associations` | A comma separated list of objects to you want to retrieve associated record IDs from. |

To request a list of all of meetings, make a `GET` request to `/crm/objects/2026-09/meetings`. You can include the following parameters in the request URL:

| Parameter | Description |
| - | - |
| `limit` | The maximum number of results to display per page. |
| `properties` | A comma separated list of the properties to be returned. If a requested property isn't defined, it won't be included in the response. If a requested property is defined but a meeting doesn't have a value, it will be returned as `null`. |

## Update meetings

You can update meetings individually or in batches. To update an individual meeting by its meeting ID, make a `PATCH` request to `/crm/objects/2026-09/meetings/{meetingId}`.

In the request body, include the meeting properties that you want to update. For example, your request body might look similar to the following:

```json theme={null}
{
  "properties": {
     "hs_timestamp": "2019-10-30T03:30:17.883Z",
     "hubspot_owner_id": "11349275740",
     "hs_meeting_title": "Intro meeting",
     "hs_meeting_body": "The first meeting to discuss options",
     "hs_internal_meeting_notes": "These are the meeting notes",
     "hs_meeting_external_url":
     "https://Zoom.com/0000",
     "hs_meeting_location": "Remote",
     "hs_meeting_start_time": "2021-03-23T01:02:44.872Z",
     "hs_meeting_end_time": "2021-03-23T01:52:44.872Z",
     "hs_meeting_outcome": "SCHEDULED"
  }
}'
```

HubSpot will ignore values for read-only and non-existent properties. To clear a property value, pass an empty string for the property in the request body.

Learn more about batch updating by checking out the [reference documentation](/docs/api-reference/latest/crm/activities/meetings/batch/update-meetings).

### Enable the meeting notetaker

The [meeting notetaker](https://knowledge.hubspot.com/meetings-tool/record-and-take-notes-in-meetings-with-meeting-notetaker) is a bot that can join and record your meetings. You can toggle the notetaker on or off programmatically by updating the `hs_meeting_notetaker_selection` property on a meeting.

To toggle the notetaker for a meeting, make a `PATCH` request to `/crm/objects/2026-09/meetings/{meetingId}` and set a value for the `hs_meeting_notetaker_selection` field in the request body.

The property accepts the following values:

| Value | Description |
| - | - |
| `enabled` | Invites the notetaker bot to join the meeting. |
| `disabled` | Removes the notetaker bot if one is already invited. |
| `deferred` | Defers the notetaker's invitation to the [default account setting](https://knowledge.hubspot.com/meetings-tool/record-and-take-notes-in-meetings-with-meeting-notetaker#configure-default-settings). |

For example, to enable the notetaker on a meeting, your request body would look similar to the following:

```json theme={null}
{
  "properties": {
    "hs_meeting_notetaker_selection": "enabled"
  }
}
```

### Associate existing meetings with records

To associate a meeting with records, such as a contact and its associated companies, make a `PUT` request to `/crm/objects/2026-09/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`. The request URL contains the following fields:

| Field | Description |
| - | - |
| `meetingId` | The ID of the meeting. |
| `toObjectType` | The type of object that you want to associate the meeting with (e.g., contact or company). |
| `toObjectId` | The ID of the record that you want to associate the meeting with. |
| `associationTypeId` | The ID of the association type between the meeting and the other object type. You can retrieve this value through the [associations API](/docs/api-reference/latest/crm/associations/associate-records/guide). |

For example, your request URL might look similar to the following:

`https://api.hubspot.com/crm/objects/2026-09/meetings/17612479134/associations/contact/104901/200`

### Remove an association

To remove an association between a meeting and a record, make a `DELETE` request to the same URL as above:

`/crm/objects/2026-09/meetings/{meetingId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

## Pin a meeting on a record

You can [pin a meeting](https://knowledge.hubspot.com/records/pin-an-activity-on-a-record) on a record so it remains on the top of the record's timeline. The meeting must already be associated with the record prior to pinning, and you can only pin one activity per record. To pin a meeting, include the meeting's `id` in the `hs_pinned_engagement_id` field when creating or updating a record via the object APIs. Learn more about using the [companies](/docs/api-reference/latest/crm/objects/companies/guide#pin-an-activity-on-a-company-record), [contacts](/docs/api-reference/latest/crm/objects/contacts/guide#pin-an-activity-on-a-contact-record), [deals](/docs/api-reference/latest/crm/objects/deals/guide#pin-an-activity-on-a-deal-record), [tickets](/docs/api-reference/latest/crm/objects/tickets/guide#pin-an-activity-on-a-ticket-record), and [custom objects](/docs/api-reference/latest/crm/objects/custom-objects/guide) APIs.

## Delete meetings

You can delete meetings individually or in batches, which will add the meeting to the recycling bin in HubSpot. You can later [restore the meeting from the record timeline.](https://knowledge.hubspot.com/records/restore-deleted-activity-in-a-record)

To delete an individual meeting by its meeting ID, make a `DELETE` request to `/crm/objects/2026-09/meetings/{meetingId}`.

Learn more about batch deleting by checking out the [reference documentation](/docs/api-reference/latest/crm/activities/meetings/delete-meeting).
