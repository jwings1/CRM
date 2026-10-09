> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

---
id: f0572e36-ed9d-43e2-9ab0-bda3b50e4a26
---

# Pipeline Rules API

> Manage validation rules, approvals, and stage permissions for CRM object pipelines.

export const SupportedProducts = ({marketing, sales, service, cms, data, commerce, crm, marketingLevel, salesLevel, serviceLevel, cmsLevel, dataLevel, commerceLevel, crmLevel}) => {
  const translations = {
    description: "Requires one of the following products or higher.",
    productNames: {
      marketing: "Marketing Hub",
      sales: "Sales Hub",
      service: "Service Hub",
      cms: "Content Hub",
      data: "Data Hub",
      commerce: "Revenue Hub",
      crm: "Smart CRM"
    },
    tiers: {
      free: "Free",
      starter: "Starter",
      professional: "Professional",
      enterprise: "Enterprise"
    }
  };
  const translateTier = tier => {
    if (!tier) return '';
    const lowerTier = tier.toLowerCase();
    return translations.tiers[lowerTier] || tier;
  };
  const products = [{
    name: marketing ? translations.productNames.marketing : '',
    level: translateTier(marketingLevel),
    icon: "https://www.hubspot.com/hubfs/Knowledge_Base_2023-24-25/developer/icons/MarketingHub.svg",
    alt: "Marketing Hub"
  }, {
    name: sales ? translations.productNames.sales : '',
    level: translateTier(salesLevel),
    icon: "https://www.hubspot.com/hubfs/Knowledge_Base_2023-24-25/developer/icons/SalesHub.svg",
    alt: "Sales Hub"
  }, {
    name: service ? translations.productNames.service : '',
    level: translateTier(serviceLevel),
    icon: "https://www.hubspot.com/hubfs/Knowledge_Base_2023-24-25/developer/icons/ServiceHub.svg",
    alt: "Service Hub"
  }, {
    name: cms ? translations.productNames.cms : '',
    level: translateTier(cmsLevel),
    icon: "https://www.hubspot.com/hubfs/Knowledge_Base_2023-24-25/developer/icons/ContentHub.svg",
    alt: "Content Hub"
  }, {
    name: data ? translations.productNames.data : '',
    level: translateTier(dataLevel),
    icon: "https://www.hubspot.com/hubfs/Knowledge_Base_2023-24-25/developer/icons/DataHub.svg",
    alt: "Data Hub"
  }, {
    name: commerce ? translations.productNames.commerce : '',
    level: translateTier(commerceLevel),
    icon: "https://www.hubspot.com/hubfs/Knowledge_Base/subscription_key_icons/commerce_icon.svg",
    alt: "Revenue Hub"
  }, {
    name: crm ? translations.productNames.crm : '',
    level: translateTier(crmLevel),
    icon: "https://www.hubspot.com/hubfs/Knowledge_Base_2023-24-25/developer/icons/SmartCRM.svg",
    alt: "Smart CRM"
  }].filter(product => product.name && product.level);
  if (products.length === 0) return null;
  return <div>
      <div className="text-sm mb-2">{translations.description}</div>
      <div className={`grid ${products.length === 1 ? 'grid-cols-1' : 'grid-cols-2'} gap-1.5`}>
        {products.map((product, index) => <div key={index} style={{
    display: 'flex',
    alignItems: 'center'
  }}>
            <img src={product.icon} alt={product.alt} className="w-3.5 h-3.5 mr-1.5 mt-2.5 mb-2.5 flex-shrink-0 align-middle" />
            <span className="font-medium mr-1 text-sm">{product.name} -</span>
            <span className="text-sm">{product.level}</span>
          </div>)}
      </div>
    </div>;
};

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

<AccordionGroup>
  <Accordion title="Supported products" defaultOpen="true" icon="cubes">
    <SupportedProducts marketing={true} marketingLevel="professional" sales={true} salesLevel="professional" service={true} serviceLevel="professional" data={true} dataLevel="professional" cms={true} cmsLevel="professional" />
  </Accordion>

  <Accordion title="Required Scopes" icon="key">
    <ScopesList
      scopes={[
  'crm.pipelines.approval.read',
  'crm.pipelines.governance.read',
  'crm.pipelines.governance.write',
  'crm.pipelines.stage_permissions.read',
  'crm.pipelines.stage_permissions.write'
]}
    />
  </Accordion>
</AccordionGroup>

Use the Pipeline Rules API to set and manage rules on CRM object pipelines. For example, restrict stage movement, control in which stages records can be created, require approvals for specific deal stages, or set up per-stage permissions. You can read, update, or remove pipeline rules via the Pipeline Rules API endpoints.

Learn more about [pipeline rules in HubSpot](https://knowledge.hubspot.com/object-settings/set-up-pipeline-rules).

## Retrieve pipeline rules

Use the Pipeline Rules API to read a pipeline's validation rules, approval requirements (deal pipelines only), and stage permissions.

### Retrieve all rules for a pipeline

To retrieve all rules for a specific pipeline, make a `GET` request to `/crm/pipelines-rules/2026-09/{objectTypeId}/{pipelineId}`.

For example, to retrieve rules for the default deals pipeline, make a `GET` request to `/crm/pipelines-rules/2026-09/0-3/default`.

Your response will look similar to:

```json theme={null}
{
  "id": "0-3-default",
  "objectTypeId": "0-3",
  "pipelineId": "default",
  "governanceValidationRules": {
    "noBackwardsMovementRule": {
      "enabledForAllStages": false,
      "pipelineStageIds": ["stage_123", "stage_456"]
    },
    "noSkippingStagesRule": {
      "enabledForAllStages": true,
      "pipelineStageIds": []
    },
    "objectCreationRule": {
      "pipelineStageIds": ["stage_123"]
    }
  },
  "createdAt": "2024-01-15T10:30:00.000Z",
  "updatedAt": "2024-06-01T14:22:00.000Z"
}
```

The response includes the following fields:

| Field | Description |
| - | - |
| `id` | Composite ID in the format `{objectTypeId}-{pipelineId}`. |
| `objectTypeId` | Object type ID (e.g., `0-3` for deals). |
| `pipelineId` | Pipeline ID. |
| `governanceValidationRules` | An object containing validation rules for record movement and creation in the pipeline. Contains the following rules: `noBackwardsMovementRule`, `noSkippingStagesRule`, `objectCreationRule`. Learn more about [validation rules](#validation-rules). |
| `approvalStageRules` (**Sales Hub** *Enterprise* only) | For deal pipelines, an array of stages with approval rules. Contains the following fields for each stage: `pipelineStageId`, `approverUserIds`, `approvalMode`, `approvalComment`, and if present, `conditionalApprovalFilterBranch`. Learn more about [approval rules](#deal-approval-rules-sales-hub-enterprise-only). |
| `createdAt` | ISO 8601 timestamp of when the ruleset was created. |
| `updatedAt` | ISO 8601 timestamp of the most recent update to the rules. |

### Retrieve pipeline stage permissions

To retrieve details about which users and teams can edit records in specific pipeline stages, make a `GET` request to `/crm/pipelines-rules/2026-09/{objectTypeId}/{pipelineId}/stage-edit-permissions`. Learn more about [restricted editing access by pipeline stage](https://knowledge.hubspot.com/records/assign-access-to-records#restrict-editing-access-by-pipeline-stage).

For example, to retrieve permissions for the default deals pipeline's stages, make a `GET` request to `/crm/pipelines-rules/2026-09/0-3/default/stage-edit-permissions`.

Your response will look similar to:

```json theme={null}
{
  "id": "0-3-default",
  "objectTypeId": "0-3",
  "pipelineId": "default",
  "stages": [
    {
      "pipelineStageId": "stage_123",
      "label": "Appointment Scheduled",
      "permissionMode": "OPEN",
      "teamIds": [],
      "userIds": [],
      "superAdmin": false
    },
    {
      "pipelineStageId": "stage_456",
      "label": "Contract Sent",
      "permissionMode": "RESTRICTED",
      "teamIds": ["1001"],
      "userIds": ["12345"],
      "superAdmin": true
    },
    {
      "pipelineStageId": "stage_789",
      "label": "Closed Won",
      "permissionMode": "OPEN",
      "teamIds": [],
      "userIds": [],
      "superAdmin": false
    }
  ],
  "createdAt": "2024-01-15T10:30:00.000Z",
  "updatedAt": "2026-06-18T12:00:00.000Z"
}
```

The response includes the following fields:

| Field | Description |
| - | - |
| `id` | Composite ID in the format `{objectTypeId}-{pipelineId}`. |
| `objectTypeId` | Object type ID (e.g., `0-3` for deals). |
| `pipelineId` | Pipeline ID. |
| `stages` | An array with permissions for each stage in the pipeline, ordered by display order. Contains the following for each stage: `pipelineStageId`, `label`, `permissionMode`, and if `permissionMode` is `RESTRICTED`, `teamIds`, `userIds`, and `superAdmin`. |
| `createdAt` | ISO 8601 timestamp of when the stage's permissions were set. |
| `updatedAt` | ISO 8601 timestamp of the most recent update to the stage's permissions. |

## Set or update pipeline rules

### Replace all pipeline rules

To replace the entire ruleset for a pipeline (e.g., customize rules on a default pipeline, set custom rules on a new pipeline), make a `PUT` request to `/crm/pipelines-rules/2026-09/{objectTypeId}/{pipelineId}`.

Include the following in your request body to set rules:

| Field | Type | Description |
| - | - | - |
| `governanceValidationRules` <RequiredIndicator /> | Object | Contains validation rules that restrict record movement and creation in a pipeline:  `noBackwardsMovementRule`, `noSkippingStagesRule`, `objectCreationRule` |
| `approvalStageRules` (**Sales Hub** *Enterprise* and deals only) | Array | For deal pipelines, contains approval requirements for specific stages. Includes fields that indicate the stages with approval requirements (`pipelineStageId`), which users can approve (`approverUserIds`), how many approvers are required (`approvalMode`), and an optional comment (`approvalComment`) or conditions (`conditionalApprovalFilterBranch`). |

If you don't want to replace the full ruleset for a pipeline, learn how to [update an individual rule](#update-individual-pipeline-rules) instead.

#### Validation rules

To set validation rules for how records can move in or be created in a pipeline, in the `governanceValidationRules` object, include the following rules.

| Rule | Description | Required fields |
| - | - | - |
| `noBackwardsMovementRule` <RequiredIndicator /> | Prevent users from moving records backwards from any stage or specific stages. | <ul><li>`enabledForAllStages`: if `true`, records cannot move backwards from any stage. When `true`, `pipelineStageIds` must be empty. Set to `false` to allow records to move backwards or to select specific stages. </li><li>`pipelineStageIds`: specific stages from which records cannot move backwards. Leave empty if `enabledForAllStages` is `true` or you want to allow records to move backwards.</li></ul> |
| `noSkippingStagesRule` <RequiredIndicator /> | Prevent users from skipping any stages or specific stages in the pipeline. | <ul><li>`enabledForAllStages`: if `true`, records cannot skip any stage. When `true`, `pipelineStageIds` must be empty. Set to `false` to allow records to skip any stages or to select specific stages. </li><li>`pipelineStageIds`: stages which records cannot skip. Leave empty if `enabledForAllStages` is `true` or you want to allow records to skip any stages.</li></ul> |
| `objectCreationRule` <RequiredIndicator /> | Set stages where new records can be created. | `pipelineStageIds`: stages in which new records may be created. Leave empty to allow records to be created in any stage. |

Learn more about [pipeline validation rules](https://knowledge.hubspot.com/object-settings/set-up-pipeline-rules).

#### Deal approval rules (**Sales Hub** *Enterprise* only)

To set approval rules for specific deal pipeline stages, in the `approvalStageRules` array, include the following fields in your request body for each input.

| Field | Type | Description |
| - | - | - |
| `pipelineStageId` <RequiredIndicator /> | String | The stage that triggers an approval when a record is moved to or past the stage. |
| `approverUserIds` <RequiredIndicator /> | Array | HubSpot user IDs of the designated approvers. |
| `approvalMode` <RequiredIndicator /> | String | Require all approvers (`ALL`) or only one approver (`ANY`) to approve. |
| `approvalComment` | String | Message shown to approvers. |
| `conditionalApprovalFilterBranch` | Object | Optional filter that determines if an approval is triggered. If present, approval is only required when the record matches the criteria. |

Learn more about [pipeline approval rules](https://knowledge.hubspot.com/object-settings/pipeline-approvals).

#### Examples

Refer to the following examples that replace all rules for a pipeline.

<Tabs>
  <Tab title="Ticket pipeline validation rules">
    Replace all validation rules on the default tickets pipeline with the following rules:

    * Tickets cannot be moved backwards from `status_3`.
    * Tickets cannot skip any stages in the pipeline.
    * Tickets can only be created in `status_1`.

    Make a `PUT` request to `/crm/pipelines-rules/2026-09/0-5/0` with the following request body.

    ```json theme={null}
    {
      "governanceValidationRules": {
        "noBackwardsMovementRule": {
          "enabledForAllStages": false,
          "pipelineStageIds": ["status_3"]
        },
        "noSkippingStagesRule": {
          "enabledForAllStages": true,
          "pipelineStageIds": []
        },
        "objectCreationRule": {
          "pipelineStageIds": ["status_1"]
        }
      }
    }
    ```
  </Tab>

  <Tab title="Deal pipeline validation and approval rules">
    Replace all validation and approval rules on the default deal pipeline with the following rules:

    * Deals cannot be moved backwards from `contractsent`.
    * Deals cannot skip the `presentationscheduled` stage.
    * Deals can be created in any stage.
    * An approval is triggered when a deal moves to `contractsent` and both approving users (`12345`, `98765`) must approve it.

    Make a `PUT` request to `/crm/pipelines-rules/2026-09/0-3/default` with the following request body.

    ```json theme={null}
    {
      "governanceValidationRules": {
        "noBackwardsMovementRule": {
          "enabledForAllStages": false,
          "pipelineStageIds": ["contractsent"]
        },
        "noSkippingStagesRule": {
          "enabledForAllStages": false,
          "pipelineStageIds": ["presentationscheduled"]
        },
        "objectCreationRule": {
          "pipelineStageIds": []
        }
      },
      "approvalStageRules": [
        {
          "pipelineStageId": "contractsent",
          "approverUserIds": ["12345", "98765"],
          "approvalMode": "ALL",
          "approvalComment": "Manager approval required."
        }
      ]
    }
    ```
  </Tab>
</Tabs>

### Update individual pipeline rules

To update individual validation or approval rules for a pipeline, make a `PATCH` request to `/crm/pipelines-rules/2026-09/{objectTypeId}/{pipelineId}`. Include only the required fields for the rules to update. Omit fields for rules you want to leave unchanged.

For example, the following request body restricts backward movement for all stages, without modifying any other rules:

```json theme={null}
{
  "noBackwardsMovementRule": {
    "enabledForAllStages": true,
    "pipelineStageIds": []
  }
}
```

The response returns the full ruleset, including both updated and unchanged rules.

### Update stage permissions

To update the stage permissions for a pipeline, make a `PUT` request to `/crm/pipelines-rules/2026-09/{objectTypeId}/{pipelineId}/stage-edit-permissions`. Learn more about [restricting edit access by pipeline stage](https://knowledge.hubspot.com/records/assign-access-to-records#restrict-editing-access-by-pipeline-stage).

In your request body, include a `stages` array with the following fields for each stage:

| Field | Description |
| - | - |
| `pipelineStageId` <RequiredIndicator /> | The stage ID. |
| `permissionMode` <RequiredIndicator /> | The stage's permissions, either `OPEN` (editable by all users with permissions to edit the object's records) or `RESTRICTED` (editing limited to specific users, teams, or Super Admins). |
| `teamIds` | IDs of teams that can edit records in the stage. Only used when `permissionMode` is `RESTRICTED`. |
| `userIds` | IDs of users that can edit records in the stage. Only used when `permissionMode` is `RESTRICTED`. |
| `superAdmin` | Whether to limit editing records in the stage to Super Admins only. Set to `true` to limit editing access only to admins. If omitted, the value is `false` by default. Only used when `permissionMode` is `RESTRICTED`. |

For example, to update stage permissions on the default deals pipeline, make a `PUT` request to `/crm/pipelines-rules/2026-09/0-3/default/stage-edit-permissions` and include the following request body.

```json theme={null}
{
  "stages": [
    {
      "pipelineStageId": "stage_123",
      "permissionMode": "OPEN"
    },
    {
      "pipelineStageId": "stage_456",
      "permissionMode": "RESTRICTED",
      "teamIds": ["1001"],
      "userIds": ["12345"],
      "superAdmin": true
    }
  ]
}
```

## Remove all pipeline rules

To remove all rules for a pipeline, make a `DELETE` request to `/crm/pipelines-rules/2026-09/{objectTypeId}/{pipelineId}`. This removes all custom validation rules and for deal pipelines, approval rules. Stage permissions are not impacted.

If successfully removed, you'll receive a `204 No Content` response.

## Manage deal pipeline approvals (**Sales Hub** *Enterprise* only)

If you've required approvals for specific deal stages, you can use the Pipeline Rules API to retrieve approval statuses and create or restart approvals. Learn more about [deal pipeline approvals](https://knowledge.hubspot.com/object-settings/pipeline-approvals).

### Read approval status for a deal

To get the current approval status for a deal that is in, or has passed through, an approval-gated stage, make a `GET` request to `/crm/pipelines-rules/2026-09/0-3/{pipelineId}/approvals/{dealId}`.

Your response will look similar to:

```json theme={null}
{
  "id": "0-3-contractsent-12345",
  "objectId": "12345",
  "objectTypeId": "0-3",
  "pipelineId": "default",
  "pipelineStageId": "contractsent",
  "approvalStatus": "PENDING",
  "approvalId": "approval_abc123",
  "createdAt": "2024-06-01T09:00:00.000Z",
  "updatedAt": "2024-06-01T09:00:00.000Z"
}
```

The response includes the following fields:

| Field | Description |
| - | - |
| `id` | Composite ID in the format `{objectTypeId}-{pipelineId}-{stageId}-{objectId}`. |
| `objectId` | The deal's record ID. |
| `objectTypeId` | CRM object type ID (`0-3` for deals). |
| `pipelineId` | The pipeline the record is in. |
| `pipelineStageId` | The pipeline stage the record is currently in. |
| `approvalStatus` | The current approval state. Values include: `PENDING` (awaiting approver action), `APPROVED` (all required approvals granted), `REJECTED` (at least one approver rejected), `NO_APPROVAL_NEEDED` (object didn't match the `conditionalApprovalFilterBranch` and was advanced automatically), `NOT_APPLICABLE` (the current stage has no approval rule). |
| `approvalId` | ID of the active or most recent approval record. `null` if no approval has been created for this record. |
| `createdAt` | ISO 8601 timestamp of when the approval record was created. |
| `updatedAt` | ISO 8601 timestamp of the most recent update to the approval. |

<Note>
  Approval status can also be retrieved by the `hs_latest_approval_status` and `hs_latest_approval_status_approval_id` properties on a deal. Learn more about [retrieving deals](/docs/api-reference/latest/crm/objects/deals/guide#retrieve-deals).
</Note>

### Create or restart a deal approval

To trigger or re-trigger approvals for a deal, make a `POST` request to `/crm/pipelines-rules/2026-09/0-3/{pipelineId}/approvals/start` and include the deal record's `objectId` in the request body. For example:

```json theme={null}
{
  "objectId": 12345
}
```

You may need to do this if:

* An approval failed to start automatically because an approver's permissions changed.
* An integration needs to drive the approval lifecycle programmatically.
* You need to manually retry after a transient failure.

Note the following behavior:

* Any existing pending approvals are cancelled before the new approvals begin.
* If conditional approval (`conditionalApprovalFilterBranch`) is set up and a record doesn't meet the filter criteria, the approval status is set to `NO_APPROVAL_NEEDED` and an approval will not be started.
