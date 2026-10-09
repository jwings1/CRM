> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

---
id: 0dec35c4-dc49-4c83-9191-a0e586c1f556
---

# Start Approval

> Initiate the approval process for a specific pipeline within a given object type. This endpoint is useful for triggering approval workflows that are associated with pipeline stages, ensuring that the necessary approvals are obtained before proceeding with further actions in the pipeline.

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

<AccordionGroup>
  <Accordion title="Supported products" defaultOpen="true" icon="cubes">
    <SupportedProducts marketing={true} sales={true} service={true} cms={true} data={true} marketingLevel="professional" salesLevel="professional" serviceLevel="professional" cmsLevel="professional" dataLevel="professional" />
  </Accordion>

  <Accordion title="Required Scopes" icon="key">
    <ScopesList
      scopes={[
  'crm-pipelines-governance-write'
]}
    />
  </Accordion>
</AccordionGroup>


## OpenAPI

````yaml specs/2026-09/crm-pipeline-governance-v2026-09.json POST /crm/pipelines-rules/2026-09/{objectTypeId}/{pipelineId}/approvals/start
openapi: 3.0.1
info:
  title: CRM Pipeline Governance
  description: Basepom for all HubSpot Projects
  version: 2026-09
  x-hubspot-product-tier-requirements:
    marketing: FREE
    sales: FREE
    service: FREE
    cms: FREE
    commerce: FREE
    crmHub: FREE
    dataHub: FREE
servers:
  - url: https://api.hubapi.com
security: []
tags:
  - name: Advanced
  - name: Basic
paths:
  /crm/pipelines-rules/2026-09/{objectTypeId}/{pipelineId}/approvals/start:
    post:
      tags:
        - Advanced
      summary: Start Approval
      description: >-
        Initiate the approval process for a specific pipeline within a given
        object type. This endpoint is useful for triggering approval workflows
        that are associated with pipeline stages, ensuring that the necessary
        approvals are obtained before proceeding with further actions in the
        pipeline.
      operationId: >-
        post-/crm/pipelines-rules/2026-09/{objectTypeId}/{pipelineId}/approvals/start_/crm/pipelines-rules/2026-09-beta/{objectTypeId}/{pipelineId}/approvals/start
      parameters:
        - name: objectTypeId
          in: path
          description: >-
            The unique identifier of the object type for which the approval
            process is being started.
          required: true
          style: simple
          explode: false
          schema:
            type: string
        - name: pipelineId
          in: path
          description: >-
            The unique identifier of the pipeline for which the approval process
            is being initiated.
          required: true
          style: simple
          explode: false
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PublicCreateApprovalRequest'
        required: true
      responses:
        '200':
          description: successful operation
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PublicObjectApprovalStatus'
        default:
          $ref: '#/components/responses/Error'
          description: ''
      security:
        - oauth2:
            - crm.pipelines.governance.write
components:
  schemas:
    PublicCreateApprovalRequest:
      required:
        - objectId
      type: object
      properties:
        objectId:
          type: integer
          description: >-
            The unique identifier of the object for which the approval request
            is being created. It is an integer formatted as int64.
          format: int64
    PublicObjectApprovalStatus:
      required:
        - approvalStatus
        - createdAt
        - id
        - objectId
        - objectTypeId
        - pipelineId
        - pipelineStageId
        - updatedAt
      type: object
      properties:
        approvalId:
          type: string
          description: >-
            The unique identifier for the approval process instance associated
            with this object.
        approvalStatus:
          type: string
          description: >-
            The current approval status of the object. This indicates whether
            the object is approved, pending approval, or rejected.
          enum:
            - APPROVED
            - NO_APPROVAL_NEEDED
            - NOT_APPLICABLE
            - PENDING
            - REJECTED
        createdAt:
          type: string
          description: >-
            The date and time when this approval status record was created, in
            ISO 8601 format.
          format: date-time
        id:
          type: string
          description: The unique identifier for this approval status object.
        objectId:
          type: string
          description: >-
            The unique identifier of the object whose approval status is being
            tracked.
        objectTypeId:
          type: string
          description: >-
            The type identifier of the object, indicating what kind of object is
            being approved.
        pipelineId:
          type: string
          description: >-
            The unique identifier of the pipeline in which the object is
            located.
        pipelineStageId:
          type: string
          description: >-
            The unique identifier of the pipeline stage where the object
            currently resides.
        updatedAt:
          type: string
          description: >-
            The date and time when this approval status record was last updated,
            in ISO 8601 format.
          format: date-time
    Error:
      required:
        - category
        - correlationId
        - message
      type: object
      properties:
        category:
          type: string
          description: A string representing the general category of the error.
        context:
          type: object
          additionalProperties:
            type: array
            items:
              type: string
          description: >-
            An object containing additional context about the error condition,
            with properties as arrays of strings.
          example: >-
            {invalidPropertyName=[propertyValue], missingScopes=[scope1,
            scope2]}
        correlationId:
          type: string
          description: >-
            A string that uniquely identifies the request for tracking and
            debugging purposes.
          format: uuid
          example: aeb5f871-7f07-4993-9211-075dc63e7cbf
        errors:
          type: array
          description: >-
            An array of ErrorDetail objects that provide detailed information
            about each error encountered.
          items:
            $ref: '#/components/schemas/ErrorDetail'
        links:
          type: object
          additionalProperties:
            type: string
          description: >-
            An object containing related links, where each key is a string and
            the value is a string representing a URL.
        message:
          type: string
          description: A string containing a human-readable message describing the error.
          example: An error occurred
        subCategory:
          type: string
          description: A string providing more specific details about the error category.
      description: >-
        Represents an error response returned by the API when an operation
        fails. This component is used in various endpoints to provide detailed
        information about the error encountered.
      example:
        message: Invalid input (details will vary based on the error)
        correlationId: aeb5f871-7f07-4993-9211-075dc63e7cbf
        category: VALIDATION_ERROR
        links:
          knowledge-base: https://www.hubspot.com/products/service/knowledge-base
    ErrorDetail:
      required:
        - message
      type: object
      properties:
        code:
          type: string
          description: >-
            The status code associated with the error detail. This is a string
            property.
        context:
          type: object
          additionalProperties:
            type: array
            items:
              type: string
          description: >-
            Context about the error condition, represented as an object with
            additional properties. Each property is an array of strings
            providing further details.
          example: '{missingScopes=[scope1, scope2]}'
        in:
          type: string
          description: >-
            The name of the field or parameter in which the error was found.
            This is a string property.
        message:
          type: string
          description: >-
            A human readable message describing the error along with remediation
            steps where appropriate. It is a required string property.
        subCategory:
          type: string
          description: >-
            A specific category that contains more specific detail about the
            error. This is a string property.
      description: >-
        Represents detailed information about an error that occurred in the API.
        This component is used to provide additional context and specifics about
        errors, typically as part of an error response.
  responses:
    Error:
      description: An error occurred.
      content:
        '*/*':
          schema:
            $ref: '#/components/schemas/Error'
  securitySchemes:
    oauth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://app.hubspot.com/oauth/authorize
          tokenUrl: https://api.hubapi.com/oauth/v1/token
          scopes:
            crm.pipelines.approval.read: ''
            crm.pipelines.governance.read: ''
            crm.pipelines.governance.write: ''
            crm.pipelines.stage_permissions.read: ''
            crm.pipelines.stage_permissions.write: ''

````