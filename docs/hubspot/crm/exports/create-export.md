> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Start an export

> Begins exporting CRM data for the portal as specified in the request body

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

````yaml specs/2026-09/crm-exports-v2026-09.json POST /crm/exports/2026-09/export/async
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
  /crm/exports/2026-09/export/async:
    post:
      tags:
        - Advanced
      summary: Start an export
      description: >-
        Begins exporting CRM data for the portal as specified in the request
        body
      operationId: post-/crm/exports/2026-09/export/async_start
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PublicExportRequest'
        required: true
      responses:
        '202':
          description: accepted
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaskLocator'
        default:
          $ref: '#/components/responses/Error'
          description: ''
      security:
        - oauth2:
            - crm.export
components:
  schemas:
    PublicExportRequest:
      properties: {}
      oneOf:
        - $ref: '#/components/schemas/PublicExportViewRequest'
        - $ref: '#/components/schemas/PublicExportListRequest'
    TaskLocator:
      required:
        - id
      type: object
      properties:
        id:
          type: string
          description: The unique ID of the export.
        links:
          type: object
          additionalProperties:
            type: string
          description: An object containing relevant links related to the export process.
    PublicExportViewRequest:
      required:
        - associatedObjectType
        - exportInternalValuesOptions
        - exportName
        - exportType
        - format
        - includeLabeledAssociations
        - includePrimaryDisplayPropertyForAssociatedObjects
        - language
        - objectProperties
        - objectType
        - overrideAssociatedObjectsPerDefinitionPerRowLimit
      type: object
      properties:
        associatedObjectType:
          type: array
          description: >-
            An array of strings indicating the types of associated objects to
            include in the export.
          items:
            type: string
        exportInternalValuesOptions:
          type: array
          description: >-
            An array of strings specifying options for internal values in the
            export. Valid values are 'NAMES' and 'VALUES'.
          items:
            type: string
            enum:
              - NAMES
              - VALUES
        exportName:
          type: string
          description: The name assigned to the export, represented as a string.
        exportType:
          type: string
          description: The type of export being requested. The only valid value is 'VIEW'.
          default: VIEW
          enum:
            - VIEW
        format:
          type: string
          description: >-
            The file format for the export. Valid options are 'XLS', 'XLSX', and
            'CSV'.
          enum:
            - CSV
            - XLS
            - XLSX
        includeLabeledAssociations:
          type: boolean
          description: >-
            A boolean indicating whether labeled associations should be included
            in the export.
        includePrimaryDisplayPropertyForAssociatedObjects:
          type: boolean
          description: >-
            A boolean indicating whether the primary display property for
            associated objects should be included.
        language:
          type: string
          description: >-
            The language code for the export. Valid values include 'EN', 'FR',
            'DE', 'JA', 'ES', 'PT_BR', 'NL', 'BN', 'CS', 'DA_DK', 'EL_GR',
            'ES_MX', 'FI', 'HR', 'HU', 'ID', 'IT', 'KO_KR', 'NO', 'PL', 'RO',
            'RU', 'SV', 'TH', 'VI_VN', 'ZH_CN', 'ZH_HK', 'AF_ZA', 'AR_EG', 'BG',
            'CA_ES', 'SL', 'TR', 'UK', 'EN_GB', 'FR_CA', 'HE_IL', 'LT_LT',
            'PT_PT', 'SK_SK', 'MS', 'TL', 'ZH_TW', 'HI_IN', 'ET_EE'.
          enum:
            - AF_ZA
            - AR_EG
            - BG
            - BN
            - CA_ES
            - CS
            - DA_DK
            - DE
            - EL_GR
            - EN
            - EN_GB
            - ES
            - ES_MX
            - ET_EE
            - FI
            - FR
            - FR_CA
            - HE_IL
            - HI_IN
            - HR
            - HU
            - ID
            - IT
            - JA
            - KO_KR
            - LT_LT
            - MS
            - NL
            - 'NO'
            - PL
            - PT_BR
            - PT_PT
            - RO
            - RU
            - SK_SK
            - SL
            - SV
            - TH
            - TL
            - TR
            - UK
            - VI_VN
            - ZH_CN
            - ZH_HK
            - ZH_TW
        objectProperties:
          type: array
          description: >-
            An array of strings specifying the properties of the object to be
            included in the export.
          items:
            type: string
        objectType:
          type: string
          description: A string representing the type of object being exported.
        overrideAssociatedObjectsPerDefinitionPerRowLimit:
          type: boolean
          description: >-
            A boolean indicating whether to override the limit of associated
            objects per definition per row.
        publicCrmSearchRequest:
          $ref: '#/components/schemas/PublicCrmSearchRequest'
      x-hubspot-sub-type-impl: true
    PublicExportListRequest:
      required:
        - associatedObjectType
        - exportInternalValuesOptions
        - exportName
        - exportType
        - format
        - includeLabeledAssociations
        - includePrimaryDisplayPropertyForAssociatedObjects
        - language
        - listId
        - objectProperties
        - objectType
        - overrideAssociatedObjectsPerDefinitionPerRowLimit
      type: object
      properties:
        associatedObjectType:
          type: array
          description: >-
            An array of strings specifying the types of associated objects to
            include in the export.
          items:
            type: string
        exportInternalValuesOptions:
          type: array
          description: >-
            An array of strings indicating options for exporting internal
            values. Valid values are 'NAMES' and 'VALUES'.
          items:
            type: string
            enum:
              - NAMES
              - VALUES
        exportName:
          type: string
          description: A string representing the name of the export.
        exportType:
          type: string
          description: A string indicating the type of export, which is 'LIST' by default.
          default: LIST
          enum:
            - LIST
        format:
          type: string
          description: >-
            A string specifying the format of the export file. Valid values are
            'XLS', 'XLSX', and 'CSV'.
          enum:
            - CSV
            - XLS
            - XLSX
        includeLabeledAssociations:
          type: boolean
          description: >-
            A boolean indicating whether to include labeled associations in the
            export.
        includePrimaryDisplayPropertyForAssociatedObjects:
          type: boolean
          description: >-
            A boolean indicating whether to include the primary display property
            for associated objects.
        language:
          type: string
          description: >-
            A string specifying the language for the export. Valid values
            include language codes such as 'EN', 'FR', 'DE', etc.
          enum:
            - AF_ZA
            - AR_EG
            - BG
            - BN
            - CA_ES
            - CS
            - DA_DK
            - DE
            - EL_GR
            - EN
            - EN_GB
            - ES
            - ES_MX
            - ET_EE
            - FI
            - FR
            - FR_CA
            - HE_IL
            - HI_IN
            - HR
            - HU
            - ID
            - IT
            - JA
            - KO_KR
            - LT_LT
            - MS
            - NL
            - 'NO'
            - PL
            - PT_BR
            - PT_PT
            - RO
            - RU
            - SK_SK
            - SL
            - SV
            - TH
            - TL
            - TR
            - UK
            - VI_VN
            - ZH_CN
            - ZH_HK
            - ZH_TW
        listId:
          type: string
          description: A string representing the ID of the list to be exported.
        objectProperties:
          type: array
          description: >-
            An array of strings listing the properties of the objects to be
            included in the export.
          items:
            type: string
        objectType:
          type: string
          description: A string representing the type of objects being exported.
        overrideAssociatedObjectsPerDefinitionPerRowLimit:
          type: boolean
          description: >-
            A boolean indicating whether to override the limit on associated
            objects per definition per row.
      x-hubspot-sub-type-impl: true
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
    PublicCrmSearchRequest:
      required:
        - filterGroups
        - filters
        - sorts
      type: object
      properties:
        filterGroups:
          type: array
          description: >-
            An array of filter groups, where each group contains multiple
            filters. This allows for complex filtering logic by combining
            multiple filters together.
          items:
            $ref: '#/components/schemas/FilterGroup'
        filters:
          type: array
          description: >-
            An array of filter objects used to specify the criteria for the
            search. Each filter defines a property, an operator, and a value to
            filter by.
          items:
            $ref: '#/components/schemas/Filter'
        query:
          type: string
          description: The search query string, to filter CRM records.
        sorts:
          type: array
          description: Defines the order in which the CRM records should be returned.
          items:
            type: string
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
    FilterGroup:
      required:
        - filters
      type: object
      properties:
        filters:
          type: array
          description: >-
            An array of filter objects that define the criteria for the filter
            group. Each filter specifies a property, an operator, and a value to
            be used in the filtering process.
          items:
            $ref: '#/components/schemas/Filter'
      description: >-
        Represents a group of filters used to query data within HubSpot. This
        component is used to define criteria for filtering records in various
        API endpoints.
    Filter:
      required:
        - operator
        - propertyName
      type: object
      properties:
        highValue:
          type: string
          description: >-
            A string representing the upper boundary value used with the
            'BETWEEN' operator.
        operator:
          type: string
          description: >-
            The operator used to compare the property value against the
            specified value(s). Valid operators include 'EQ', 'NEQ', 'LT',
            'LTE', 'GT', 'GTE', 'BETWEEN', 'IN', 'NOT_IN', 'HAS_PROPERTY',
            'NOT_HAS_PROPERTY', 'CONTAINS_TOKEN', and 'NOT_CONTAINS_TOKEN'.
          enum:
            - BETWEEN
            - CONTAINS_TOKEN
            - EQ
            - GT
            - GTE
            - HAS_PROPERTY
            - IN
            - LT
            - LTE
            - NEQ
            - NOT_CONTAINS_TOKEN
            - NOT_HAS_PROPERTY
            - NOT_IN
        propertyName:
          type: string
          description: The name of the property to filter by. This is a string value.
        value:
          type: string
          description: >-
            A string representing the value to compare the property against when
            using certain operators.
        values:
          type: array
          description: >-
            An array of string values used with operators like 'IN' and 'NOT_IN'
            to specify multiple comparison values.
          items:
            type: string
      description: >-
        Defines a single condition for searching CRM objects, specifying the
        property to filter on, the operator to use (such as equals, greater
        than, or contains), and the value(s) to compare against. 
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