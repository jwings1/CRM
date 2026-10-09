> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Tasks API

> Use the tasks engagement API to log and manage tasks on CRM records. 

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

Use the tasks API to create and manage tasks. You can create tasks [in HubSpot](https://knowledge.hubspot.com/records/manually-log-activities-on-records) or via the tasks API.

## Create a task

To create a task, make a `POST` request to `/crm/objects/2026-09/tasks`.

In the request body, add task details in a **properties** object. You can also add an **associations** object to associate your new task with an existing record (e.g., contacts, companies).

### Properties

In the properties object, you can include the following fields:

| Field | Description |
| - | - |
| `hs_timestamp` | Required. This field marks the task's due date. You can use either a Unix timestamp in milliseconds or UTC format. |
| `hs_task_body` | The task [notes.](https://knowledge.hubspot.com/tasks/create-tasks#task-details) |
| `hubspot_owner_id` | The [owner ID](/docs/api-reference/latest/crm/owners/guide) of the user assigned to the task. |
| `hs_task_subject` | The title of the task. |
| `hs_task_status` | The status of the task, either `COMPLETED` or `NOT_STARTED`. |
| `hs_task_priority` | The priority of the task. Values include `LOW`, `MEDIUM`, or `HIGH`. |
| `hs_task_type` | The type of task. Values include `EMAIL`, `CALL`, or `TODO`. |
| `hs_task_reminders` | The timestamp for when to send a reminder for the due date of the task. You must use Unix timestamp in milliseconds. |

### Associations

To create and associate a task with existing records, include an associations object in your request. For example, to create a task and associate it with two contacts, your request body might look similar to the following:

```json theme={null}
// Example request body
{
  "properties": {
    "hs_timestamp": "2019-10-30T03:30:17.883Z",
    "hs_task_body": "Send Proposal",
    "hubspot_owner_id": "64492917",
    "hs_task_subject": "Follow-up for Brian Buyer",
    "hs_task_status": "WAITING",
    "hs_task_priority": "HIGH",
    "hs_task_type": "CALL"
  },
  "associations": [
    {
      "to": {
        "id": 101
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 204
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
          "associationTypeId": 204
        }
      ]
    }
  ]
}
```

In the associations object, you should include the following:

| Field | Description |
| - | - |
| `to` | The record you want to associate with the task, specified by its unique `id` value. |
| `types` | The type of the association between the task and the record. Include the `associationCategory`and `associationTypeId`. Default association type IDs are listed [here](/docs/api-reference/latest/crm/associations/associate-records/guide#association-type-id-values), or you can retrieve the value for custom association types (i.e. labels) via the [associations API](/docs/api-reference/latest/crm/associations/associate-records/guide#retrieve-association-types). |

Learn more about batch creating tasks by checking out the [reference documentation](/docs/api-reference/latest/crm/activities/tasks/batch/create-tasks).

## Retrieve tasks

You can retrieve tasks individually or in bulk. Learn more about batch retrieval by checking out the [reference documentation](/docs/api-reference/latest/crm/activities/tasks/batch/get-tasks).

To retrieve an individual task by its task ID, make a `GET` request to `/crm/objects/2026-09/tasks/{taskId}`. You can also include the following parameters in the request URL:

| Parameter | Description |
| - | - |
| `properties` | A comma separated list of the properties to be returned. If a requested property isn't defined, it won't be included in the response. If a requested property is defined but a task doesn't have a value, it will be returned as `null`. |
| `associations` | A comma separated list of object types to retrieve associated IDs for. Any specified associations that don't exist will not be returned in the response. Learn more about the [associations API.](/docs/api-reference/latest/crm/associations/associate-records/guide) |

To request a list of all of tasks, make a `GET` request to `/crm/objects/2026-09/tasks`. You can include the following parameters in the request URL:

| Parameter | Description |
| - | - |
| `limit` | The maximum number of results to display per page. |
| `properties` | A comma separated list of the properties to be returned. If a requested property isn't defined, it won't be included in the response. If a requested property is defined but a task doesn't have a value, it will be returned as `null`. |

## Update tasks

You can update tasks individually or in batches. To update an individual task by its task ID, make a `PATCH` request to `/crm/objects/2026-09/tasks/{taskId}`.

In the request body, include the task properties that you want to update. For example, your request body might look similar to the following:

```json theme={null}
//Example PATCH request to https://api.hubspot.com/crm/objects/2026-09/tasks/{taskId}
{
  "properties": {
    "hs_timestamp": "2019-10-30T03:30:17.883Z",
    "hs_task_body": "Send Proposal",
    "hubspot_owner_id": "64492917",
    "hs_task_subject": "Close deal",
    "hs_task_status": "COMPLETED",
    "hs_task_priority": "HIGH"
  }
}
```

HubSpot will ignore values for read-only and non-existent properties. To clear a property value, pass an empty string for the property in the request body.

Learn more about batch updating by checking out the [reference documentation](/docs/api-reference/latest/crm/activities/tasks/batch/update-tasks).

### Associate existing tasks with records

To associate an existing task with records (e.g., contacts, deals, etc.), make a `PUT` request to `/crm/objects/2026-09/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`. The request URL should contain the following fields:

| Field | Description |
| - | - |
| `taskId` | The ID of the task. |
| `toObjectType` | The type of object that you want to associate the task with (e.g., contact or company) |
| `toObjectId` | The ID of the record that you want to associate the task with. |
| `associationTypeId` | A unique identifier to indicate the association type between the task and the other object. The ID can be represented numerically or in snake case (e.g., `task_to_contact`). You can retrieve the value through the [associations API](/docs/api-reference/latest/crm/associations/associate-records/guide). |

For example, your request URL might look similar to the following:

`https://api.hubspot.com/crm/objects/2026-09/tasks/17687016786/associations/contacts/104901/204`

### Remove an association

To remove an association between a task and a record, make a `DELETE` request to the same URL as above:

`/crm/objects/2026-09/tasks/{taskId}/associations/{toObjectType}/{toObjectId}/{associationTypeId}`

## Pin a task on a record

You can [pin a task](https://knowledge.hubspot.com/records/pin-an-activity-on-a-record) on a record so it remains on the top of the record's timeline. The task must already be associated with the record prior to pinning, and you can only pin one activity per record. To pin a task, include the task's `id` in the `hs_pinned_engagement_id` field when creating or updating a record via the object APIs. Learn more about using the [companies,](/docs/api-reference/latest/crm/objects/companies/guide#pin-an-activity-on-a-company-record)[contacts](/docs/api-reference/latest/crm/objects/contacts/guide#pin-an-activity-on-a-contact-record), [deals](/docs/api-reference/latest/crm/objects/deals/guide#pin-an-activity-on-a-deal-record), [tickets](/docs/api-reference/latest/crm/objects/tickets/guide#pin-an-activity-on-a-ticket-record), and [custom objects](/docs/api-reference/latest/crm/objects/custom-objects/guide) APIs.

## Delete tasks

You can delete tasks individually or in batches, which will add the task to the recycling bin in HubSpot. You can later [restore the task from the record timeline](https://knowledge.hubspot.com/records/restore-deleted-activity-in-a-record).

To delete an individual task by its task ID, make a `DELETE` request to `/crm/objects/2026-09/tasks/{taskId}`.

Learn more about deleting tasks by checking out the [reference documentation](/docs/api-reference/latest/crm/activities/tasks/delete-task).
