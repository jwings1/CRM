> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Retrieve imports

> Retrieve a list of imports in your HubSpot account. This endpoint allows you to view the imports that have been processed, providing details about each import. It supports pagination to navigate through large sets of import data.

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
  'crm.import'
]}
    />
  </Accordion>
</AccordionGroup>


## OpenAPI

````yaml specs/2026-09/crm-imports-v2026-09.json GET /crm/imports/2026-09
openapi: 3.0.1
info:
  title: CRM Imports
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
  /crm/imports/2026-09:
    get:
      tags:
        - Basic
      summary: List Imports
      description: >-
        Retrieve a list of imports in your HubSpot account. This endpoint allows
        you to view the imports that have been processed, providing details
        about each import. It supports pagination to navigate through large sets
        of import data.
      operationId: get-/crm/imports/2026-09_/crm/imports/v3
      parameters:
        - name: after
          in: query
          description: >-
            The paging cursor token of the last successfully read resource will
            be returned as the `paging.next.after` JSON property of a paged
            response containing more results.
          required: false
          style: form
          explode: true
          schema:
            type: string
        - name: limit
          in: query
          description: The maximum number of results to display per page.
          required: false
          style: form
          explode: true
          schema:
            type: integer
            format: int32
      responses:
        '200':
          description: successful operation
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/CollectionResponsePublicImportResponseForwardPaging
        default:
          $ref: '#/components/responses/Error'
          description: ''
      security:
        - oauth2:
            - crm.import
components:
  schemas:
    CollectionResponsePublicImportResponseForwardPaging:
      required:
        - results
      type: object
      properties:
        paging:
          $ref: '#/components/schemas/ForwardPaging'
        results:
          type: array
          description: >-
            An array of PublicImportResponse objects, each representing an
            individual import response.
          items:
            $ref: '#/components/schemas/PublicImportResponse'
    ForwardPaging:
      type: object
      properties:
        next:
          $ref: '#/components/schemas/NextPage'
      description: >-
        Paging information for forward-only pagination. Contains the next page
        reference when more results are available; omitted or empty on the last
        page.
    PublicImportResponse:
      required:
        - createdAt
        - id
        - mappedObjectTypeIds
        - metadata
        - optOutImport
        - state
        - updatedAt
      type: object
      properties:
        createdAt:
          type: string
          description: The timestamp when the object was created, in ISO 8601 format.
          format: date-time
        id:
          type: string
          description: The unique identifier for this import.
        importName:
          type: string
          description: The user-provided name for this import.
        importRequestJson:
          type: object
          properties: {}
          description: The complete import request configuration as a JSON object.
        importSource:
          type: string
          description: Indicates where/how the import was initiated.
          enum:
            - API
            - CRM_UI
            - IMPORT
            - MOBILE_ANDROID
            - MOBILE_IOS
            - SALESFORCE
        importTemplate:
          $ref: '#/components/schemas/ImportTemplate'
        mappedObjectTypeIds:
          type: array
          description: An array of object type IDs that are mapped during the import.
          items:
            type: string
        metadata:
          $ref: '#/components/schemas/PublicImportMetadata'
        optOutImport:
          type: boolean
          description: >-
            Whether or not the import is a list of people disqualified from
            receiving emails.
        state:
          type: string
          description: The status of the import.
          enum:
            - CANCELED
            - DEFERRED
            - DONE
            - FAILED
            - PROCESSING
            - REVERTED
            - STARTED
        updatedAt:
          type: string
          description: >-
            The timestamp when the import record was last updated, formatted as
            an ISO 8601 instant.
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
    NextPage:
      required:
        - after
      type: object
      properties:
        after:
          type: string
          description: >-
            A string token used as a cursor to fetch the next set of results in
            a paginated response.
        link:
          type: string
          description: A URL string that provides the link to the next page of results.
      description: >-
        Specifies the paging information needed to retrieve the next set of
        results in a paginated API response
    ImportTemplate:
      required:
        - templateId
        - templateType
      type: object
      properties:
        templateId:
          type: integer
          description: >-
            The unique identifier for the specific saved template or previous
            import being referenced.
          format: int64
        templateType:
          type: string
          description: >-
            The classification of what type of template this represents, and
            what is its origin or purpose.
          enum:
            - admin_defined
            - previous_import
            - user_file
    PublicImportMetadata:
      required:
        - counters
        - fileIds
        - objectLists
      type: object
      properties:
        counters:
          type: object
          additionalProperties:
            type: integer
            format: int32
          description: >-
            Summarized outcomes of each row a developer attempted to import into
            HubSpot.
        fileIds:
          type: array
          description: The IDs of files uploaded in the File Manager API.
          items:
            type: string
        objectLists:
          type: array
          description: The lists containing the imported objects.
          items:
            $ref: '#/components/schemas/PublicObjectListRecord'
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
    PublicObjectListRecord:
      required:
        - listId
        - objectType
      type: object
      properties:
        listId:
          type: string
          description: The ID of the list containing the imported objects.
        objectType:
          type: string
          description: The type of object contained in the list.
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
            crm.import: ''

````