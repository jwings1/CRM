> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

---
id: 9e565d46-ab4e-4bf4-bc7c-9a01868e2308
---

# Search Lists

> Search for lists within your HubSpot account using various criteria. This endpoint allows you to filter and retrieve lists based on specific search parameters, making it easier to manage and organize your lists effectively.

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
  'crm.lists.read'
]}
    />
  </Accordion>
</AccordionGroup>


## OpenAPI

````yaml specs/2026-09/crm-lists-v2026-09.json POST /crm/lists/2026-09/search
openapi: 3.0.1
info:
  title: CRM Lists
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
  - name: Basic
  - name: Batch
  - name: Search
paths:
  /crm/lists/2026-09/search:
    post:
      tags:
        - Search
      summary: Search Lists
      description: >-
        Search for lists within your HubSpot account using various criteria.
        This endpoint allows you to filter and retrieve lists based on specific
        search parameters, making it easier to manage and organize your lists
        effectively.
      operationId: post-/crm/lists/2026-09/search
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ListSearchRequest'
        required: true
      responses:
        '200':
          description: successful operation
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListSearchResponse'
        default:
          $ref: '#/components/responses/Error'
          description: ''
      security:
        - oauth2:
            - crm.segments.read
        - oauth2:
            - crm.lists.read
components:
  schemas:
    ListSearchRequest:
      required:
        - additionalProperties
        - listIds
        - offset
        - processingTypes
      type: object
      properties:
        additionalProperties:
          type: array
          description: >-
            An array of strings representing additional properties to include in
            the search.
          items:
            type: string
        count:
          type: integer
          description: An integer specifying the number of results to return.
          format: int32
        listIds:
          type: array
          description: An array of strings specifying the IDs of the lists to search.
          items:
            type: string
        objectTypeId:
          type: string
          description: A string representing the object type ID to filter the lists.
        offset:
          type: integer
          description: >-
            An integer used for pagination, indicating the starting point for
            the search results.
          format: int32
        processingTypes:
          type: array
          description: >-
            An array of strings indicating the types of processing to apply to
            the search results.
          items:
            type: string
        query:
          type: string
          description: A string representing the search query to filter the lists.
        sort:
          type: string
          description: A string specifying the sorting criteria for the search results.
    ListSearchResponse:
      required:
        - hasMore
        - lists
        - offset
        - total
      type: object
      properties:
        hasMore:
          type: boolean
          description: >-
            A boolean indicating whether there are more results available beyond
            the current page.
        lists:
          type: array
          description: >-
            An array of objects representing the lists found in the search, each
            conforming to the PublicObjectListSearchResult schema.
          items:
            $ref: '#/components/schemas/PublicObjectListSearchResult'
        offset:
          type: integer
          description: >-
            An integer indicating the position in the list of results where the
            current page starts.
          format: int32
        total:
          type: integer
          description: An integer indicating the total number of lists found by the search.
          format: int32
    PublicObjectListSearchResult:
      required:
        - additionalProperties
        - listId
        - listVersion
        - name
        - objectTypeId
        - processingStatus
        - processingType
      type: object
      properties:
        additionalProperties:
          type: object
          additionalProperties:
            type: string
          description: >-
            An object containing additional properties of the list, with each
            property represented as a string.
        createdAt:
          type: string
          description: The date and time when the list was created, in ISO 8601 format.
          format: date-time
        createdById:
          type: string
          description: >-
            The unique identifier of the user who created the list, represented
            as a string.
        deletedAt:
          type: string
          description: The date and time when the list was deleted, in ISO 8601 format.
          format: date-time
        filtersUpdatedAt:
          type: string
          description: >-
            The date and time when the list's filters were last updated, in ISO
            8601 format.
          format: date-time
        listId:
          type: string
          description: The unique identifier for the list, represented as a string.
        listVersion:
          type: integer
          description: An integer indicating the version of the list.
          format: int32
        name:
          type: string
          description: The name of the list, represented as a string.
        objectTypeId:
          type: string
          description: >-
            The unique identifier for the type of object associated with the
            list, represented as a string.
        processingStatus:
          type: string
          description: A string representing the current processing status of the list.
        processingType:
          type: string
          description: A string indicating the type of processing applied to the list.
        updatedAt:
          type: string
          description: >-
            The date and time when the list was last updated, in ISO 8601
            format.
          format: date-time
        updatedById:
          type: string
          description: >-
            The unique identifier of the user who last updated the list,
            represented as a string.
    Error:
      required:
        - category
        - correlationId
        - message
      type: object
      properties:
        category:
          type: string
          description: A string indicating the category of the error.
        context:
          type: object
          additionalProperties:
            type: array
            items:
              type: string
          description: >-
            An object containing additional context about the error, represented
            as a map of key-value pairs.
          example: >-
            {invalidPropertyName=[propertyValue], missingScopes=[scope1,
            scope2]}
        correlationId:
          type: string
          description: >-
            A unique identifier for the error instance, used for tracking and
            debugging purposes.
          format: uuid
          example: aeb5f871-7f07-4993-9211-075dc63e7cbf
        errors:
          type: array
          description: >-
            An array of ErrorDetail objects, each providing additional
            information about specific errors that occurred.
          items:
            $ref: '#/components/schemas/ErrorDetail'
        links:
          type: object
          additionalProperties:
            type: string
          description: >-
            An object containing related links, represented as a map of link
            names to URLs.
        message:
          type: string
          description: A string that provides a human-readable description of the error.
          example: An error occurred
        subCategory:
          type: string
          description: >-
            An object representing a more specific classification of the error
            within its category.
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
            A string representing a specific error code that identifies the type
            of error.
        context:
          type: object
          additionalProperties:
            type: array
            items:
              type: string
          description: >-
            An object containing additional context about the error, represented
            as a map of strings to arrays of strings, which can include specific
            parameters or values related to the error.
          example: '{missingScopes=[scope1, scope2]}'
        in:
          type: string
          description: >-
            A string indicating the location where the error occurred, such as
            'query', 'header', or 'body'.
        message:
          type: string
          description: A string containing a human-readable description of the error.
        subCategory:
          type: string
          description: >-
            An object providing additional categorization of the error, which
            may contain further details.
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
            cms.membership.access_groups.write: ''
            crm.lists.read: ''
            crm.lists.write: ''
            crm.segments.read: ''
            crm.segments.write: ''

````