> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Subtasks

> Use the tasks API to create subtasks. 

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
    <SupportedProducts marketing={true} sales={true} service={true} cms={true} data={true} marketingLevel="starter" salesLevel="starter" serviceLevel="starter" cmsLevel="starter" dataLevel="starter" />
  </Accordion>

  <Accordion title="Required Scopes" icon="key">
    <ScopesList
      scopes={[
  'crm.objects.contacts.read',
  'crm.objects.contacts.write'
]}
    />
  </Accordion>
</AccordionGroup>

Use subtasks to track multiple steps required to complete a main task. You can use the tasks API to create up to 30 subtasks associated with an existing task. Subtasks use the same properties and permissions as main tasks.

Refer to the [tasks API guide](/docs/api-reference/latest/crm/activities/tasks/guide#associations) for more details about creating and managing tasks via API.

<Warning>
  **Please note:** At this time, subtasks are only supported for main tasks created on [projects](/docs/api-reference/latest/crm/objects/projects/guide). To use subtasks, a HubSpot account must be enrolled in the [Subtasks beta](https://app.hubspot.com/portal-recommend/l?slug=product-updates/\&rollout=260899) and have the [project object activated](https://knowledge.hubspot.com/records/understand-and-use-projects-object).

  To view subtasks on projects within a HubSpot account, the account must also be enrolled in the [Flexible CRM Views beta](https://app.hubspot.com/portal-recommend/l?slug=product-updates/\&rollout=225899). Learn more about [using subtasks with projects in HubSpot](https://knowledge.hubspot.com/tasks/use-subtasks-with-objects).
</Warning>

## Create a project subtask

To create a subtask, make a `POST` request to `/crm/objects/2026-09/tasks`. In the request body, specify the subtask details in the `properties` object and associate it with the parent task in the `associations` array.

| Field | Description |
| - | - |
| `properties` | The subtask's details. Subtasks use the same properties as other tasks, so you can set values for the [default task properties](/docs/api-reference/latest/crm/activities/tasks/guide#properties) when creating the subtask. You must include at least `hs_timestamp` (the subtask's due date), but `hs_task_subject` (title) or `hs_task_body` (notes) are recommended to describe the subtask. |
| `associations` | Indicates the task with which the subtask will be associated. For the `to` field, include the `id` of the main task. To indicate that you're associating a subtask to a task in the `types` object, the `associationCategory` is `HUBSPOT_DEFINED` and the `associationTypeId` is `1313`. |

For example, to create a subtask and associate it with a main task with the ID `12345`, your request would look similar to:

```json theme={null}
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
        "id": 12345
      },
      "types": [
        {
          "associationCategory": "HUBSPOT_DEFINED",
          "associationTypeId": 1313
        }
      ]
    }
  ]
}
```
