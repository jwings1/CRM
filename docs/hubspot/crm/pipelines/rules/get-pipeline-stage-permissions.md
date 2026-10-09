> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

---
id: 8cc47359-132e-4a1a-8fa2-85fe9c479635
---

# Retrieve permissions

> Retrieve the stage edit permissions for a specific pipeline in your HubSpot account. This endpoint allows you to view the permissions set for editing stages within a given pipeline, identified by its object type and pipeline ID. This can be useful for managing access and ensuring that only authorized users can modify pipeline stages.

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
  'crm-pipelines-locked-stages-access',
  'pipeline-level-permissions-access'
]}
    />
  </Accordion>
</AccordionGroup>


## OpenAPI

````yaml specs/2026-09/crm-pipeline-governance-v2026-09.json GET /crm/pipelines-rules/2026-09/{objectTypeId}/{pipelineId}/stage-edit-permissions
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
  /crm/pipelines-rules/2026-09/{objectTypeId}/{pipelineId}/stage-edit-permissions:
    get:
      tags:
        - Basic
      summary: Retrieve permissions
      description: >-
        Retrieve the stage edit permissions for a specific pipeline in your
        HubSpot account. This endpoint allows you to view the permissions set
        for editing stages within a given pipeline, identified by its object
        type and pipeline ID. This can be useful for managing access and
        ensuring that only authorized users can modify pipeline stages.
      operationId: >-
        get-/crm/pipelines-rules/2026-09/{objectTypeId}/{pipelineId}/stage-edit-permissions
      parameters:
        - name: objectTypeId
          in: path
          description: >-
            The unique identifier of the object type for which the pipeline
            stage edit permissions are being retrieved.
          required: true
          style: simple
          explode: false
          schema:
            type: string
        - name: pipelineId
          in: path
          description: >-
            The unique identifier of the pipeline whose stage edit permissions
            are being retrieved.
          required: true
          style: simple
          explode: false
          schema:
            type: string
      responses:
        '200':
          description: successful operation
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PublicPipelineStagePermissions'
        default:
          $ref: '#/components/responses/Error'
          description: ''
      security:
        - oauth2:
            - crm.pipelines.stage_permissions.read
components:
  schemas:
    PublicPipelineStagePermissions:
      required:
        - createdAt
        - id
        - objectTypeId
        - pipelineId
        - stages
        - updatedAt
      type: object
      properties:
        createdAt:
          type: string
          description: >-
            The date and time when these permissions were created, in ISO 8601
            format.
          format: date-time
        id:
          type: string
          description: The unique identifier for this set of pipeline stage permissions.
        objectTypeId:
          type: string
          description: >-
            The identifier for the type of object associated with these
            permissions.
        pipelineId:
          type: string
          description: >-
            The unique identifier for the pipeline to which these stage
            permissions apply.
        stages:
          type: array
          description: >-
            An array of stage permissions, each defining access rules for a
            specific stage within the pipeline.
          items:
            $ref: '#/components/schemas/PublicStagePermission'
        updatedAt:
          type: string
          description: >-
            The date and time when these permissions were last updated, in ISO
            8601 format.
          format: date-time
    PublicStagePermission:
      required:
        - label
        - permissionMode
        - pipelineStageId
        - superAdmin
        - teamIds
        - userIds
      type: object
      properties:
        label:
          type: string
          description: >-
            A descriptive label for the stage, used for display purposes. It is
            a string that helps identify the stage's purpose or function.
        permissionMode:
          type: string
          description: >-
            Defines the mode of permission for the stage. It is a string that
            can be either 'OPEN' or 'RESTRICTED', indicating whether the stage
            is accessible to all users or restricted to certain users or teams.
          enum:
            - OPEN
            - RESTRICTED
        pipelineStageId:
          type: string
          description: >-
            The unique identifier for the pipeline stage. It is a string that
            distinguishes this stage from others within the pipeline.
        superAdmin:
          type: boolean
          description: >-
            A boolean value indicating whether super administrators have access
            to this stage. If true, super admins can access the stage regardless
            of other permissions.
        teamIds:
          type: array
          description: >-
            An array of strings representing the IDs of teams that have access
            to this stage. This property is used to specify which teams are
            allowed to interact with the stage.
          items:
            type: string
        userIds:
          type: array
          description: >-
            An array of strings representing the IDs of individual users who
            have access to this stage. This property allows for specifying
            user-level access control.
          items:
            type: string
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