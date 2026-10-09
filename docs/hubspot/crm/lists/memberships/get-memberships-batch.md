> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

---
id: febea539-5731-4702-b991-eb69b70e7dc6
---

# Batch read memberships

> Retrieve batch membership information for records within specified lists. This endpoint is useful for obtaining membership details in bulk, allowing for efficient data retrieval when dealing with multiple records.

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

````yaml specs/2026-09/crm-lists-v2026-09.json POST /crm/lists/2026-09/records/memberships/batch/read
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
  /crm/lists/2026-09/records/memberships/batch/read:
    post:
      tags:
        - Batch
      summary: Batch read memberships
      description: >-
        Retrieve batch membership information for records within specified
        lists. This endpoint is useful for obtaining membership details in bulk,
        allowing for efficient data retrieval when dealing with multiple
        records.
      operationId: post-/crm/lists/2026-09/records/memberships/batch/read
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BatchInputRecordIdInput'
        required: true
      responses:
        '200':
          description: successful operation
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BatchResponseRecordIdWithMemberships'
        '207':
          description: multiple statuses
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/BatchResponseRecordIdWithMembershipsWithErrors
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
    BatchInputRecordIdInput:
      required:
        - inputs
      type: object
      properties:
        inputs:
          type: array
          description: >-
            An array of record ID inputs. Each element is a string representing
            a unique record ID to be processed in the batch operation.
          items:
            $ref: '#/components/schemas/RecordIdInput'
    BatchResponseRecordIdWithMemberships:
      required:
        - completedAt
        - results
        - startedAt
        - status
      type: object
      properties:
        completedAt:
          type: string
          description: >-
            The date and time when the batch operation was completed, in ISO
            8601 format.
          format: date-time
        links:
          type: object
          additionalProperties:
            type: string
          description: >-
            An object containing additional links related to the batch
            operation.
        requestedAt:
          type: string
          description: >-
            The date and time when the batch operation was requested, in ISO
            8601 format.
          format: date-time
        results:
          type: array
          description: >-
            An array of results from the batch operation, each containing record
            IDs and their associated memberships.
          items:
            $ref: '#/components/schemas/RecordIdWithMemberships'
        startedAt:
          type: string
          description: >-
            The date and time when the batch operation started, in ISO 8601
            format.
          format: date-time
        status:
          type: string
          description: >-
            The current status of the batch operation. Valid values include
            'PENDING', 'PROCESSING', 'CANCELED', and 'COMPLETE'.
          enum:
            - CANCELED
            - COMPLETE
            - PENDING
            - PROCESSING
    BatchResponseRecordIdWithMembershipsWithErrors:
      required:
        - completedAt
        - results
        - startedAt
        - status
      type: object
      properties:
        completedAt:
          type: string
          description: >-
            The date and time when the batch process was completed, in ISO 8601
            format.
          format: date-time
        errors:
          type: array
          description: >-
            An array of errors that occurred during the batch process. Each item
            in the array is a reference to a StandardError schema.
          items:
            $ref: '#/components/schemas/StandardError'
        links:
          type: object
          additionalProperties:
            type: string
          description: >-
            An object containing additional links related to the batch process.
            Each key-value pair represents a link name and its URL.
        numErrors:
          type: integer
          description: The total number of errors encountered during the batch process.
          format: int32
        requestedAt:
          type: string
          description: >-
            The date and time when the batch process was requested, in ISO 8601
            format.
          format: date-time
        results:
          type: array
          description: >-
            An array of results containing record IDs with their memberships.
            Each item in the array is a reference to a RecordIdWithMemberships
            schema.
          items:
            $ref: '#/components/schemas/RecordIdWithMemberships'
        startedAt:
          type: string
          description: >-
            The date and time when the batch process started, in ISO 8601
            format.
          format: date-time
        status:
          type: string
          description: >-
            The current status of the batch process. Valid values include
            'PENDING', 'PROCESSING', 'CANCELED', and 'COMPLETE'.
          enum:
            - CANCELED
            - COMPLETE
            - PENDING
            - PROCESSING
    RecordIdInput:
      required:
        - objectTypeId
        - recordId
      type: object
      properties:
        objectTypeId:
          type: string
          description: >-
            A string representing the unique identifier of the object type
            associated with the record.
        recordId:
          type: string
          description: A string representing the unique identifier of the record.
    RecordIdWithMemberships:
      required:
        - objectTypeId
        - recordId
        - recordListMemberships
      type: object
      properties:
        objectTypeId:
          type: string
          description: >-
            The identifier for the type of object the record belongs to,
            represented as a string.
        recordId:
          type: string
          description: The unique identifier for the record, represented as a string.
        recordListMemberships:
          type: array
          description: >-
            An array of memberships indicating the lists the record is part of,
            each containing details like list ID, version, and timestamps of
            when the record was added.
          items:
            $ref: '#/components/schemas/RecordListMembership'
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
          description: >-
            An object containing additional context about the error, represented
            as a map of strings to arrays of strings.
        errors:
          type: array
          description: >-
            An array of ErrorDetail objects that provide more specific details
            about individual errors.
          items:
            $ref: '#/components/schemas/ErrorDetail'
        id:
          type: string
          description: A string that uniquely identifies the error instance.
        links:
          type: object
          additionalProperties:
            type: string
          description: >-
            An object containing related links, represented as a map of strings
            to strings.
        message:
          type: string
          description: A string containing a human-readable explanation of the error.
        status:
          type: string
          description: >-
            A string representing the HTTP status code associated with the
            error.
        subCategory:
          type: object
          properties: {}
          description: An object providing additional categorization of the error.
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
    RecordListMembership:
      required:
        - firstAddedTimestamp
        - lastAddedTimestamp
        - listId
        - listVersion
      type: object
      properties:
        firstAddedTimestamp:
          type: string
          description: >-
            The date and time when the record was first added to the list, in
            ISO 8601 format.
          format: date-time
        isPublicList:
          type: boolean
          description: A boolean indicating whether the list is public.
        lastAddedTimestamp:
          type: string
          description: >-
            The date and time when the record was last added to the list, in ISO
            8601 format.
          format: date-time
        listId:
          type: string
          description: The unique identifier of the list. It is a string value.
        listVersion:
          type: integer
          description: The version number of the list, represented as an integer.
          format: int32
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