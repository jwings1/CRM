> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Retrieve export status

> Returns the status of the export with taskId, including the URL of the resulting file if the export status is COMPLETE

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
    <SupportedProducts marketing={true} sales={true} service={true} cms={true} marketingLevel="FREE" salesLevel="FREE" serviceLevel="FREE" cmsLevel="FREE" />
  </Accordion>

  <Accordion title="Required Scopes" icon="key">
    <ScopesList
      scopes={[
  'crm.export'
]}
    />
  </Accordion>
</AccordionGroup>


## OpenAPI

````yaml specs/2026-09/crm-exports-v2026-09.json GET /crm/exports/2026-09/export/async/tasks/{taskId}/status
openapi: 3.0.1
info:
  title: CRM Exports
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
  /crm/exports/2026-09/export/async/tasks/{taskId}/status:
    get:
      tags:
        - Advanced
      summary: Get the status of the export including the URL to download the file
      description: >-
        Returns the status of the export with taskId, including the URL of the
        resulting file if the export status is COMPLETE
      operationId: get-/crm/exports/2026-09/export/async/tasks/{taskId}/status_getStatus
      parameters:
        - name: taskId
          in: path
          description: >-
            The unique identifier of the export task whose status you want to
            retrieve. It is an integer value.
          required: true
          style: simple
          explode: false
          schema:
            type: integer
            format: int64
      responses:
        '200':
          description: successful operation
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ActionResponseWithSingleResultURI'
        default:
          $ref: '#/components/responses/Error'
          description: ''
      security:
        - oauth2:
            - crm.export
components:
  schemas:
    ActionResponseWithSingleResultURI:
      required:
        - completedAt
        - startedAt
        - status
      type: object
      properties:
        completedAt:
          type: string
          description: The timestamp when the export was completed, in ISO 8601 format.
          format: date-time
        errors:
          type: array
          description: >-
            An array of StandardError objects detailing any errors that occurred
            during the export task.
          items:
            $ref: '#/components/schemas/StandardError'
        links:
          type: object
          additionalProperties:
            type: string
          description: A collection of related links associated with the export.
        numErrors:
          type: integer
          description: The number of errors encountered during the export process.
          format: int32
        requestedAt:
          type: string
          description: The timestamp when the export request was made, in ISO 8601 format.
          format: date-time
        result:
          type: string
          description: The URL of the resulting file if the export status is COMPLETE.
        startedAt:
          type: string
          description: The timestamp when the export process started, in ISO 8601 format.
          format: date-time
        status:
          type: string
          description: >-
            The current status of the export, which can be PENDING, PROCESSING,
            COMPLETE or CANCELED.
          enum:
            - CANCELED
            - COMPLETE
            - PENDING
            - PROCESSING
    StandardError:
      required:
        - category
        - context
        - errors
        - links
        - message
        - status
      type: object
      properties:
        category:
          type: string
          description: A string indicating the general category of the error.
        context:
          type: object
          additionalProperties:
            type: array
            items:
              type: string
          description: Context about the error condition
        errors:
          type: array
          description: >-
            An array of ErrorDetail objects providing further information about
            the error.
          items:
            $ref: '#/components/schemas/ErrorDetail'
        id:
          type: string
          description: A string that uniquely identifies this error instance.
        links:
          type: object
          additionalProperties:
            type: string
          description: >-
            An object mapping link names to associated URIs that contain
            documentation about the error or recommended remediation steps.
        message:
          type: string
          description: >-
            A human readable message describing the error along with remediation
            steps where appropriate
        status:
          type: string
          description: A string representing the status of the error.
        subCategory:
          type: object
          properties: {}
          description: >-
            A specific category that contains more specific detail about the
            error
      description: Ye olde error
    Error:
      required:
        - category
        - correlationId
        - message
      type: object
      properties:
        category:
          type: string
          description: The error category
        context:
          type: object
          additionalProperties:
            type: array
            items:
              type: string
          description: Context about the error condition
          example: >-
            {invalidPropertyName=[propertyValue], missingScopes=[scope1,
            scope2]}
        correlationId:
          type: string
          description: >-
            A unique identifier for the request. Include this value with any
            error reports or support tickets
          format: uuid
          example: aeb5f871-7f07-4993-9211-075dc63e7cbf
        errors:
          type: array
          description: further information about the error
          items:
            $ref: '#/components/schemas/ErrorDetail'
        links:
          type: object
          additionalProperties:
            type: string
          description: >-
            A map of link names to associated URIs containing documentation
            about the error or recommended remediation steps
        message:
          type: string
          description: >-
            A human readable message describing the error along with remediation
            steps where appropriate
          example: An error occurred
        subCategory:
          type: string
          description: >-
            A specific category that contains more specific detail about the
            error
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
          description: The status code associated with the error detail
        context:
          type: object
          additionalProperties:
            type: array
            items:
              type: string
          description: Context about the error condition
          example: '{missingScopes=[scope1, scope2]}'
        in:
          type: string
          description: The name of the field or parameter in which the error was found.
        message:
          type: string
          description: >-
            A human readable message describing the error along with remediation
            steps where appropriate
        subCategory:
          type: string
          description: >-
            A specific category that contains more specific detail about the
            error
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
            crm.export: ''

````