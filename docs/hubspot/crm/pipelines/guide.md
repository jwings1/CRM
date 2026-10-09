> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

---
id: 7bedcefc-49e1-4850-84cd-9759144e3d3d
---

# Pipelines API

> Create, read, update, or delete object pipelines and pipeline stages.

export const RequiredIndicator = () => {
  return <span className="required-indicator">
      required
    </span>;
};

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
  'automation',
  'crm.objects.appointments.read',
  'crm.objects.appointments.sensitive.read.v2',
  'crm.objects.appointments.sensitive.write.v2',
  'crm.objects.appointments.write',
  'crm.objects.carts.read',
  'crm.objects.carts.write',
  'crm.objects.commercepayments.write',
  'crm.objects.companies.highly_sensitive.read.v2',
  'crm.objects.companies.highly_sensitive.write.v2',
  'crm.objects.companies.read',
  'crm.objects.companies.sensitive.read.v2',
  'crm.objects.companies.sensitive.write.v2',
  'crm.objects.companies.write',
  'crm.objects.contacts.highly_sensitive.read.v2',
  'crm.objects.contacts.highly_sensitive.write.v2',
  'crm.objects.contacts.read',
  'crm.objects.contacts.sensitive.read.v2',
  'crm.objects.contacts.sensitive.write.v2',
  'crm.objects.contacts.write',
  'crm.objects.courses.read',
  'crm.objects.courses.write',
  'crm.objects.custom.highly_sensitive.read.v2',
  'crm.objects.custom.highly_sensitive.write.v2',
  'crm.objects.custom.read',
  'crm.objects.custom.sensitive.read.v2',
  'crm.objects.custom.sensitive.write.v2',
  'crm.objects.custom.write',
  'crm.objects.deals.highly_sensitive.read.v2',
  'crm.objects.deals.highly_sensitive.write.v2',
  'crm.objects.deals.read',
  'crm.objects.deals.sensitive.read.v2',
  'crm.objects.deals.sensitive.write.v2',
  'crm.objects.deals.write',
  'crm.objects.feedback_submissions.read',
  'crm.objects.goals.read',
  'crm.objects.goals.write',
  'crm.objects.invoices.read',
  'crm.objects.invoices.write',
  'crm.objects.leads.read',
  'crm.objects.leads.write',
  'crm.objects.line_items.read',
  'crm.objects.line_items.write',
  'crm.objects.listings.read',
  'crm.objects.listings.write',
  'crm.objects.marketing_events.read',
  'crm.objects.marketing_events.write',
  'crm.objects.orders.read',
  'crm.objects.orders.write',
  'crm.objects.owners.read',
  'crm.objects.products.write',
  'crm.objects.quotes.read',
  'crm.objects.quotes.write',
  'crm.objects.services.read',
  'crm.objects.services.write',
  'crm.objects.subscriptions.read',
  'crm.objects.subscriptions.write',
  'crm.objects.users.read',
  'crm.objects.users.write',
  'crm.pipelines.orders.read',
  'crm.pipelines.orders.write',
  'crm.schemas.appointments.read',
  'crm.schemas.appointments.write',
  'crm.schemas.carts.read',
  'crm.schemas.carts.write',
  'crm.schemas.commercepayments.read',
  'crm.schemas.commercepayments.write',
  'crm.schemas.companies.read',
  'crm.schemas.companies.write',
  'crm.schemas.contacts.read',
  'crm.schemas.contacts.write',
  'crm.schemas.courses.read',
  'crm.schemas.courses.write',
  'crm.schemas.custom.read',
  'crm.schemas.deals.read',
  'crm.schemas.deals.write',
  'crm.schemas.invoices.read',
  'crm.schemas.invoices.write',
  'crm.schemas.line_items.read',
  'crm.schemas.listings.read',
  'crm.schemas.listings.write',
  'crm.schemas.orders.read',
  'crm.schemas.orders.write',
  'crm.schemas.quotes.read',
  'crm.schemas.services.read',
  'crm.schemas.services.write',
  'crm.schemas.subscriptions.read',
  'crm.schemas.subscriptions.write',
  'e-commerce',
  'media_bridge.read',
  'tickets',
  'tickets.highly_sensitive.v2',
  'tickets.sensitive.v2',
  'timeline'
]}
  />
</Accordion>

In HubSpot, a pipeline is where records are tracked through stages. For example, sales pipelines can be used to predict revenue and identify roadblocks, or service pipelines can be used to manage ticket statuses and analyze blockers. Depending on your [subscription](https://legal.hubspot.com/hubspot-product-and-services-catalog), you can create multiple pipelines for an object. For example, when working with deals, an account might have one pipeline for *New Sales* and another for *Contract Renewals*.

Use the Pipelines API to create and manage [object pipelines](https://knowledge.hubspot.com/object-settings/set-up-and-customize-pipelines).

## What’s new in 2026-09

In `2026-09` and future versions of the Pipelines API, HubSpot will validate references before deleting a pipeline or pipeline stage. If a pipeline or stage is in use (e.g., the pipeline has records, or is referenced by a workflow), the delete request will be blocked and return a validation error.

To validate, in requests to the following endpoints, the `validateDealStageUsagesBeforeDelete` (deal pipelines) or `validateReferencesBeforeDelete` (all other object pipelines) field defaults to `true`.

* `DELETE` `/crm/pipelines/2026-09/{objectTypeId}/{pipelineId}`
* `DELETE` `/crm/pipelines/2026-09/{objectTypeId}/{pipelineId}/stages/{stageId}`
* `PATCH` `/crm/pipelines/2026-09/{objectTypeId}/{pipelineId}`
* `PUT` `/crm/pipelines/2026-09/{objectTypeId}/{pipelineId}`

To bypass a validation check (i.e., allow a pipeline or stage to be deleted regardless of references), set the `validateDealStageUsagesBeforeDelete` (deal pipelines) or `validateReferencesBeforeDelete` (all other object pipelines) parameter to `false` in your request.

For example, to skip validation and delete a deal pipeline, include the `validateDealStageUsagesBeforeDelete` query parameter in your request: `/crm/pipelines/2026-09/0-3/sales_pipeline?validateDealStageUsagesBeforeDelete=false`

Before migrating to `/2026-09/`, review integration logic that deletes pipelines or pipeline stages.

* If deletes are expected to succeed even when a pipeline or stage is in use, update the requests to pass `false` to the validation query parameters.
* If deletes should not succeed when pipelines or stages are in use, no changes are needed. Users will need to remove references to the pipeline or stages before retrying the delete request.

## Manage pipelines

### Create a pipeline

To create a new pipeline, make a `POST` request to `/crm/pipelines/2026-09/{objectType}`. In the request body, include the following:

| Field | Description |
| - | - |
| `displayOrder` <RequiredIndicator /> | A number that decides the order the pipeline is displayed within all pipelines of the object. If multiple pipelines are the same number in the order, they're listed alphabetically by label. |
| `label` <RequiredIndicator /> | The name of the pipeline as it is displayed in HubSpot. |
| `stages` <RequiredIndicator /> | Inputs to set the stages in the pipeline. |

For each stage input, include the following fields:

| Field | Description |
| - | - |
| `metadata` <RequiredIndicator /> | Properties related to the stage. For deals, `probability` is required with a value between `0.0` (Closed Lost) and `1.0` (Closed Won). For tickets, you include `ticketState` with a value of either `OPEN` or `CLOSED`. To skip adding properties, include a blank object (`{}`). |
| `displayOrder` <RequiredIndicator /> | A number that decides the order in which the stage will be displayed. If multiple stages are the same number in the order, they're listed alphabetically by label. |
| `label` <RequiredIndicator /> | The stage name as it is displayed in HubSpot. This must be unique for each stage. |
| `stageId` | The internal name of the stage. This must be unique for each stage. If not set, it defaults to a unique numerical ID value. |

<Warning>
  **Please note:**
  Appointment, course, listing, lead, order, and service pipelines can have up to 30 stages. Deal, ticket, and custom object pipelines can have up to 100 stages.
</Warning>

For example, to create a new deal pipeline, your request may look like the following:

```json theme={null}
{
  "displayOrder": 3,
  "label": "New deal pipeline",
  "stages": [
    {
      "label": "In Progress",
      "metadata": {
        "probability": "0.2"
      },
      "displayOrder": 0,
      "stageId": "custom_stage_internal_name"
    },
    {
      "label": "Contract signed",
      "metadata": {
        "probability": "0.8"
      },
      "displayOrder": 1
    },
    {
      "label": "Closed Won",
      "metadata": {
        "probability": "1.0"
      },
      "displayOrder": 2
    },
    {
      "label": "Closed Lost",
      "metadata": {
        "probability": "0.0"
      },
      "displayOrder": 3
    }
  ]
}
```

### Replace a pipeline

If there's an existing pipeline you want to replace instead of creating a new pipeline, make a `PUT` request to `/crm/pipelines/2026-09/{objectType}/{pipelineId}` with the `id` of the pipeline to replace. In the request body, include the [fields](#create-a-pipeline) required when creating a new pipeline. The information you include in the request body will overwrite the existing pipeline's details. If you don't want to fully overwrite the pipeline's details, make a [`PATCH` request](#update-a-pipeline) instead.

### Retrieve pipelines

* To retrieve all pipelines for an object, make a `GET` request to `/crm/pipelines/2026-09/{objectType}`. Each pipeline's `id`, `label`, and `displayOrder` values will be returned, along with information about when it was created or updated. You can use the `id` values to retrieve and update individual pipelines.
* To retrieve an individual pipeline, make a `GET` request to `/crm/pipelines/2026-09/{objectType}/{pipelineId}`.

### Update a pipeline

To partially edit a pipeline's details, such as label or display order, make a `PATCH` request to `/crm/pipelines/2026-09/{objectType}/{pipelineId}`. In the request body, include the properties to update. Other fields will not be overwritten.

If you want to edit a pipeline's stages, use the [stage endpoints](#manage-pipeline-stages).

### Delete a pipeline

To delete a pipeline, make a `DELETE` request to `/crm/pipelines/2026-09/{objectType}/{pipelineId}`.

By default, the endpoint blocks deletes if the pipeline includes records or has references in other tools. If there are existing records, your response will look similar to the following:

```json theme={null}
{
  "status": "error",
  "message": "Stage IDs: [renter_viewing, renter_security_deposit_paid, renter_new_lead, renter_closed_won, renter_closed_lost] are being referenced by object IDs: [22901690010]",
  "correlationId": "1fb9ac01-f574-4919-bf55-2c8c25ac1507",
  "context": {
    "stageIds": [
      "[renter_viewing, renter_security_deposit_paid, renter_new_lead, renter_closed_won, renter_closed_lost]"
    ],
    "objectIds": ["[22901690010]"]
  },
  "category": "VALIDATION_ERROR",
  "subCategory": "PipelineError.STAGE_ID_IN_USE"
}
```

To bypass the validation check (i.e., allow a pipeline to be deleted regardless of references), set the `validateDealStageUsagesBeforeDelete` (deal pipelines) or `validateReferencesBeforeDelete` (all other object pipelines) parameter to `false` in your request.

## Manage pipeline stages

### Create a stage

To add a new stage to a pipeline, make a `POST` request to `/crm/pipelines/2026-09/{objectType}/{pipelineId}/stages`.

In the request body, include the following:

| Field | Description |
| - | - |
| `metadata` <RequiredIndicator /> | Properties related to the stage. For deals, `probability` is required with a value between `0.0` (Closed Lost) and `1.0` (Closed Won). For tickets, you include `ticketState` with a value of either `OPEN` or `CLOSED`. To skip adding properties, include a blank object (`{}`). |
| `displayOrder` <RequiredIndicator /> | A number that decides the order in which the stage will be displayed. If multiple stages are the same number in the order, they're listed alphabetically by label. |
| `label` <RequiredIndicator /> | The stage name as it is displayed in HubSpot. This must be unique for each stage. |
| `stageId` | The internal name of the stage. This must be unique for each stage. If not set, it defaults to a unique numerical ID value. |

<Warning>
  **Please note:**
  Appointment, course, listing, lead, order, and service pipelines can have up to 30 stages. Deal, ticket, and custom object pipelines can have up to 100 stages.
</Warning>

For example, to add a stage called *Contract signed* as the fifth stage in a pipeline, your request would look like:

```json theme={null}
{
  "metadata": {
    "probability": "0.8"
  },
  "displayOrder": 4,
  "label": "Contract signed"
}
```

### Replace a stage

To replace a stage's details, make a `PUT` request to `/crm/pipelines/2026-09/{objectType}/{pipelineId}/stages/{stageId}`. Include the [required fields](#create-a-stage) in your request body. This request will overwrite the stage's existing details.

If you don't want to fully overwrite the stage's details (i.e. change one field), make a [`PATCH` request](#update-a-stage) instead.

### Retrieve stages

* To retrieve all stages in a pipeline, make a `GET` request to `/crm/pipelines/2026-09/{objectType}/{pipelineId}/stages`. Each stage's `id`, `label`, and `displayOrder` values will be returned, along with information about when it was created or updated. You can use the `id` values to retrieve and update individual stages.
* To retrieve an individual stage, make a `GET` request to `/crm/pipelines/2026-09/{objectType}/{pipelineId}/stages/{stageId}`.

### Update a stage

To partially edit a stage's details, such as label or display order, make a `PATCH` request to `/crm/pipelines/2026-09/{objectType}/{pipelineId}/stages/{stageId}`. In the request body, include the properties to update. Other fields will not be overwritten.

### Delete a stage

To delete a pipeline stage, make a `DELETE` request to `/crm/pipelines/2026-09/{objectType}/{pipelineId}/stages/{stageId}`.

By default, the endpoint blocks deletes if the stage includes records or has references in other tools. To bypass the validation check (i.e., allow a stage to be deleted regardless of references), set the `validateDealStageUsagesBeforeDelete` (deal pipelines) or `validateReferencesBeforeDelete` (all other object pipelines) parameter to `false` in your request.

## Track changes to pipelines and stages

You can use the audit endpoints to track changes made to your pipelines and pipeline stages.

* To view changes made to a pipeline, make a `GET` request to `/crm/pipelines/2026-09/{objectType}/{pipelineId}/audit`.
* To view changes made to a stage, make a `GET` request to `/crm/pipelines/2026-09/{objectType}/{pipelineId}/stages/{stageId}/audit`.

In the response, updates are listed in reverse chronological order with details about the type of action, when it occurred, and who made the change.

For example, when auditing changes to a pipeline, your response would look like the following:

```json expandable theme={null}
{
  "results": [
    {
      "portalId": 123456,
      "identifier": "123456:11348541",
      "action": "UPDATE",
      "timestamp": "2024-10-07T20:58:57.414Z",
      "message": "Pipeline update",
      "rawObject": "{\"displayOrder\":1,\"pipelineId\":\"11348541\",\"portalId\":123456,\"objectType\":\"DEAL\",\"objectTypeId\":\"0-3\",\"version\":11,\"label\":\"Partner pipeline\",\"active\":true,\"stages\":[{\"displayOrder\":0,\"portalId\":123456,\"objectTypeId\":\"0-3\",\"pipelineId\":\"11348541\",\"stageId\":\"11348542\",\"label\":\"Appointment scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.2\"},\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":9586504,\"createdAt\":1614359253457,\"updatedAt\":1728334737395,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"internalWriteOnly\":false,\"active\":true,\"isApprovalStage\":null},{\"displayOrder\":1,\"portalId\":123456,\"objectTypeId\":\"0-3\",\"pipelineId\":\"11348541\",\"stageId\":\"11348543\",\"label\":\"Qualified to buy\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.4\"},\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":9586504,\"createdAt\":1614359253457,\"updatedAt\":1728334737395,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"internalWriteOnly\":false,\"active\":true,\"isApprovalStage\":null},{\"displayOrder\":2,\"portalId\":123456,\"objectTypeId\":\"0-3\",\"pipelineId\":\"11348541\",\"stageId\":\"11348544\",\"label\":\"Presentation scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.6\"},\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":9586504,\"createdAt\":1614359253457,\"updatedAt\":1728334737395,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"internalWriteOnly\":false,\"active\":true,\"isApprovalStage\":null},{\"displayOrder\":3,\"portalId\":123456,\"objectTypeId\":\"0-3\",\"pipelineId\":\"11348541\",\"stageId\":\"11348545\",\"label\":\"Decision Maker Bought-In\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":9586504,\"createdAt\":1614359253457,\"updatedAt\":1728334737395,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"internalWriteOnly\":false,\"active\":true,\"isApprovalStage\":null},{\"displayOrder\":4,\"portalId\":123456,\"objectTypeId\":\"0-3\",\"pipelineId\":\"11348541\",\"stageId\":\"11348546\",\"label\":\"Contract sent\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.9\"},\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":9586504,\"createdAt\":1614359253457,\"updatedAt\":1728334737395,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"internalWriteOnly\":false,\"active\":true,\"isApprovalStage\":null},{\"displayOrder\":5,\"portalId\":123456,\"objectTypeId\":\"0-3\",\"pipelineId\":\"11348541\",\"stageId\":\"259717454\",\"label\":\"Contract signed\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.2\"},\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":9586504,\"createdAt\":1728334734115,\"updatedAt\":1728334737395,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"internalWriteOnly\":false,\"active\":true,\"isApprovalStage\":null},{\"displayOrder\":6,\"portalId\":123456,\"objectTypeId\":\"0-3\",\"pipelineId\":\"11348541\",\"stageId\":\"11348547\",\"label\":\"Closed won\",\"metadata\":{\"isClosed\":\"true\",\"probability\":\"1.0\"},\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":9586504,\"createdAt\":1614359253457,\"updatedAt\":1728334737395,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"internalWriteOnly\":false,\"active\":true,\"isApprovalStage\":null},{\"displayOrder\":7,\"portalId\":123456,\"objectTypeId\":\"0-3\",\"pipelineId\":\"11348541\",\"stageId\":\"11348548\",\"label\":\"Closed lost\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":9586504,\"createdAt\":1614359253457,\"updatedAt\":1728334737395,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"internalWriteOnly\":false,\"active\":true,\"isApprovalStage\":null}],\"createdBy\":9586504,\"updatedBy\":9586504,\"createdAt\":1614359253457,\"updatedAt\":1728334737395,\"limitExempt\":false,\"autoCloseDateEnabled\":true,\"clearCloseDateWhenMovingClosedToOpen\":false,\"permission\":null,\"createStageId\":null,\"inactiveDefaultPipeline\":false,\"default\":false}",
      "fromUserId": 9586504
    },
    {
      "portalId": 123456,
      "identifier": "123456:11348541",
      "action": "UPDATE",
      "timestamp": "2024-10-07T20:58:54.143Z",
      "message": "Pipeline update",
      "rawObject": "{\"displayOrder\":1,\"pipelineId\":\"11348541\",\"portalId\":123456,\"objectType\":\"DEAL\",\"objectTypeId\":\"0-3\",\"version\":10,\"label\":\"Partner pipeline\",\"active\":true,\"stages\":[{\"displayOrder\":0,\"portalId\":123456,\"objectTypeId\":\"0-3\",\"pipelineId\":\"11348541\",\"stageId\":\"11348542\",\"label\":\"Appointment scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.2\"},\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":9586504,\"createdAt\":1614359253457,\"updatedAt\":1728334734115,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"internalWriteOnly\":false,\"active\":true,\"isApprovalStage\":null},{\"displayOrder\":1,\"portalId\":123456,\"objectTypeId\":\"0-3\",\"pipelineId\":\"11348541\",\"stageId\":\"11348543\",\"label\":\"Qualified to buy\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.4\"},\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":9586504,\"createdAt\":1614359253457,\"updatedAt\":1728334734115,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"internalWriteOnly\":false,\"active\":true,\"isApprovalStage\":null},{\"displayOrder\":2,\"portalId\":123456,\"objectTypeId\":\"0-3\",\"pipelineId\":\"11348541\",\"stageId\":\"11348544\",\"label\":\"Presentation scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.6\"},\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":9586504,\"createdAt\":1614359253457,\"updatedAt\":1728334734115,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"internalWriteOnly\":false,\"active\":true,\"isApprovalStage\":null},{\"displayOrder\":3,\"portalId\":123456,\"objectTypeId\":\"0-3\",\"pipelineId\":\"11348541\",\"stageId\":\"11348545\",\"label\":\"Decision Maker Bought-In\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":9586504,\"createdAt\":1614359253457,\"updatedAt\":1728334734115,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"internalWriteOnly\":false,\"active\":true,\"isApprovalStage\":null},{\"displayOrder\":4,\"portalId\":123456,\"objectTypeId\":\"0-3\",\"pipelineId\":\"11348541\",\"stageId\":\"11348546\",\"label\":\"Contract sent\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.9\"},\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":9586504,\"createdAt\":1614359253457,\"updatedAt\":1728334734115,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"internalWriteOnly\":false,\"active\":true,\"isApprovalStage\":null},{\"displayOrder\":5,\"portalId\":123456,\"objectTypeId\":\"0-3\",\"pipelineId\":\"11348541\",\"stageId\":\"11348547\",\"label\":\"Closed won\",\"metadata\":{\"isClosed\":\"true\",\"probability\":\"1.0\"},\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":9586504,\"createdAt\":1614359253457,\"updatedAt\":1728334734115,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"internalWriteOnly\":false,\"active\":true,\"isApprovalStage\":null},{\"displayOrder\":6,\"portalId\":123456,\"objectTypeId\":\"0-3\",\"pipelineId\":\"11348541\",\"stageId\":\"11348548\",\"label\":\"Closed lost\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":9586504,\"createdAt\":1614359253457,\"updatedAt\":1728334734115,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"internalWriteOnly\":false,\"active\":true,\"isApprovalStage\":null},{\"displayOrder\":7,\"portalId\":123456,\"objectTypeId\":\"0-3\",\"pipelineId\":\"11348541\",\"stageId\":\"259717454\",\"label\":\"Contract signed\",\"metadata\":{\"probability\":\"0.2\",\"isClosed\":\"false\"},\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":9586504,\"createdAt\":1728334734115,\"updatedAt\":1728334734115,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"internalWriteOnly\":false,\"active\":true,\"isApprovalStage\":null}],\"createdBy\":9586504,\"updatedBy\":9586504,\"createdAt\":1614359253457,\"updatedAt\":1728334734115,\"limitExempt\":false,\"autoCloseDateEnabled\":true,\"clearCloseDateWhenMovingClosedToOpen\":false,\"permission\":null,\"createStageId\":null,\"inactiveDefaultPipeline\":false,\"default\":false}",
      "fromUserId": 9586504
    },
    {
      "portalId": 123456,
      "identifier": "123456:11348541",
      "action": "UPDATE",
      "timestamp": "2023-07-27T15:30:01.098Z",
      "message": "Pipeline update",
      "rawObject": "{\"displayOrder\":1,\"pipelineId\":\"11348541\",\"portalId\":123456,\"label\":\"Partner pipeline\",\"active\":true,\"stages\":[{\"displayOrder\":0,\"stageId\":\"11348542\",\"label\":\"Appointment scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.2\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":1,\"stageId\":\"11348543\",\"label\":\"Qualified to buy\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.4\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":2,\"stageId\":\"11348544\",\"label\":\"Presentation scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.6\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":3,\"stageId\":\"11348545\",\"label\":\"Decision Maker Bought-In\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":4,\"stageId\":\"11348546\",\"label\":\"Contract sent\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.9\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":5,\"stageId\":\"11348547\",\"label\":\"Closed won\",\"metadata\":{\"isClosed\":\"true\",\"probability\":\"1.0\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":6,\"stageId\":\"11348548\",\"label\":\"Closed lost\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null}],\"version\":8,\"updatedBy\":null}",
      "fromUserId": 9586504
    },
    {
      "portalId": 123456,
      "identifier": "123456:11348541",
      "action": "UPDATE",
      "timestamp": "2023-03-17T17:37:42.613Z",
      "message": "Pipeline update",
      "rawObject": "{\"displayOrder\":1,\"pipelineId\":\"11348541\",\"portalId\":123456,\"label\":\"Partner pipeline\",\"active\":true,\"stages\":[{\"displayOrder\":0,\"stageId\":\"11348542\",\"label\":\"Appointment scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.2\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":1,\"stageId\":\"11348543\",\"label\":\"Qualified to buy\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.4\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":2,\"stageId\":\"11348544\",\"label\":\"Presentation scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.6\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":3,\"stageId\":\"11348545\",\"label\":\"Decision Maker Bought-In\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":4,\"stageId\":\"11348546\",\"label\":\"Contract sent\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.9\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":5,\"stageId\":\"11348547\",\"label\":\"Closed won\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":6,\"stageId\":\"11348548\",\"label\":\"Closed lost\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null}],\"version\":7,\"updatedBy\":null}",
      "fromUserId": 9586504
    },
    {
      "portalId": 123456,
      "identifier": "123456:11348541",
      "action": "UPDATE",
      "timestamp": "2023-03-17T17:31:59.276Z",
      "message": "Pipeline update",
      "rawObject": "{\"displayOrder\":1,\"pipelineId\":\"11348541\",\"portalId\":123456,\"label\":\"Partner pipeline\",\"active\":true,\"stages\":[{\"displayOrder\":0,\"stageId\":\"11348542\",\"label\":\"Appointment scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.2\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":1,\"stageId\":\"11348543\",\"label\":\"Qualified to buy\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.4\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":2,\"stageId\":\"11348544\",\"label\":\"Presentation scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.6\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":3,\"stageId\":\"11348545\",\"label\":\"Decision Maker Bought-In\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":4,\"stageId\":\"11348546\",\"label\":\"Contract sent\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.9\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":5,\"stageId\":\"11348547\",\"label\":\"Closed won\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":6,\"stageId\":\"11348548\",\"label\":\"Closed lost\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null}],\"version\":6,\"updatedBy\":null}",
      "fromUserId": 9586504
    },
    {
      "portalId": 123456,
      "identifier": "123456:11348541",
      "action": "UPDATE",
      "timestamp": "2023-03-17T17:29:18.824Z",
      "message": "Pipeline update",
      "rawObject": "{\"displayOrder\":1,\"pipelineId\":\"11348541\",\"portalId\":123456,\"label\":\"Partner pipeline\",\"active\":true,\"stages\":[{\"displayOrder\":0,\"stageId\":\"11348542\",\"label\":\"Appointment scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.2\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":1,\"stageId\":\"11348543\",\"label\":\"Qualified to buy\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.4\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":2,\"stageId\":\"11348544\",\"label\":\"Presentation scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.6\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":3,\"stageId\":\"11348545\",\"label\":\"Decision Maker Bought-In\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":4,\"stageId\":\"11348546\",\"label\":\"Contract sent\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.9\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":5,\"stageId\":\"11348547\",\"label\":\"Closed won\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":6,\"stageId\":\"11348548\",\"label\":\"Closed lost\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null}],\"version\":5,\"updatedBy\":null}",
      "fromUserId": 9586504
    },
    {
      "portalId": 123456,
      "identifier": "123456:11348541",
      "action": "UPDATE",
      "timestamp": "2022-12-09T20:29:21.004Z",
      "message": "Pipeline update",
      "rawObject": "{\"displayOrder\":1,\"pipelineId\":\"11348541\",\"portalId\":123456,\"label\":\"Partner pipeline\",\"active\":true,\"stages\":[{\"displayOrder\":0,\"stageId\":\"11348542\",\"label\":\"Appointment scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.2\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":1,\"stageId\":\"11348543\",\"label\":\"Qualified to buy\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.4\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":2,\"stageId\":\"11348544\",\"label\":\"Presentation scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.6\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":3,\"stageId\":\"11348545\",\"label\":\"Decision Maker Bought-In\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":4,\"stageId\":\"11348546\",\"label\":\"Contract sent\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.9\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":5,\"stageId\":\"11348547\",\"label\":\"Closed won\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":6,\"stageId\":\"11348548\",\"label\":\"Closed lost\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null}],\"version\":null,\"updatedBy\":null}",
      "fromUserId": 9586504
    },
    {
      "portalId": 123456,
      "identifier": "123456:11348541",
      "action": "UPDATE",
      "timestamp": "2022-11-08T14:32:11.024Z",
      "message": "Pipeline update",
      "rawObject": "{\"displayOrder\":1,\"pipelineId\":\"11348541\",\"portalId\":123456,\"label\":\"Additional pipeline\",\"active\":true,\"stages\":[{\"displayOrder\":0,\"stageId\":\"11348542\",\"label\":\"Appointment scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.2\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":1,\"stageId\":\"11348543\",\"label\":\"Qualified to buy\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.4\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":2,\"stageId\":\"11348544\",\"label\":\"Presentation scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.6\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":3,\"stageId\":\"11348545\",\"label\":\"Decision Maker Bought-In\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":4,\"stageId\":\"11348546\",\"label\":\"Contract sent\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.9\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":5,\"stageId\":\"11348547\",\"label\":\"Closed won\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":6,\"stageId\":\"11348548\",\"label\":\"Closed lost\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null}],\"version\":null,\"updatedBy\":null}",
      "fromUserId": 9586504
    },
    {
      "portalId": 123456,
      "identifier": "123456:11348541",
      "action": "UPDATE",
      "timestamp": "2022-11-08T14:31:58.571Z",
      "message": "Pipeline update",
      "rawObject": "{\"displayOrder\":1,\"pipelineId\":\"11348541\",\"portalId\":123456,\"label\":\"Additional pipeline\",\"active\":true,\"stages\":[{\"displayOrder\":0,\"stageId\":\"11348542\",\"label\":\"Appointment scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.2\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":1,\"stageId\":\"11348543\",\"label\":\"Qualified to buy\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.4\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":2,\"stageId\":\"11348544\",\"label\":\"Presentation scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.6\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":3,\"stageId\":\"11348545\",\"label\":\"Decision Maker Bought-In\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":4,\"stageId\":\"11348546\",\"label\":\"Contract sent\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.9\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":5,\"stageId\":\"11348547\",\"label\":\"Closed won\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null},{\"displayOrder\":6,\"stageId\":\"11348548\",\"label\":\"Closed lost\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"writePermissions\":\"CRM_PERMISSIONS_ENFORCEMENT\",\"isInternalWriteOnly\":null}],\"version\":null,\"updatedBy\":null}",
      "fromUserId": 9586504
    },
    {
      "portalId": 123456,
      "identifier": "123456:11348541",
      "action": "UPDATE",
      "timestamp": "2022-05-11T17:49:38.304Z",
      "message": "Pipeline update",
      "rawObject": "{\"displayOrder\":1,\"pipelineId\":\"11348541\",\"portalId\":123456,\"label\":\"Additional pipeline\",\"active\":true,\"stages\":[{\"displayOrder\":0,\"stageId\":\"11348542\",\"label\":\"Appointment scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.2\"},\"updatedBy\":9586504,\"updatedAt\":1652291367982,\"internalWriteOnly\":null},{\"displayOrder\":1,\"stageId\":\"11348543\",\"label\":\"Qualified to buy\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.4\"},\"updatedBy\":9586504,\"updatedAt\":1652291367982,\"internalWriteOnly\":null},{\"displayOrder\":2,\"stageId\":\"11348544\",\"label\":\"Presentation scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.6\"},\"updatedBy\":9586504,\"updatedAt\":1652291367982,\"internalWriteOnly\":null},{\"displayOrder\":3,\"stageId\":\"11348545\",\"label\":\"Decision Maker Bought-In\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":9586504,\"updatedAt\":1652291367982,\"internalWriteOnly\":null},{\"displayOrder\":4,\"stageId\":\"11348546\",\"label\":\"Contract sent\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.9\"},\"updatedBy\":9586504,\"updatedAt\":1652291367982,\"internalWriteOnly\":null},{\"displayOrder\":5,\"stageId\":\"11348547\",\"label\":\"Closed won\",\"metadata\":{\"isClosed\":\"true\",\"probability\":\"0.8\"},\"updatedBy\":9586504,\"updatedAt\":1652291367982,\"internalWriteOnly\":null},{\"displayOrder\":6,\"stageId\":\"11348548\",\"label\":\"Closed lost\",\"metadata\":{\"isClosed\":\"true\",\"probability\":\"0.8\"},\"updatedBy\":9586504,\"updatedAt\":1652291367982,\"internalWriteOnly\":null}],\"version\":1,\"updatedBy\":null}",
      "fromUserId": 9586504
    },
    {
      "portalId": 123456,
      "identifier": "123456:11348541",
      "action": "UPDATE",
      "timestamp": "2022-05-11T17:49:28.001Z",
      "message": "Pipeline update",
      "rawObject": "{\"displayOrder\":1,\"pipelineId\":\"11348541\",\"portalId\":123456,\"label\":\"Additional pipeline\",\"active\":true,\"stages\":[{\"displayOrder\":0,\"stageId\":\"11348542\",\"label\":\"Appointment scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.2\"},\"updatedBy\":null,\"updatedAt\":null,\"internalWriteOnly\":null},{\"displayOrder\":1,\"stageId\":\"11348543\",\"label\":\"Qualified to buy\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.4\"},\"updatedBy\":null,\"updatedAt\":null,\"internalWriteOnly\":null},{\"displayOrder\":2,\"stageId\":\"11348544\",\"label\":\"Presentation scheduled\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.6\"},\"updatedBy\":null,\"updatedAt\":null,\"internalWriteOnly\":null},{\"displayOrder\":3,\"stageId\":\"11348545\",\"label\":\"Decision Maker Bought-In\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"internalWriteOnly\":null},{\"displayOrder\":4,\"stageId\":\"11348546\",\"label\":\"Contract sent\",\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.9\"},\"updatedBy\":null,\"updatedAt\":null,\"internalWriteOnly\":null},{\"displayOrder\":5,\"stageId\":\"11348547\",\"label\":\"Closed won\",\"metadata\":{\"isClosed\":\"true\",\"probability\":\"0.8\"},\"updatedBy\":null,\"updatedAt\":null,\"internalWriteOnly\":null},{\"displayOrder\":6,\"stageId\":\"11348548\",\"label\":\"Closed lost\",\"metadata\":{\"isClosed\":\"true\",\"probability\":\"0.0\"},\"updatedBy\":null,\"updatedAt\":null,\"internalWriteOnly\":null}],\"version\":0,\"updatedBy\":null}",
      "fromUserId": 9586504
    },
    {
      "portalId": 123456,
      "identifier": "123456:11348541",
      "action": "CREATE",
      "timestamp": "2021-02-26T17:07:35.013Z",
      "message": "User defined. pipeline created",
      "rawObject": "{\"label\":\"Additional pipeline\",\"displayOrder\":1,\"active\":true,\"stages\":[{\"label\":\"Appointment scheduled\",\"displayOrder\":0,\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.2\"},\"portalId\":123456,\"pipelineId\":\"11348541\",\"stageId\":\"11348542\",\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":null,\"createdAt\":1614359253457,\"updatedAt\":null,\"active\":true},{\"label\":\"Qualified to buy\",\"displayOrder\":1,\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.4\"},\"portalId\":123456,\"pipelineId\":\"11348541\",\"stageId\":\"11348543\",\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":null,\"createdAt\":1614359253457,\"updatedAt\":null,\"active\":true},{\"label\":\"Presentation scheduled\",\"displayOrder\":2,\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.6\"},\"portalId\":123456,\"pipelineId\":\"11348541\",\"stageId\":\"11348544\",\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":null,\"createdAt\":1614359253457,\"updatedAt\":null,\"active\":true},{\"label\":\"Decision Maker Bought-In\",\"displayOrder\":3,\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.8\"},\"portalId\":123456,\"pipelineId\":\"11348541\",\"stageId\":\"11348545\",\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":null,\"createdAt\":1614359253457,\"updatedAt\":null,\"active\":true},{\"label\":\"Contract sent\",\"displayOrder\":4,\"metadata\":{\"isClosed\":\"false\",\"probability\":\"0.9\"},\"portalId\":123456,\"pipelineId\":\"11348541\",\"stageId\":\"11348546\",\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":null,\"createdAt\":1614359253457,\"updatedAt\":null,\"active\":true},{\"label\":\"Closed won\",\"displayOrder\":5,\"metadata\":{\"isClosed\":\"true\",\"probability\":\"1.0\"},\"portalId\":123456,\"pipelineId\":\"11348541\",\"stageId\":\"11348547\",\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":null,\"createdAt\":1614359253457,\"updatedAt\":null,\"active\":true},{\"label\":\"Closed lost\",\"displayOrder\":6,\"metadata\":{\"isClosed\":\"true\",\"probability\":\"0.0\"},\"portalId\":123456,\"pipelineId\":\"11348541\",\"stageId\":\"11348548\",\"maxVisibleVersion\":null,\"createdBy\":9586504,\"updatedBy\":null,\"createdAt\":1614359253457,\"updatedAt\":null,\"active\":true}],\"objectType\":\"DEAL\",\"objectTypeId\":\"0-3\",\"pipelineId\":\"11348541\",\"portalId\":123456,\"version\":0,\"createdBy\":9586504,\"updatedBy\":null,\"createdAt\":1614359253457,\"updatedAt\":null,\"limitExempt\":false,\"permission\":null,\"default\":false}",
      "fromUserId": 9586504
    }
  ]
}
```
