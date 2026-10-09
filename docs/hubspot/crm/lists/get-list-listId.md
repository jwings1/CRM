> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

---
id: c70dc7b1-d57b-4c8b-9624-278d94b43791
---

# Retrieve list

> Retrieve details of a specific list in your HubSpot account using the list's unique identifier. This endpoint allows you to optionally include filters associated with the list in the response.

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

````yaml specs/2026-09/crm-lists-v2026-09.json GET /crm/lists/2026-09/{listId}
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
  /crm/lists/2026-09/{listId}:
    get:
      tags:
        - Basic
      summary: Retrieve list
      description: >-
        Retrieve details of a specific list in your HubSpot account using the
        list's unique identifier. This endpoint allows you to optionally include
        filters associated with the list in the response.
      operationId: get-/crm/lists/2026-09/{listId}
      parameters:
        - name: listId
          in: path
          description: The unique identifier of the list to retrieve.
          required: true
          style: simple
          explode: false
          schema:
            type: string
        - name: includeFilters
          in: query
          description: >-
            A boolean indicating whether to include the list's filters in the
            response. Defaults to false.
          required: false
          style: form
          explode: true
          schema:
            type: boolean
            default: false
      responses:
        '200':
          description: successful operation
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListFetchResponse'
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
    ListFetchResponse:
      required:
        - list
      type: object
      properties:
        list:
          $ref: '#/components/schemas/PublicObjectList'
    PublicObjectList:
      required:
        - listId
        - listVersion
        - name
        - objectTypeId
        - processingStatus
        - processingType
      type: object
      properties:
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
        filterBranch:
          description: >-
            An object representing the filter branch applied to the list, which
            can be one of several types of filter branches.
          oneOf:
            - $ref: '#/components/schemas/PublicOrFilterBranch'
            - $ref: '#/components/schemas/PublicAndFilterBranch'
            - $ref: '#/components/schemas/PublicNotAllFilterBranch'
            - $ref: '#/components/schemas/PublicNotAnyFilterBranch'
            - $ref: '#/components/schemas/PublicRestrictedFilterBranch'
            - $ref: '#/components/schemas/PublicUnifiedEventsFilterBranch'
            - $ref: '#/components/schemas/PublicAssociationFilterBranch'
        filtersUpdatedAt:
          type: string
          description: >-
            The date and time when the list's filters were last updated, in ISO
            8601 format.
          format: date-time
        listId:
          type: string
          description: The unique identifier for the list, represented as a string.
        listPermissions:
          $ref: '#/components/schemas/PublicListPermissions'
        listVersion:
          type: integer
          description: An integer indicating the version of the list.
          format: int32
        membershipSettings:
          $ref: '#/components/schemas/PublicMembershipSettings'
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
        size:
          type: integer
          description: An integer representing the size of the list.
          format: int64
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
    PublicOrFilterBranch:
      title: OR
      required:
        - filterBranchOperator
        - filterBranchType
        - filterBranches
        - filters
      type: object
      properties:
        filterBranchOperator:
          type: string
          description: >-
            A string representing the operator used to combine the filters
            within the branch.
        filterBranchType:
          type: string
          description: >-
            A string indicating the type of filter branch, which is 'OR' for
            this component.
          default: OR
          enum:
            - OR
        filterBranches:
          type: array
          description: >-
            An array of nested filter branches, allowing for the combination of
            multiple logical conditions within the 'OR' branch.
          items:
            oneOf:
              - $ref: '#/components/schemas/PublicOrFilterBranch'
              - $ref: '#/components/schemas/PublicAndFilterBranch'
              - $ref: '#/components/schemas/PublicNotAllFilterBranch'
              - $ref: '#/components/schemas/PublicNotAnyFilterBranch'
              - $ref: '#/components/schemas/PublicRestrictedFilterBranch'
              - $ref: '#/components/schemas/PublicUnifiedEventsFilterBranch'
              - $ref: '#/components/schemas/PublicAssociationFilterBranch'
        filters:
          type: array
          description: >-
            An array of individual filters that are part of the 'OR' branch.
            Each filter represents a specific condition that can be evaluated.
          items:
            oneOf:
              - $ref: '#/components/schemas/PublicPropertyFilter'
              - $ref: '#/components/schemas/PublicAssociationInListFilter'
              - $ref: '#/components/schemas/PublicPageViewAnalyticsFilter'
              - $ref: '#/components/schemas/PublicCtaAnalyticsFilter'
              - $ref: '#/components/schemas/PublicEventAnalyticsFilter'
              - $ref: '#/components/schemas/PublicFormSubmissionFilter'
              - $ref: '#/components/schemas/PublicFormSubmissionOnPageFilter'
              - $ref: '#/components/schemas/PublicIntegrationEventFilter'
              - $ref: '#/components/schemas/PublicEmailSubscriptionFilter'
              - $ref: '#/components/schemas/PublicCommunicationSubscriptionFilter'
              - $ref: '#/components/schemas/PublicSurveyMonkeyFilter'
              - $ref: '#/components/schemas/PublicSurveyMonkeyValueFilter'
              - $ref: '#/components/schemas/PublicWebinarFilter'
              - $ref: '#/components/schemas/PublicEmailEventFilter'
              - $ref: '#/components/schemas/PublicPrivacyAnalyticsFilter'
              - $ref: '#/components/schemas/PublicAdsSearchFilter'
              - $ref: '#/components/schemas/PublicAdsTimeFilter'
              - $ref: '#/components/schemas/PublicInListFilter'
              - $ref: '#/components/schemas/PublicUnifiedEventsFilter'
              - $ref: '#/components/schemas/PublicConstantFilter'
      x-hubspot-sub-type-impl: true
    PublicAndFilterBranch:
      title: AND
      required:
        - filterBranchOperator
        - filterBranchType
        - filterBranches
        - filters
      type: object
      properties:
        filterBranchOperator:
          type: string
          description: A string representing the operator used within this filter branch.
        filterBranchType:
          type: string
          description: A string indicating the type of filter branch. Defaults to 'AND'.
          default: AND
          enum:
            - AND
        filterBranches:
          type: array
          description: >-
            An array of nested filter branches. Each item can be a branch of
            various types, such as 'OR', 'AND', 'NOT_ALL', etc.
          items:
            oneOf:
              - $ref: '#/components/schemas/PublicOrFilterBranch'
              - $ref: '#/components/schemas/PublicAndFilterBranch'
              - $ref: '#/components/schemas/PublicNotAllFilterBranch'
              - $ref: '#/components/schemas/PublicNotAnyFilterBranch'
              - $ref: '#/components/schemas/PublicRestrictedFilterBranch'
              - $ref: '#/components/schemas/PublicUnifiedEventsFilterBranch'
              - $ref: '#/components/schemas/PublicAssociationFilterBranch'
        filters:
          type: array
          description: >-
            An array of filters that apply to this branch. Each filter can be of
            various types, such as property filters, event filters, or
            subscription filters.
          items:
            oneOf:
              - $ref: '#/components/schemas/PublicPropertyFilter'
              - $ref: '#/components/schemas/PublicAssociationInListFilter'
              - $ref: '#/components/schemas/PublicPageViewAnalyticsFilter'
              - $ref: '#/components/schemas/PublicCtaAnalyticsFilter'
              - $ref: '#/components/schemas/PublicEventAnalyticsFilter'
              - $ref: '#/components/schemas/PublicFormSubmissionFilter'
              - $ref: '#/components/schemas/PublicFormSubmissionOnPageFilter'
              - $ref: '#/components/schemas/PublicIntegrationEventFilter'
              - $ref: '#/components/schemas/PublicEmailSubscriptionFilter'
              - $ref: '#/components/schemas/PublicCommunicationSubscriptionFilter'
              - $ref: '#/components/schemas/PublicSurveyMonkeyFilter'
              - $ref: '#/components/schemas/PublicSurveyMonkeyValueFilter'
              - $ref: '#/components/schemas/PublicWebinarFilter'
              - $ref: '#/components/schemas/PublicEmailEventFilter'
              - $ref: '#/components/schemas/PublicPrivacyAnalyticsFilter'
              - $ref: '#/components/schemas/PublicAdsSearchFilter'
              - $ref: '#/components/schemas/PublicAdsTimeFilter'
              - $ref: '#/components/schemas/PublicInListFilter'
              - $ref: '#/components/schemas/PublicUnifiedEventsFilter'
              - $ref: '#/components/schemas/PublicConstantFilter'
      x-hubspot-sub-type-impl: true
    PublicNotAllFilterBranch:
      title: NOT_ALL
      required:
        - filterBranchOperator
        - filterBranchType
        - filterBranches
        - filters
      type: object
      properties:
        filterBranchOperator:
          type: string
          description: A string representing the operator used within the filter branch.
        filterBranchType:
          type: string
          description: >-
            A string that specifies the type of filter branch. The default value
            is 'NOT_ALL'.
          default: NOT_ALL
          enum:
            - NOT_ALL
        filterBranches:
          type: array
          description: >-
            An array of filter branches that can include various types such as
            PublicOrFilterBranch, PublicAndFilterBranch, and others, allowing
            for nested filtering logic.
          items:
            oneOf:
              - $ref: '#/components/schemas/PublicOrFilterBranch'
              - $ref: '#/components/schemas/PublicAndFilterBranch'
              - $ref: '#/components/schemas/PublicNotAllFilterBranch'
              - $ref: '#/components/schemas/PublicNotAnyFilterBranch'
              - $ref: '#/components/schemas/PublicRestrictedFilterBranch'
              - $ref: '#/components/schemas/PublicUnifiedEventsFilterBranch'
              - $ref: '#/components/schemas/PublicAssociationFilterBranch'
        filters:
          type: array
          description: >-
            An array of filters that can include various types such as
            PublicPropertyFilter, PublicAssociationInListFilter, and others,
            used to apply specific conditions to the data.
          items:
            oneOf:
              - $ref: '#/components/schemas/PublicPropertyFilter'
              - $ref: '#/components/schemas/PublicAssociationInListFilter'
              - $ref: '#/components/schemas/PublicPageViewAnalyticsFilter'
              - $ref: '#/components/schemas/PublicCtaAnalyticsFilter'
              - $ref: '#/components/schemas/PublicEventAnalyticsFilter'
              - $ref: '#/components/schemas/PublicFormSubmissionFilter'
              - $ref: '#/components/schemas/PublicFormSubmissionOnPageFilter'
              - $ref: '#/components/schemas/PublicIntegrationEventFilter'
              - $ref: '#/components/schemas/PublicEmailSubscriptionFilter'
              - $ref: '#/components/schemas/PublicCommunicationSubscriptionFilter'
              - $ref: '#/components/schemas/PublicSurveyMonkeyFilter'
              - $ref: '#/components/schemas/PublicSurveyMonkeyValueFilter'
              - $ref: '#/components/schemas/PublicWebinarFilter'
              - $ref: '#/components/schemas/PublicEmailEventFilter'
              - $ref: '#/components/schemas/PublicPrivacyAnalyticsFilter'
              - $ref: '#/components/schemas/PublicAdsSearchFilter'
              - $ref: '#/components/schemas/PublicAdsTimeFilter'
              - $ref: '#/components/schemas/PublicInListFilter'
              - $ref: '#/components/schemas/PublicUnifiedEventsFilter'
              - $ref: '#/components/schemas/PublicConstantFilter'
      x-hubspot-sub-type-impl: true
    PublicNotAnyFilterBranch:
      title: NOT_ANY
      required:
        - filterBranchOperator
        - filterBranchType
        - filterBranches
        - filters
      type: object
      properties:
        filterBranchOperator:
          type: string
          description: A string representing the operator used in the filter branch.
        filterBranchType:
          type: string
          description: >-
            A string that specifies the type of filter branch. Default value is
            'NOT_ANY'.
          default: NOT_ANY
          enum:
            - NOT_ANY
        filterBranches:
          type: array
          description: >-
            An array of filter branches that can include various types such as
            'PublicOrFilterBranch', 'PublicAndFilterBranch',
            'PublicNotAllFilterBranch', 'PublicNotAnyFilterBranch',
            'PublicRestrictedFilterBranch', 'PublicUnifiedEventsFilterBranch',
            and 'PublicAssociationFilterBranch'.
          items:
            oneOf:
              - $ref: '#/components/schemas/PublicOrFilterBranch'
              - $ref: '#/components/schemas/PublicAndFilterBranch'
              - $ref: '#/components/schemas/PublicNotAllFilterBranch'
              - $ref: '#/components/schemas/PublicNotAnyFilterBranch'
              - $ref: '#/components/schemas/PublicRestrictedFilterBranch'
              - $ref: '#/components/schemas/PublicUnifiedEventsFilterBranch'
              - $ref: '#/components/schemas/PublicAssociationFilterBranch'
        filters:
          type: array
          description: >-
            An array of filters that can include types like
            'PublicPropertyFilter', 'PublicAssociationInListFilter',
            'PublicPageViewAnalyticsFilter', 'PublicCtaAnalyticsFilter',
            'PublicEventAnalyticsFilter', 'PublicFormSubmissionFilter',
            'PublicFormSubmissionOnPageFilter', 'PublicIntegrationEventFilter',
            'PublicEmailSubscriptionFilter',
            'PublicCommunicationSubscriptionFilter', 'PublicSurveyMonkeyFilter',
            'PublicSurveyMonkeyValueFilter', 'PublicWebinarFilter',
            'PublicEmailEventFilter', 'PublicPrivacyAnalyticsFilter',
            'PublicAdsSearchFilter', 'PublicAdsTimeFilter',
            'PublicInListFilter', 'PublicUnifiedEventsFilter', and
            'PublicConstantFilter'.
          items:
            oneOf:
              - $ref: '#/components/schemas/PublicPropertyFilter'
              - $ref: '#/components/schemas/PublicAssociationInListFilter'
              - $ref: '#/components/schemas/PublicPageViewAnalyticsFilter'
              - $ref: '#/components/schemas/PublicCtaAnalyticsFilter'
              - $ref: '#/components/schemas/PublicEventAnalyticsFilter'
              - $ref: '#/components/schemas/PublicFormSubmissionFilter'
              - $ref: '#/components/schemas/PublicFormSubmissionOnPageFilter'
              - $ref: '#/components/schemas/PublicIntegrationEventFilter'
              - $ref: '#/components/schemas/PublicEmailSubscriptionFilter'
              - $ref: '#/components/schemas/PublicCommunicationSubscriptionFilter'
              - $ref: '#/components/schemas/PublicSurveyMonkeyFilter'
              - $ref: '#/components/schemas/PublicSurveyMonkeyValueFilter'
              - $ref: '#/components/schemas/PublicWebinarFilter'
              - $ref: '#/components/schemas/PublicEmailEventFilter'
              - $ref: '#/components/schemas/PublicPrivacyAnalyticsFilter'
              - $ref: '#/components/schemas/PublicAdsSearchFilter'
              - $ref: '#/components/schemas/PublicAdsTimeFilter'
              - $ref: '#/components/schemas/PublicInListFilter'
              - $ref: '#/components/schemas/PublicUnifiedEventsFilter'
              - $ref: '#/components/schemas/PublicConstantFilter'
      x-hubspot-sub-type-impl: true
    PublicRestrictedFilterBranch:
      title: RESTRICTED
      required:
        - filterBranchOperator
        - filterBranchType
        - filterBranches
        - filters
      type: object
      properties:
        filterBranchOperator:
          type: string
          description: A string representing the operator used within the filter branch.
        filterBranchType:
          type: string
          description: >-
            A string indicating the type of filter branch. The default value is
            'RESTRICTED'.
          default: RESTRICTED
          enum:
            - RESTRICTED
        filterBranches:
          type: array
          description: >-
            An array of nested filter branches, which can include various types
            such as 'PublicOrFilterBranch', 'PublicAndFilterBranch', and others.
          items:
            oneOf:
              - $ref: '#/components/schemas/PublicOrFilterBranch'
              - $ref: '#/components/schemas/PublicAndFilterBranch'
              - $ref: '#/components/schemas/PublicNotAllFilterBranch'
              - $ref: '#/components/schemas/PublicNotAnyFilterBranch'
              - $ref: '#/components/schemas/PublicRestrictedFilterBranch'
              - $ref: '#/components/schemas/PublicUnifiedEventsFilterBranch'
              - $ref: '#/components/schemas/PublicAssociationFilterBranch'
        filters:
          type: array
          description: >-
            An array of filters applied within the branch, which can include
            different filter types like 'PublicPropertyFilter',
            'PublicAssociationInListFilter', and more.
          items:
            oneOf:
              - $ref: '#/components/schemas/PublicPropertyFilter'
              - $ref: '#/components/schemas/PublicAssociationInListFilter'
              - $ref: '#/components/schemas/PublicPageViewAnalyticsFilter'
              - $ref: '#/components/schemas/PublicCtaAnalyticsFilter'
              - $ref: '#/components/schemas/PublicEventAnalyticsFilter'
              - $ref: '#/components/schemas/PublicFormSubmissionFilter'
              - $ref: '#/components/schemas/PublicFormSubmissionOnPageFilter'
              - $ref: '#/components/schemas/PublicIntegrationEventFilter'
              - $ref: '#/components/schemas/PublicEmailSubscriptionFilter'
              - $ref: '#/components/schemas/PublicCommunicationSubscriptionFilter'
              - $ref: '#/components/schemas/PublicSurveyMonkeyFilter'
              - $ref: '#/components/schemas/PublicSurveyMonkeyValueFilter'
              - $ref: '#/components/schemas/PublicWebinarFilter'
              - $ref: '#/components/schemas/PublicEmailEventFilter'
              - $ref: '#/components/schemas/PublicPrivacyAnalyticsFilter'
              - $ref: '#/components/schemas/PublicAdsSearchFilter'
              - $ref: '#/components/schemas/PublicAdsTimeFilter'
              - $ref: '#/components/schemas/PublicInListFilter'
              - $ref: '#/components/schemas/PublicUnifiedEventsFilter'
              - $ref: '#/components/schemas/PublicConstantFilter'
      x-hubspot-sub-type-impl: true
    PublicUnifiedEventsFilterBranch:
      title: UNIFIED_EVENTS
      required:
        - eventTypeId
        - filterBranchOperator
        - filterBranchType
        - filterBranches
        - filters
        - operator
      type: object
      properties:
        coalescingRefineBy:
          description: >-
            An optional refinement criterion that can be applied to coalesce
            event data. It can be one of several predefined refinement types.
          oneOf:
            - $ref: '#/components/schemas/PublicNumOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicSetOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicRelativeComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicRelativeRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAllHistoryRefineBy'
            - $ref: '#/components/schemas/PublicTimePointOperation'
            - $ref: '#/components/schemas/PublicRangedTimeOperation'
        eventTypeId:
          type: string
          description: A string that specifies the ID of the event type being filtered.
        filterBranchOperator:
          type: string
          description: >-
            A string that specifies the logical operator used to combine the
            filters and filter branches within this branch.
        filterBranchType:
          type: string
          description: >-
            A string indicating the type of filter branch. Default value is
            'UNIFIED_EVENTS'.
          default: UNIFIED_EVENTS
          enum:
            - UNIFIED_EVENTS
        filterBranches:
          type: array
          description: >-
            An array of nested filter branches, allowing for complex filter
            logic. Each item can be one of several filter branch types.
          items:
            oneOf:
              - $ref: '#/components/schemas/PublicOrFilterBranch'
              - $ref: '#/components/schemas/PublicAndFilterBranch'
              - $ref: '#/components/schemas/PublicNotAllFilterBranch'
              - $ref: '#/components/schemas/PublicNotAnyFilterBranch'
              - $ref: '#/components/schemas/PublicRestrictedFilterBranch'
              - $ref: '#/components/schemas/PublicUnifiedEventsFilterBranch'
              - $ref: '#/components/schemas/PublicAssociationFilterBranch'
        filters:
          type: array
          description: >-
            An array of filters applied to the events. Each filter can be one of
            several predefined filter types.
          items:
            oneOf:
              - $ref: '#/components/schemas/PublicPropertyFilter'
              - $ref: '#/components/schemas/PublicAssociationInListFilter'
              - $ref: '#/components/schemas/PublicPageViewAnalyticsFilter'
              - $ref: '#/components/schemas/PublicCtaAnalyticsFilter'
              - $ref: '#/components/schemas/PublicEventAnalyticsFilter'
              - $ref: '#/components/schemas/PublicFormSubmissionFilter'
              - $ref: '#/components/schemas/PublicFormSubmissionOnPageFilter'
              - $ref: '#/components/schemas/PublicIntegrationEventFilter'
              - $ref: '#/components/schemas/PublicEmailSubscriptionFilter'
              - $ref: '#/components/schemas/PublicCommunicationSubscriptionFilter'
              - $ref: '#/components/schemas/PublicSurveyMonkeyFilter'
              - $ref: '#/components/schemas/PublicSurveyMonkeyValueFilter'
              - $ref: '#/components/schemas/PublicWebinarFilter'
              - $ref: '#/components/schemas/PublicEmailEventFilter'
              - $ref: '#/components/schemas/PublicPrivacyAnalyticsFilter'
              - $ref: '#/components/schemas/PublicAdsSearchFilter'
              - $ref: '#/components/schemas/PublicAdsTimeFilter'
              - $ref: '#/components/schemas/PublicInListFilter'
              - $ref: '#/components/schemas/PublicUnifiedEventsFilter'
              - $ref: '#/components/schemas/PublicConstantFilter'
        operator:
          type: string
          description: >-
            A string representing the operation to be performed on the events.
            Valid values are 'HAS_COMPLETED' and 'HAS_NOT_COMPLETED'.
          enum:
            - HAS_COMPLETED
            - HAS_NOT_COMPLETED
        pruningRefineBy:
          description: >-
            An optional refinement criterion used to prune event data. It can be
            one of several predefined refinement types.
          oneOf:
            - $ref: '#/components/schemas/PublicNumOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicSetOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicRelativeComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicRelativeRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAllHistoryRefineBy'
            - $ref: '#/components/schemas/PublicTimePointOperation'
            - $ref: '#/components/schemas/PublicRangedTimeOperation'
      x-hubspot-sub-type-impl: true
    PublicAssociationFilterBranch:
      title: ASSOCIATION
      required:
        - associationCategory
        - associationTypeId
        - filterBranchOperator
        - filterBranchType
        - filterBranches
        - filters
        - objectTypeId
        - operator
      type: object
      properties:
        associationCategory:
          type: string
          description: A string that categorizes the type of association being filtered.
        associationTypeId:
          type: integer
          description: An integer representing the type ID of the association.
          format: int32
        filterBranchOperator:
          type: string
          description: >-
            A string that defines the logical operator for combining filters
            within this branch.
        filterBranchType:
          type: string
          description: >-
            A string indicating the type of filter branch, which is
            'ASSOCIATION' for this component.
          default: ASSOCIATION
          enum:
            - ASSOCIATION
        filterBranches:
          type: array
          description: >-
            An array of nested filter branches, allowing for complex logical
            groupings of filters.
          items:
            oneOf:
              - $ref: '#/components/schemas/PublicOrFilterBranch'
              - $ref: '#/components/schemas/PublicAndFilterBranch'
              - $ref: '#/components/schemas/PublicNotAllFilterBranch'
              - $ref: '#/components/schemas/PublicNotAnyFilterBranch'
              - $ref: '#/components/schemas/PublicRestrictedFilterBranch'
              - $ref: '#/components/schemas/PublicUnifiedEventsFilterBranch'
              - $ref: '#/components/schemas/PublicAssociationFilterBranch'
        filters:
          type: array
          description: >-
            An array of filters applied within this branch, each defining
            specific criteria for filtering associations.
          items:
            oneOf:
              - $ref: '#/components/schemas/PublicPropertyFilter'
              - $ref: '#/components/schemas/PublicAssociationInListFilter'
              - $ref: '#/components/schemas/PublicPageViewAnalyticsFilter'
              - $ref: '#/components/schemas/PublicCtaAnalyticsFilter'
              - $ref: '#/components/schemas/PublicEventAnalyticsFilter'
              - $ref: '#/components/schemas/PublicFormSubmissionFilter'
              - $ref: '#/components/schemas/PublicFormSubmissionOnPageFilter'
              - $ref: '#/components/schemas/PublicIntegrationEventFilter'
              - $ref: '#/components/schemas/PublicEmailSubscriptionFilter'
              - $ref: '#/components/schemas/PublicCommunicationSubscriptionFilter'
              - $ref: '#/components/schemas/PublicSurveyMonkeyFilter'
              - $ref: '#/components/schemas/PublicSurveyMonkeyValueFilter'
              - $ref: '#/components/schemas/PublicWebinarFilter'
              - $ref: '#/components/schemas/PublicEmailEventFilter'
              - $ref: '#/components/schemas/PublicPrivacyAnalyticsFilter'
              - $ref: '#/components/schemas/PublicAdsSearchFilter'
              - $ref: '#/components/schemas/PublicAdsTimeFilter'
              - $ref: '#/components/schemas/PublicInListFilter'
              - $ref: '#/components/schemas/PublicUnifiedEventsFilter'
              - $ref: '#/components/schemas/PublicConstantFilter'
        objectTypeId:
          type: string
          description: >-
            A string representing the type ID of the object involved in the
            association.
        operator:
          type: string
          description: A string that specifies the operator used in the filter logic.
      x-hubspot-sub-type-impl: true
    PublicListPermissions:
      required:
        - teamsWithEditAccess
        - usersWithEditAccess
      type: object
      properties:
        teamsWithEditAccess:
          type: array
          description: >-
            An array of integers representing the IDs of teams that have edit
            access to the list.
          items:
            type: integer
            format: int32
        usersWithEditAccess:
          type: array
          description: >-
            An array of integers representing the IDs of users that have edit
            access to the list.
          items:
            type: integer
            format: int32
    PublicMembershipSettings:
      type: object
      properties:
        includeUnassigned:
          type: boolean
          description: >-
            A boolean indicating whether to include unassigned records in the
            membership settings.
        membershipTeamId:
          type: integer
          description: >-
            A string representing the unique identifier of the team associated
            with the membership settings.
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
    PublicPropertyFilter:
      title: PROPERTY
      required:
        - filterType
        - operation
        - property
      type: object
      properties:
        filterType:
          type: string
          description: >-
            The type of filter being applied. This is a string value that
            specifies the kind of filter operation.
          default: PROPERTY
          enum:
            - PROPERTY
        operation:
          description: >-
            The specific operation or condition used in the filter. This is a
            string value that defines how the filter should be applied to the
            property.
          oneOf:
            - $ref: '#/components/schemas/PublicBoolPropertyOperation'
            - $ref: '#/components/schemas/PublicNumberPropertyOperation'
            - $ref: '#/components/schemas/PublicStringPropertyOperation'
            - $ref: '#/components/schemas/PublicDateTimePropertyOperation'
            - $ref: '#/components/schemas/PublicRangedDatePropertyOperation'
            - $ref: '#/components/schemas/PublicComparativePropertyUpdatedOperation'
            - $ref: '#/components/schemas/PublicComparativeDatePropertyOperation'
            - $ref: '#/components/schemas/PublicRollingDateRangePropertyOperation'
            - $ref: '#/components/schemas/PublicRollingPropertyUpdatedOperation'
            - $ref: '#/components/schemas/PublicEnumerationPropertyOperation'
            - $ref: '#/components/schemas/PublicAllPropertyTypesOperation'
            - $ref: '#/components/schemas/PublicRangedNumberPropertyOperation'
            - $ref: '#/components/schemas/PublicMultiStringPropertyOperation'
            - $ref: '#/components/schemas/PublicDatePropertyOperation'
            - $ref: '#/components/schemas/PublicCalendarDatePropertyOperation'
            - $ref: '#/components/schemas/PublicTimePointOperation'
            - $ref: '#/components/schemas/PublicRangedTimeOperation'
            - $ref: '#/components/schemas/PublicComparativeStringPropertyOperation'
            - $ref: '#/components/schemas/PublicComparativeNumberPropertyOperation'
        property:
          type: string
          description: >-
            The name of the property to which the filter is applied. This is a
            string value representing the property name.
      x-hubspot-sub-type-impl: true
    PublicAssociationInListFilter:
      title: ASSOCIATION
      required:
        - associationCategory
        - associationTypeId
        - coalescingRefineBy
        - filterType
        - listId
        - operator
      type: object
      properties:
        associationCategory:
          type: string
          description: >-
            A string that categorizes the type of association, providing
            additional context for the filter.
        associationTypeId:
          type: integer
          description: >-
            An integer that identifies the specific type of association that is
            being filtered.
          format: int32
        coalescingRefineBy:
          description: >-
            An optional refinement criterion that can be applied to the filter.
            It can be one of several types, such as PublicNumOccurrencesRefineBy
            or PublicRelativeComparativeTimestampRefineBy.
          oneOf:
            - $ref: '#/components/schemas/PublicNumOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicSetOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicRelativeComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicRelativeRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAllHistoryRefineBy'
            - $ref: '#/components/schemas/PublicTimePointOperation'
            - $ref: '#/components/schemas/PublicRangedTimeOperation'
        filterType:
          type: string
          description: >-
            A string that specifies the type of filter being applied. The
            default value is 'IN_LIST'.
          default: ASSOCIATION
          enum:
            - ASSOCIATION
        listId:
          type: string
          description: >-
            A string representing the unique identifier of the list to which the
            filter is applied.
        operator:
          type: string
          description: >-
            A string that defines the operator used in the filter. This
            determines how the filter criteria are applied.
        toObjectType:
          type: string
          description: >-
            A string that describes the type of object to which the association
            is related.
        toObjectTypeId:
          type: string
          description: >-
            A string that specifies the type ID of the object to which the
            association is related.
      x-hubspot-sub-type-impl: true
    PublicPageViewAnalyticsFilter:
      title: PAGE_VIEW
      required:
        - filterType
        - operator
        - pageUrl
      type: object
      properties:
        coalescingRefineBy:
          description: >-
            An optional property that defines the method for refining the filter
            by coalescing multiple conditions. It can be one of several
            predefined refine types.
          oneOf:
            - $ref: '#/components/schemas/PublicNumOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicSetOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicRelativeComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicRelativeRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAllHistoryRefineBy'
            - $ref: '#/components/schemas/PublicTimePointOperation'
            - $ref: '#/components/schemas/PublicRangedTimeOperation'
        enableTracking:
          type: boolean
          description: >-
            A boolean value that indicates whether tracking is enabled for the
            page view analytics filter.
        filterType:
          type: string
          description: >-
            A string representing the type of filter being applied. This
            property determines the category of the filter used in the
            analytics.
          default: PAGE_VIEW
          enum:
            - PAGE_VIEW
        operator:
          type: string
          description: >-
            A string indicating the operator used in the filter, which defines
            how the filter criteria are applied.
        pageUrl:
          type: string
          description: >-
            A string representing the specific URL of the page to be tracked or
            analyzed. This property is used to filter analytics data based on
            page URL.
        pruningRefineBy:
          description: >-
            An optional property that specifies the method for refining the
            filter by pruning conditions. It can be one of several predefined
            refine types.
          oneOf:
            - $ref: '#/components/schemas/PublicNumOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicSetOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicRelativeComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicRelativeRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAllHistoryRefineBy'
            - $ref: '#/components/schemas/PublicTimePointOperation'
            - $ref: '#/components/schemas/PublicRangedTimeOperation'
      x-hubspot-sub-type-impl: true
    PublicCtaAnalyticsFilter:
      title: CTA
      required:
        - ctaName
        - filterType
        - operator
      type: object
      properties:
        coalescingRefineBy:
          description: >-
            An optional refinement criterion that can be one of several types,
            such as number of occurrences or time-based refinements.
          oneOf:
            - $ref: '#/components/schemas/PublicNumOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicSetOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicRelativeComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicRelativeRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAllHistoryRefineBy'
            - $ref: '#/components/schemas/PublicTimePointOperation'
            - $ref: '#/components/schemas/PublicRangedTimeOperation'
        ctaName:
          type: string
          description: >-
            The name of the Call-To-Action being filtered for in the analytics
            data.
        filterType:
          type: string
          description: >-
            A string indicating the type of filter being applied. Defaults to
            'CTA'.
          default: CTA
          enum:
            - CTA
        operator:
          type: string
          description: A string representing the operation to be performed by the filter.
        pruningRefineBy:
          description: >-
            An optional refinement criterion used to further narrow down the
            filter results, similar to coalescingRefineBy.
          oneOf:
            - $ref: '#/components/schemas/PublicNumOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicSetOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicRelativeComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicRelativeRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAllHistoryRefineBy'
            - $ref: '#/components/schemas/PublicTimePointOperation'
            - $ref: '#/components/schemas/PublicRangedTimeOperation'
      x-hubspot-sub-type-impl: true
    PublicEventAnalyticsFilter:
      title: EVENT
      required:
        - eventId
        - filterType
        - operator
      type: object
      properties:
        coalescingRefineBy:
          description: >-
            An optional property that allows for additional refinement of the
            filter criteria using a coalescing method. It can be one of several
            predefined refinement types.
          oneOf:
            - $ref: '#/components/schemas/PublicNumOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicSetOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicRelativeComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicRelativeRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAllHistoryRefineBy'
            - $ref: '#/components/schemas/PublicTimePointOperation'
            - $ref: '#/components/schemas/PublicRangedTimeOperation'
        eventId:
          type: string
          description: >-
            A string representing the unique identifier of the event to be
            filtered. This property is required.
        filterType:
          type: string
          description: >-
            A string representing the type of filter being applied. This
            property is required.
          default: EVENT
          enum:
            - EVENT
        operator:
          type: string
          description: >-
            A string that specifies the operator used in the filter. This
            property is required.
        pruningRefineBy:
          description: >-
            An optional property that allows for additional refinement of the
            filter criteria using a pruning method. It can be one of several
            predefined refinement types.
          oneOf:
            - $ref: '#/components/schemas/PublicNumOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicSetOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicRelativeComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicRelativeRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAllHistoryRefineBy'
            - $ref: '#/components/schemas/PublicTimePointOperation'
            - $ref: '#/components/schemas/PublicRangedTimeOperation'
      x-hubspot-sub-type-impl: true
    PublicFormSubmissionFilter:
      title: FORM_SUBMISSION
      required:
        - filterType
        - operator
      type: object
      properties:
        coalescingRefineBy:
          description: >-
            An optional refinement criterion used to coalesce form submissions
            based on specific conditions. It can be one of several types,
            similar to pruningRefineBy.
          oneOf:
            - $ref: '#/components/schemas/PublicNumOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicSetOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicRelativeComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicRelativeRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAllHistoryRefineBy'
            - $ref: '#/components/schemas/PublicTimePointOperation'
            - $ref: '#/components/schemas/PublicRangedTimeOperation'
        filterType:
          type: string
          description: >-
            A string that specifies the type of filter being applied. The
            default value is 'FORM_SUBMISSION'.
          default: FORM_SUBMISSION
          enum:
            - FORM_SUBMISSION
        formId:
          type: string
          description: >-
            A string representing the unique identifier of the form to which the
            filter applies.
        operator:
          type: string
          description: >-
            A string that defines the operation to be performed by the filter.
            Valid values include 'FILLED_OUT' and 'NOT_FILLED_OUT'.
          enum:
            - FILLED_OUT
            - NOT_FILLED_OUT
        pruningRefineBy:
          description: >-
            An optional refinement criterion that further specifies the
            conditions for pruning form submissions. It can be one of several
            types, such as number of occurrences or timestamp comparisons.
          oneOf:
            - $ref: '#/components/schemas/PublicNumOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicSetOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicRelativeComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicRelativeRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAllHistoryRefineBy'
            - $ref: '#/components/schemas/PublicTimePointOperation'
            - $ref: '#/components/schemas/PublicRangedTimeOperation'
      x-hubspot-sub-type-impl: true
    PublicFormSubmissionOnPageFilter:
      title: FORM_SUBMISSION_ON_PAGE
      required:
        - filterType
        - operator
        - pageId
      type: object
      properties:
        coalescingRefineBy:
          description: >-
            An optional refinement criterion used to coalesce results based on
            specific conditions, similar to pruningRefineBy.
          oneOf:
            - $ref: '#/components/schemas/PublicNumOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicSetOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicRelativeComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicRelativeRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAllHistoryRefineBy'
            - $ref: '#/components/schemas/PublicTimePointOperation'
            - $ref: '#/components/schemas/PublicRangedTimeOperation'
        filterType:
          type: string
          description: The type of filter applied, which is fixed as 'FORM_SUBMISSION'.
          default: FORM_SUBMISSION_ON_PAGE
          enum:
            - FORM_SUBMISSION_ON_PAGE
        formId:
          type: string
          description: >-
            A string representing the unique identifier of the form to be
            filtered.
        operator:
          type: string
          description: >-
            The operation to be performed by the filter. It is a string and can
            have values such as 'FILLED_OUT' or 'NOT_FILLED_OUT'.
          enum:
            - FILLED_OUT
            - NOT_FILLED_OUT
        pageId:
          type: string
          description: >-
            A string representing the unique identifier of the page where the
            form submission occurred.
        pruningRefineBy:
          description: >-
            An optional property that allows further refinement of the filter
            using various criteria such as occurrences or time ranges.
          oneOf:
            - $ref: '#/components/schemas/PublicNumOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicSetOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicRelativeComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicRelativeRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAllHistoryRefineBy'
            - $ref: '#/components/schemas/PublicTimePointOperation'
            - $ref: '#/components/schemas/PublicRangedTimeOperation'
      x-hubspot-sub-type-impl: true
    PublicIntegrationEventFilter:
      title: INTEGRATION_EVENT
      required:
        - eventTypeId
        - filterLines
        - filterType
      type: object
      properties:
        eventTypeId:
          type: integer
          description: >-
            A string that uniquely identifies the type of event to be filtered.
            This property is required.
          format: int32
        filterLines:
          type: array
          description: >-
            An array of filter lines that define additional filtering criteria.
            Each filter line is an object that specifies conditions for
            filtering events.
          items:
            $ref: '#/components/schemas/PublicEventFilterMetadata'
        filterType:
          type: string
          description: >-
            A string representing the type of filter being applied. This
            property is required.
          default: INTEGRATION_EVENT
          enum:
            - INTEGRATION_EVENT
      x-hubspot-sub-type-impl: true
    PublicEmailSubscriptionFilter:
      title: EMAIL_SUBSCRIPTION
      required:
        - acceptedStatuses
        - filterType
        - subscriptionIds
      type: object
      properties:
        acceptedStatuses:
          type: array
          description: >-
            An array of strings indicating the statuses that are accepted for
            the filter.
          items:
            type: string
        filterType:
          type: string
          description: >-
            A string indicating the type of filter. The default value is
            'EMAIL_SUBSCRIPTION'.
          default: EMAIL_SUBSCRIPTION
          enum:
            - EMAIL_SUBSCRIPTION
        subscriptionIds:
          type: array
          description: >-
            An array of strings representing the IDs of the subscriptions to
            filter by.
          items:
            type: string
        subscriptionType:
          type: string
          description: A string representing the type of subscription to filter by.
      x-hubspot-sub-type-impl: true
    PublicCommunicationSubscriptionFilter:
      title: COMMUNICATION_SUBSCRIPTION
      required:
        - acceptedOptStates
        - channel
        - filterType
        - subscriptionIds
        - subscriptionType
      type: object
      properties:
        acceptedOptStates:
          type: array
          description: >-
            An array of strings representing the opt-in states that are accepted
            for the subscription.
          items:
            type: string
        businessUnitId:
          type: string
          description: >-
            A string representing the ID of the business unit associated with
            the subscription.
        channel:
          type: string
          description: A string indicating the communication channel for the subscription.
        filterType:
          type: string
          description: >-
            A string representing the type of filter. Defaults to
            'COMMUNICATION_SUBSCRIPTION'.
          default: COMMUNICATION_SUBSCRIPTION
          enum:
            - COMMUNICATION_SUBSCRIPTION
        subscriptionIds:
          type: array
          description: >-
            An array of strings representing the IDs of the subscriptions to be
            filtered.
          items:
            type: string
        subscriptionType:
          type: string
          description: A string indicating the type of subscription being filtered.
      x-hubspot-sub-type-impl: true
    PublicSurveyMonkeyFilter:
      title: SURVEY_MONKEY
      required:
        - filterType
        - operator
        - surveyId
      type: object
      properties:
        filterType:
          type: string
          description: >-
            A string representing the type of filter. The default value is
            'SURVEY_MONKEY_VALUE'.
          default: SURVEY_MONKEY
          enum:
            - SURVEY_MONKEY
        operator:
          type: string
          description: >-
            A string that specifies the operation to be performed for the
            filter.
        surveyId:
          type: string
          description: >-
            A string that uniquely identifies the survey from which the data is
            being filtered.
      x-hubspot-sub-type-impl: true
    PublicSurveyMonkeyValueFilter:
      title: SURVEY_MONKEY_VALUE
      required:
        - filterType
        - operator
        - surveyId
        - surveyQuestion
        - valueComparison
      type: object
      properties:
        filterType:
          type: string
          description: >-
            A string that specifies the type of filter being applied. Default
            value is 'SURVEY_MONKEY_VALUE'.
          default: SURVEY_MONKEY_VALUE
          enum:
            - SURVEY_MONKEY_VALUE
        operator:
          type: string
          description: >-
            A string that specifies the operator used in the filter, determining
            how the survey data should be evaluated against the specified
            criteria.
        surveyAnswerColId:
          type: string
          description: >-
            A string representing the column identifier for the survey answer
            being filtered.
        surveyAnswerRowId:
          type: string
          description: >-
            A string representing the row identifier for the survey answer being
            filtered.
        surveyId:
          type: string
          description: >-
            A string representing the unique identifier of the SurveyMonkey
            survey.
        surveyQuestion:
          type: string
          description: >-
            A string indicating the specific question within the survey that the
            filter is targeting.
        valueComparison:
          description: >-
            An object that defines the operation for comparing values, which can
            be one of several types such as boolean, number, string, date, or
            enumeration operations.
          oneOf:
            - $ref: '#/components/schemas/PublicBoolPropertyOperation'
            - $ref: '#/components/schemas/PublicNumberPropertyOperation'
            - $ref: '#/components/schemas/PublicStringPropertyOperation'
            - $ref: '#/components/schemas/PublicDateTimePropertyOperation'
            - $ref: '#/components/schemas/PublicRangedDatePropertyOperation'
            - $ref: '#/components/schemas/PublicComparativePropertyUpdatedOperation'
            - $ref: '#/components/schemas/PublicComparativeDatePropertyOperation'
            - $ref: '#/components/schemas/PublicRollingDateRangePropertyOperation'
            - $ref: '#/components/schemas/PublicRollingPropertyUpdatedOperation'
            - $ref: '#/components/schemas/PublicEnumerationPropertyOperation'
            - $ref: '#/components/schemas/PublicAllPropertyTypesOperation'
            - $ref: '#/components/schemas/PublicRangedNumberPropertyOperation'
            - $ref: '#/components/schemas/PublicMultiStringPropertyOperation'
            - $ref: '#/components/schemas/PublicDatePropertyOperation'
            - $ref: '#/components/schemas/PublicCalendarDatePropertyOperation'
            - $ref: '#/components/schemas/PublicTimePointOperation'
            - $ref: '#/components/schemas/PublicRangedTimeOperation'
            - $ref: '#/components/schemas/PublicComparativeStringPropertyOperation'
            - $ref: '#/components/schemas/PublicComparativeNumberPropertyOperation'
      x-hubspot-sub-type-impl: true
    PublicWebinarFilter:
      title: WEBINAR
      required:
        - filterType
        - operator
      type: object
      properties:
        filterType:
          type: string
          description: >-
            A string that specifies the type of filter being applied. The
            default value is 'WEBINAR'.
          default: WEBINAR
          enum:
            - WEBINAR
        operator:
          type: string
          description: >-
            A string that defines the operation or condition applied by the
            filter.
        webinarId:
          type: string
          description: >-
            A string representing the unique identifier of the webinar to which
            the filter is applied.
      x-hubspot-sub-type-impl: true
    PublicEmailEventFilter:
      title: EMAIL_EVENT
      required:
        - appId
        - emailId
        - filterType
        - level
        - operator
      type: object
      properties:
        appId:
          type: string
          description: >-
            A string representing the application ID associated with the email
            event.
        clickUrl:
          type: string
          description: A string representing the URL that is clicked in the email event.
        emailId:
          type: string
          description: >-
            A string representing the unique identifier of the email associated
            with the event.
        filterType:
          type: string
          description: >-
            A string representing the type of filter being applied. This
            property is required.
          default: EMAIL_EVENT
          enum:
            - EMAIL_EVENT
        level:
          type: string
          description: A string indicating the level of the email event filter.
        operator:
          type: string
          description: A string that specifies the operator used in the filter condition.
          enum:
            - BOUNCED
            - LINK_CLICKED
            - MARKED_SPAM
            - OPENED
            - OPENED_BUT_LINK_NOT_CLICKED
            - OPENED_BUT_NOT_REPLIED
            - RECEIVED
            - RECEIVED_BUT_NOT_OPENED
            - REPLIED
            - SENT
            - SENT_BUT_LINK_NOT_CLICKED
            - SENT_BUT_NOT_RECEIVED
            - UNSUBSCRIBED
        pruningRefineBy:
          description: >-
            An object that provides additional criteria for refining the filter.
            It can be one of several types such as PublicNumOccurrencesRefineBy,
            PublicSetOccurrencesRefineBy, etc.
          oneOf:
            - $ref: '#/components/schemas/PublicNumOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicSetOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicRelativeComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicRelativeRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAllHistoryRefineBy'
            - $ref: '#/components/schemas/PublicTimePointOperation'
            - $ref: '#/components/schemas/PublicRangedTimeOperation'
      x-hubspot-sub-type-impl: true
    PublicPrivacyAnalyticsFilter:
      title: PRIVACY
      required:
        - filterType
        - operator
        - privacyName
      type: object
      properties:
        filterType:
          type: string
          description: >-
            A string representing the type of filter. The default value is
            'PRIVACY_ANALYTICS'.
          default: PRIVACY
          enum:
            - PRIVACY
        operator:
          type: string
          description: A string that defines the operator used in the filter condition.
        privacyName:
          type: string
          description: >-
            A string that specifies the name of the privacy setting being
            filtered.
      x-hubspot-sub-type-impl: true
    PublicAdsSearchFilter:
      title: ADS_SEARCH
      required:
        - adNetwork
        - entityType
        - filterType
        - operator
        - searchTermType
        - searchTerms
      type: object
      properties:
        adNetwork:
          type: string
          description: >-
            The advertising network being targeted by the filter. This is a
            string value indicating the ad network.
        entityType:
          type: string
          description: >-
            The type of entity to which the filter is applied. This is a string
            value representing the entity type.
        filterType:
          type: string
          description: >-
            The type of filter being applied. This is a string value that
            defines the category or nature of the filter.
          default: ADS_SEARCH
          enum:
            - ADS_SEARCH
        operator:
          type: string
          description: >-
            The operator used to apply the filter. This is a string value that
            specifies the logical operation for the filter.
        searchTermType:
          type: string
          description: >-
            The type of search term used in the filter. This is a string value
            that specifies how the search term is interpreted.
        searchTerms:
          type: array
          description: >-
            An array of strings representing the search terms used in the
            filter.
          items:
            type: string
      x-hubspot-sub-type-impl: true
    PublicAdsTimeFilter:
      title: ADS_TIME
      required:
        - filterType
        - pruningRefineBy
      type: object
      properties:
        filterType:
          type: string
          description: >-
            A string representing the type of filter being applied. The default
            value is 'ADS_TIME'.
          default: ADS_TIME
          enum:
            - ADS_TIME
        pruningRefineBy:
          description: >-
            An optional property that allows further refinement of the filter
            criteria based on time. It can be one of several types, such as
            relative or absolute time comparisons.
          oneOf:
            - $ref: '#/components/schemas/PublicNumOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicSetOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicRelativeComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicRelativeRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAllHistoryRefineBy'
            - $ref: '#/components/schemas/PublicTimePointOperation'
            - $ref: '#/components/schemas/PublicRangedTimeOperation'
      x-hubspot-sub-type-impl: true
    PublicInListFilter:
      title: IN_LIST
      required:
        - filterType
        - listId
        - operator
      type: object
      properties:
        filterType:
          type: string
          description: A string indicating the type of filter. Defaults to 'IN_LIST'.
          default: IN_LIST
          enum:
            - IN_LIST
        listId:
          type: string
          description: >-
            The unique identifier of the list to check for membership,
            represented as a string.
        metadata:
          $ref: '#/components/schemas/PublicInListFilterMetadata'
        operator:
          type: string
          description: A string representing the operator used in the filter.
      x-hubspot-sub-type-impl: true
    PublicUnifiedEventsFilter:
      title: UNIFIED_EVENTS
      required:
        - filterLines
        - filterType
      type: object
      properties:
        coalescingRefineBy:
          description: >-
            An optional refinement condition used to coalesce events based on
            specific criteria, such as number of occurrences or time range.
          oneOf:
            - $ref: '#/components/schemas/PublicNumOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicSetOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicRelativeComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicRelativeRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAllHistoryRefineBy'
            - $ref: '#/components/schemas/PublicTimePointOperation'
            - $ref: '#/components/schemas/PublicRangedTimeOperation'
        eventTypeId:
          type: string
          description: >-
            A string representing the unique identifier for the event type being
            filtered.
        filterLines:
          type: array
          description: >-
            An array of filters that are applied to the events. Each filter
            specifies additional criteria for refining the event data.
          items:
            $ref: '#/components/schemas/PublicEventFilterMetadata'
        filterType:
          type: string
          description: >-
            A string that specifies the type of filter, defaulting to
            'UNIFIED_EVENTS'.
          default: UNIFIED_EVENTS
          enum:
            - UNIFIED_EVENTS
        pruningRefineBy:
          description: >-
            An optional refinement condition used to prune the events based on
            specific criteria, such as number of occurrences or time range.
          oneOf:
            - $ref: '#/components/schemas/PublicNumOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicSetOccurrencesRefineBy'
            - $ref: '#/components/schemas/PublicRelativeComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicRelativeRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteComparativeTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAbsoluteRangedTimestampRefineBy'
            - $ref: '#/components/schemas/PublicAllHistoryRefineBy'
            - $ref: '#/components/schemas/PublicTimePointOperation'
            - $ref: '#/components/schemas/PublicRangedTimeOperation'
      x-hubspot-sub-type-impl: true
    PublicConstantFilter:
      title: CONSTANT
      required:
        - filterType
        - shouldAccept
      type: object
      properties:
        filterType:
          type: string
          description: >-
            A string that specifies the type of filter. For this component, it
            is a constant value indicating the filter's nature.
          default: CONSTANT
          enum:
            - CONSTANT
        shouldAccept:
          type: boolean
          description: >-
            A boolean indicating whether the filter condition should be accepted
            or not.
        source:
          type: string
          description: >-
            A string that represents the origin or context of the filter,
            providing additional information about where or how the filter is
            applied.
      x-hubspot-sub-type-impl: true
    PublicNumOccurrencesRefineBy:
      title: NUM_OCCURRENCES
      required:
        - type
      type: object
      properties:
        maxOccurrences:
          type: integer
          description: An integer specifying the maximum number of occurrences allowed.
          format: int32
        minOccurrences:
          type: integer
          description: An integer specifying the minimum number of occurrences required.
          format: int32
        type:
          type: string
          description: >-
            A string indicating the type of refinement, which is
            'NUM_OCCURRENCES' by default.
          default: NUM_OCCURRENCES
          enum:
            - NUM_OCCURRENCES
      x-hubspot-sub-type-impl: true
    PublicSetOccurrencesRefineBy:
      title: SET_OCCURRENCES
      required:
        - setType
        - type
      type: object
      properties:
        setType:
          type: string
          description: A string specifying the set type used for the refinement.
        type:
          type: string
          description: >-
            A string indicating the type of refinement, which is
            'SET_OCCURRENCES'.
          default: SET_OCCURRENCES
          enum:
            - SET_OCCURRENCES
      x-hubspot-sub-type-impl: true
    PublicRelativeComparativeTimestampRefineBy:
      title: RELATIVE_COMPARATIVE
      required:
        - comparison
        - timeOffset
        - type
      type: object
      properties:
        comparison:
          type: string
          description: >-
            A string that defines the comparison operation to be used in the
            refinement.
        timeOffset:
          $ref: '#/components/schemas/PublicTimeOffset'
        type:
          type: string
          description: >-
            A string that specifies the type of refinement, with the default
            value 'RELATIVE_COMPARATIVE'.
          default: RELATIVE_COMPARATIVE
          enum:
            - RELATIVE_COMPARATIVE
      x-hubspot-sub-type-impl: true
    PublicRelativeRangedTimestampRefineBy:
      title: RELATIVE_RANGED
      required:
        - lowerBoundOffset
        - rangeType
        - type
        - upperBoundOffset
      type: object
      properties:
        lowerBoundOffset:
          $ref: '#/components/schemas/PublicTimeOffset'
        rangeType:
          type: string
          description: A string that specifies the type of range being applied.
        type:
          type: string
          description: >-
            A string indicating the type of refinement, with a default value of
            'RELATIVE_RANGED'.
          default: RELATIVE_RANGED
          enum:
            - RELATIVE_RANGED
        upperBoundOffset:
          $ref: '#/components/schemas/PublicTimeOffset'
      x-hubspot-sub-type-impl: true
    PublicAbsoluteComparativeTimestampRefineBy:
      title: ABSOLUTE_COMPARATIVE
      required:
        - comparison
        - timestamp
        - type
      type: object
      properties:
        comparison:
          type: string
          description: >-
            A string representing the comparison operation to be performed with
            the timestamp.
        timestamp:
          type: integer
          description: >-
            An integer representing the specific timestamp to be used in the
            comparison, typically expressed as a Unix timestamp in milliseconds.
          format: int64
        type:
          type: string
          description: >-
            A string representing the type of refinement, which is
            'ABSOLUTE_COMPARATIVE' by default.
          default: ABSOLUTE_COMPARATIVE
          enum:
            - ABSOLUTE_COMPARATIVE
      x-hubspot-sub-type-impl: true
    PublicAbsoluteRangedTimestampRefineBy:
      title: ABSOLUTE_RANGED
      required:
        - lowerTimestamp
        - rangeType
        - type
        - upperTimestamp
      type: object
      properties:
        lowerTimestamp:
          type: integer
          description: >-
            An integer representing the lower bound of the timestamp range, in
            Unix time format (milliseconds).
          format: int64
        rangeType:
          type: string
          description: A string that specifies the type of range being used in the filter.
        type:
          type: string
          description: >-
            A string that indicates the type of refine by operation, which is
            'ABSOLUTE_RANGED'.
          default: ABSOLUTE_RANGED
          enum:
            - ABSOLUTE_RANGED
        upperTimestamp:
          type: integer
          description: >-
            An integer representing the upper bound of the timestamp range, in
            Unix time format (milliseconds).
          format: int64
      x-hubspot-sub-type-impl: true
    PublicAllHistoryRefineBy:
      title: ALL_HISTORY
      required:
        - type
      type: object
      properties:
        type:
          type: string
          description: >-
            A string that specifies the type of refinement, with a default value
            of 'ALL_HISTORY'.
          default: ALL_HISTORY
          enum:
            - ALL_HISTORY
      x-hubspot-sub-type-impl: true
    PublicTimePointOperation:
      title: TIME_POINT
      required:
        - includeObjectsWithNoValueSet
        - operationType
        - operator
        - timePoint
        - type
      type: object
      properties:
        endpointBehavior:
          type: string
          description: >-
            A string describing the behavior of the endpoint in the context of
            the time point operation.
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether to include objects that have no value
            set for the time point.
        operationType:
          type: string
          description: >-
            A string indicating the type of operation, which is 'TIME_POINT' by
            default.
          default: TIME_POINT
          enum:
            - TIME_POINT
        operator:
          type: string
          description: A string representing the operator used in the time point operation.
        propertyParser:
          type: string
          description: >-
            A string representing the parser used for the property in the time
            point operation.
        timePoint:
          description: >-
            An object representing the specific time point used in the
            operation. It can be one of several types, such as a date point,
            indexed time point, or property-referenced time.
          oneOf:
            - $ref: '#/components/schemas/PublicDatePoint'
            - $ref: '#/components/schemas/PublicIndexedTimePoint'
            - $ref: '#/components/schemas/PublicPropertyReferencedTime'
        type:
          type: string
          description: A string indicating the specific type of the time point operation.
      x-hubspot-sub-type-impl: true
    PublicRangedTimeOperation:
      title: TIME_RANGED
      required:
        - includeObjectsWithNoValueSet
        - lowerBoundTimePoint
        - operationType
        - operator
        - type
        - upperBoundTimePoint
      type: object
      properties:
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether objects with no value set should be
            included in the operation.
        lowerBoundEndpointBehavior:
          type: string
          description: >-
            A string specifying the behavior of the lower bound endpoint in the
            time range.
        lowerBoundTimePoint:
          description: >-
            An object representing the lower bound time point of the range,
            which can be a date point, indexed time point, or
            property-referenced time.
          oneOf:
            - $ref: '#/components/schemas/PublicDatePoint'
            - $ref: '#/components/schemas/PublicIndexedTimePoint'
            - $ref: '#/components/schemas/PublicPropertyReferencedTime'
        operationType:
          type: string
          description: >-
            A string indicating the operation type, which is related to time
            range operations.
        operator:
          type: string
          description: A string representing the operator used in the time range operation.
        propertyParser:
          type: string
          description: A string that defines the property parser used in the operation.
        type:
          type: string
          description: A string indicating the type of operation, which is 'TIME_RANGED'.
          default: TIME_RANGED
          enum:
            - TIME_RANGED
        upperBoundEndpointBehavior:
          type: string
          description: >-
            A string specifying the behavior of the upper bound endpoint in the
            time range.
        upperBoundTimePoint:
          description: >-
            An object representing the upper bound time point of the range,
            which can be a date point, indexed time point, or
            property-referenced time.
          oneOf:
            - $ref: '#/components/schemas/PublicDatePoint'
            - $ref: '#/components/schemas/PublicIndexedTimePoint'
            - $ref: '#/components/schemas/PublicPropertyReferencedTime'
      x-hubspot-sub-type-impl: true
    PublicBoolPropertyOperation:
      title: BOOL
      required:
        - includeObjectsWithNoValueSet
        - operationType
        - operator
        - value
      type: object
      properties:
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether objects with no value set should be
            included in the operation.
        operationType:
          type: string
          description: >-
            A string indicating the type of operation. The default value is
            'BOOLEAN'.
          default: BOOL
          enum:
            - BOOL
        operator:
          type: string
          description: A string representing the operator used in the operation.
        value:
          type: boolean
          description: A boolean representing the value to be used in the operation.
      x-hubspot-sub-type-impl: true
    PublicNumberPropertyOperation:
      title: NUMBER
      required:
        - includeObjectsWithNoValueSet
        - operationType
        - operator
        - value
      type: object
      properties:
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether to include objects that do not have a
            value set for the property.
        operationType:
          type: string
          description: >-
            A string indicating the type of operation. The default value is
            'NUMBER'.
          default: NUMBER
          enum:
            - NUMBER
        operator:
          type: string
          description: A string representing the operator used in the operation.
        value:
          type: number
          description: A number representing the value involved in the operation.
      x-hubspot-sub-type-impl: true
    PublicStringPropertyOperation:
      title: STRING
      required:
        - includeObjectsWithNoValueSet
        - operationType
        - operator
        - value
      type: object
      properties:
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether to include objects that have no value
            set for the property.
        operationType:
          type: string
          description: >-
            A string indicating the type of operation. The default value is
            'STRING'.
          default: STRING
          enum:
            - STRING
        operator:
          type: string
          description: A string representing the operator used in the operation.
        value:
          type: string
          description: A string representing the value involved in the operation.
      x-hubspot-sub-type-impl: true
    PublicDateTimePropertyOperation:
      title: DATETIME
      required:
        - includeObjectsWithNoValueSet
        - operationType
        - operator
        - requiresTimeZoneConversion
        - timestamp
      type: object
      properties:
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether objects with no value set for the
            property should be included in the operation.
        operationType:
          type: string
          description: >-
            A string representing the type of operation being performed. The
            default value is 'DATE_TIME'.
          default: DATETIME
          enum:
            - DATETIME
        operator:
          type: string
          description: A string specifying the operator used in the operation.
        requiresTimeZoneConversion:
          type: boolean
          description: >-
            A boolean indicating whether the operation requires conversion based
            on time zones.
        timestamp:
          type: integer
          description: >-
            An integer representing a Unix timestamp in milliseconds, used as a
            reference point for the operation.
          format: int64
      x-hubspot-sub-type-impl: true
    PublicRangedDatePropertyOperation:
      title: RANGED_DATE
      required:
        - includeObjectsWithNoValueSet
        - lowerBound
        - operationType
        - operator
        - requiresTimeZoneConversion
        - upperBound
      type: object
      properties:
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether to include objects that do not have a
            value set for the property.
        lowerBound:
          type: integer
          description: >-
            An integer representing the lower bound of the date range, formatted
            as an int64.
          format: int64
        operationType:
          type: string
          description: >-
            A string that indicates the type of operation, which is
            'RANGED_DATE' by default.
          default: RANGED_DATE
          enum:
            - RANGED_DATE
        operator:
          type: string
          description: A string representing the operator used in the operation.
        requiresTimeZoneConversion:
          type: boolean
          description: >-
            A boolean indicating whether the operation requires time zone
            conversion.
        upperBound:
          type: integer
          description: >-
            An integer representing the upper bound of the date range, formatted
            as an int64.
          format: int64
      x-hubspot-sub-type-impl: true
    PublicComparativePropertyUpdatedOperation:
      title: COMPARATIVE_PROPERTY_UPDATED
      required:
        - comparisonPropertyName
        - includeObjectsWithNoValueSet
        - operationType
        - operator
      type: object
      properties:
        comparisonPropertyName:
          type: string
          description: A string specifying the name of the property to be compared.
        defaultComparisonValue:
          type: string
          description: >-
            A string representing the default value to use in the comparison if
            no other value is set.
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether objects with no value set should be
            included in the operation.
        operationType:
          type: string
          description: >-
            A string indicating the type of operation. Defaults to
            'COMPARATIVE_STRING'.
          default: COMPARATIVE_PROPERTY_UPDATED
          enum:
            - COMPARATIVE_PROPERTY_UPDATED
        operator:
          type: string
          description: A string representing the operator used in the comparison.
      x-hubspot-sub-type-impl: true
    PublicComparativeDatePropertyOperation:
      title: COMPARATIVE_DATE
      required:
        - comparisonPropertyName
        - includeObjectsWithNoValueSet
        - operationType
        - operator
      type: object
      properties:
        comparisonPropertyName:
          type: string
          description: >-
            A string specifying the name of the property to be used for
            comparison.
        defaultComparisonValue:
          type: string
          description: >-
            A string representing the default value to be used in the comparison
            if no specific value is set.
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether to include objects that do not have a
            value set for the property being compared.
        operationType:
          type: string
          description: >-
            A string indicating the type of operation, with a default value of
            'COMPARATIVE_DATE'.
          default: COMPARATIVE_DATE
          enum:
            - COMPARATIVE_DATE
        operator:
          type: string
          description: A string representing the operator used in the comparison.
      x-hubspot-sub-type-impl: true
    PublicRollingDateRangePropertyOperation:
      title: ROLLING_DATE_RANGE
      required:
        - includeObjectsWithNoValueSet
        - numberOfDays
        - operationType
        - operator
        - requiresTimeZoneConversion
      type: object
      properties:
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether to include objects that do not have a
            value set for the property being filtered.
        numberOfDays:
          type: integer
          description: An integer specifying the number of days for the rolling date range.
          format: int32
        operationType:
          type: string
          description: >-
            A string indicating the type of operation, which is
            'ROLLING_DATE_RANGE' by default.
          default: ROLLING_DATE_RANGE
          enum:
            - ROLLING_DATE_RANGE
        operator:
          type: string
          description: A string representing the operator used in the filter operation.
        requiresTimeZoneConversion:
          type: boolean
          description: >-
            A boolean indicating whether the operation requires time zone
            conversion.
      x-hubspot-sub-type-impl: true
    PublicRollingPropertyUpdatedOperation:
      title: ROLLING_PROPERTY_UPDATED
      required:
        - includeObjectsWithNoValueSet
        - numberOfDays
        - operationType
        - operator
      type: object
      properties:
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether objects with no value set should be
            included in the operation.
        numberOfDays:
          type: integer
          description: >-
            An integer specifying the number of days over which the rolling
            operation is applied.
          format: int32
        operationType:
          type: string
          description: >-
            A string indicating the type of operation, defaulting to
            'ROLLING_PROPERTY_UPDATED'.
          default: ROLLING_PROPERTY_UPDATED
          enum:
            - ROLLING_PROPERTY_UPDATED
        operator:
          type: string
          description: A string representing the operator used in the operation.
      x-hubspot-sub-type-impl: true
    PublicEnumerationPropertyOperation:
      title: ENUMERATION
      required:
        - includeObjectsWithNoValueSet
        - operationType
        - operator
        - values
      type: object
      properties:
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether objects with no value set should be
            included in the operation.
        operationType:
          type: string
          description: >-
            A string indicating the type of operation, with a default value of
            'ENUMERATION'.
          default: ENUMERATION
          enum:
            - ENUMERATION
        operator:
          type: string
          description: >-
            A string representing the operator used in the enumeration
            operation.
        values:
          type: array
          description: >-
            An array of strings representing the enumeration values involved in
            the operation.
          items:
            type: string
      x-hubspot-sub-type-impl: true
    PublicAllPropertyTypesOperation:
      title: ALL_PROPERTY
      required:
        - includeObjectsWithNoValueSet
        - operationType
        - operator
      type: object
      properties:
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether objects with no value set for the
            property should be included in the operation. This property is
            required.
        operationType:
          type: string
          description: >-
            A string indicating the type of operation being performed. This
            property is required.
          default: ALL_PROPERTY
          enum:
            - ALL_PROPERTY
        operator:
          type: string
          description: >-
            A string representing the operator used in the filter operation.
            This property is required.
      x-hubspot-sub-type-impl: true
    PublicRangedNumberPropertyOperation:
      title: NUMBER_RANGED
      required:
        - includeObjectsWithNoValueSet
        - lowerBound
        - operationType
        - operator
        - upperBound
      type: object
      properties:
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether to include objects that have no value
            set for the property.
        lowerBound:
          type: integer
          description: An integer specifying the lower bound of the range.
          format: int64
        operationType:
          type: string
          description: >-
            A string indicating the type of operation, which is 'RANGED_NUMBER'
            by default.
          default: NUMBER_RANGED
          enum:
            - NUMBER_RANGED
        operator:
          type: string
          description: A string representing the operator used in the operation.
        upperBound:
          type: integer
          description: An integer specifying the upper bound of the range.
          format: int64
      x-hubspot-sub-type-impl: true
    PublicMultiStringPropertyOperation:
      title: MULTISTRING
      required:
        - includeObjectsWithNoValueSet
        - operationType
        - operator
        - values
      type: object
      properties:
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether objects with no value set should be
            included in the operation.
        operationType:
          type: string
          description: >-
            A string indicating the type of operation. The default value is
            'MULTI_STRING'.
          default: MULTISTRING
          enum:
            - MULTISTRING
        operator:
          type: string
          description: A string representing the operator used in the operation.
        values:
          type: array
          description: >-
            An array of strings representing the values involved in the
            operation.
          items:
            type: string
      x-hubspot-sub-type-impl: true
    PublicDatePropertyOperation:
      title: DATE
      required:
        - day
        - includeObjectsWithNoValueSet
        - month
        - operationType
        - operator
        - year
      type: object
      properties:
        day:
          type: integer
          description: An integer representing the day component of the date.
          format: int32
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether to include objects that do not have a
            value set for the date property.
        month:
          type: string
          description: An integer representing the month component of the date.
        operationType:
          type: string
          description: >-
            A string indicating the type of operation, specifically for date
            properties.
          default: DATE
          enum:
            - DATE
        operator:
          type: string
          description: A string representing the operator used in the date operation.
        year:
          type: integer
          description: An integer representing the year component of the date.
          format: int32
      x-hubspot-sub-type-impl: true
    PublicCalendarDatePropertyOperation:
      title: CALENDAR_DATE
      required:
        - includeObjectsWithNoValueSet
        - operationType
        - operator
        - timeUnit
      type: object
      properties:
        fiscalYearStart:
          type: string
          description: >-
            A string indicating the start of the fiscal year, used if the
            operation involves fiscal year calculations.
          enum:
            - APRIL
            - AUGUST
            - DECEMBER
            - FEBRUARY
            - JANUARY
            - JULY
            - JUNE
            - MARCH
            - MAY
            - NOVEMBER
            - OCTOBER
            - SEPTEMBER
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether to include objects that have no value
            set for the calendar date property.
        operationType:
          type: string
          description: >-
            A string indicating the type of operation. The default value is
            'CALENDAR_DATE'.
          default: CALENDAR_DATE
          enum:
            - CALENDAR_DATE
        operator:
          type: string
          description: A string representing the operator used in the operation.
        timeUnit:
          type: string
          description: >-
            A string representing the unit of time used in the operation, such
            as 'DAY', 'WEEK', 'MONTH', or 'YEAR'.
        timeUnitCount:
          type: integer
          description: >-
            An integer representing the count of the time units involved in the
            operation.
          format: int32
        useFiscalYear:
          type: boolean
          description: >-
            A boolean indicating whether to use the fiscal year in the
            operation.
      x-hubspot-sub-type-impl: true
    PublicComparativeStringPropertyOperation:
      title: COMPARATIVE_STRING
      required:
        - comparisonPropertyName
        - includeObjectsWithNoValueSet
        - operationType
        - operator
      type: object
      properties:
        comparisonPropertyName:
          type: string
          description: A string specifying the name of the property to be compared.
        defaultComparisonValue:
          type: string
          description: >-
            A string representing the default value to use in the comparison if
            the property value is not set.
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether to include objects that have no value
            set for the property being compared.
        operationType:
          type: string
          description: >-
            A string indicating the type of operation. Defaults to
            'COMPARATIVE_STRING'.
          default: COMPARATIVE_STRING
          enum:
            - COMPARATIVE_STRING
        operator:
          type: string
          description: A string representing the operator used in the comparison.
      x-hubspot-sub-type-impl: true
    PublicComparativeNumberPropertyOperation:
      title: COMPARATIVE_NUMBER
      required:
        - comparisonPropertyName
        - includeObjectsWithNoValueSet
        - operationType
        - operator
      type: object
      properties:
        comparisonPropertyName:
          type: string
        defaultComparisonValue:
          type: string
        includeObjectsWithNoValueSet:
          type: boolean
        operationType:
          type: string
          default: COMPARATIVE_NUMBER
          enum:
            - COMPARATIVE_NUMBER
        operator:
          type: string
      x-hubspot-sub-type-impl: true
    PublicEventFilterMetadata:
      required:
        - operation
        - property
      type: object
      properties:
        operation:
          description: >-
            Defines the operation to be applied to the property for filtering.
            It is a string value.
          oneOf:
            - $ref: '#/components/schemas/PublicBoolPropertyOperation'
            - $ref: '#/components/schemas/PublicNumberPropertyOperation'
            - $ref: '#/components/schemas/PublicStringPropertyOperation'
            - $ref: '#/components/schemas/PublicDateTimePropertyOperation'
            - $ref: '#/components/schemas/PublicRangedDatePropertyOperation'
            - $ref: '#/components/schemas/PublicComparativePropertyUpdatedOperation'
            - $ref: '#/components/schemas/PublicComparativeDatePropertyOperation'
            - $ref: '#/components/schemas/PublicRollingDateRangePropertyOperation'
            - $ref: '#/components/schemas/PublicRollingPropertyUpdatedOperation'
            - $ref: '#/components/schemas/PublicEnumerationPropertyOperation'
            - $ref: '#/components/schemas/PublicAllPropertyTypesOperation'
            - $ref: '#/components/schemas/PublicRangedNumberPropertyOperation'
            - $ref: '#/components/schemas/PublicMultiStringPropertyOperation'
            - $ref: '#/components/schemas/PublicDatePropertyOperation'
            - $ref: '#/components/schemas/PublicCalendarDatePropertyOperation'
            - $ref: '#/components/schemas/PublicTimePointOperation'
            - $ref: '#/components/schemas/PublicRangedTimeOperation'
            - $ref: '#/components/schemas/PublicComparativeStringPropertyOperation'
            - $ref: '#/components/schemas/PublicComparativeNumberPropertyOperation'
        property:
          type: string
          description: >-
            Represents the specific property of the event that the filter is
            targeting. It is a string value.
    PublicInListFilterMetadata:
      required:
        - id
        - inListType
      type: object
      properties:
        id:
          type: string
          description: A string representing the unique identifier for the filter metadata.
        inListType:
          type: string
          description: A string indicating the type of list that the filter applies to.
    PublicTimeOffset:
      required:
        - amount
        - offsetDirection
        - timeUnit
      type: object
      properties:
        amount:
          type: integer
          description: An integer specifying the amount of time units to offset.
          format: int64
        offsetDirection:
          type: string
          description: >-
            A string indicating the direction of the time offset. Valid values
            are 'BEFORE' and 'AFTER'.
        timeUnit:
          type: string
          description: >-
            A string representing the unit of time for the offset. Valid values
            include 'MINUTE', 'HOUR', 'DAY', 'WEEK', 'MONTH', 'QUARTER', and
            'YEAR'.
    PublicDatePoint:
      title: DATE
      required:
        - day
        - month
        - timeType
        - year
        - zoneId
      type: object
      properties:
        day:
          type: integer
          description: An integer representing the day component of the date.
          format: int32
        hour:
          type: integer
          description: An integer representing the hour component of the time.
          format: int32
        millisecond:
          type: integer
          description: An integer representing the millisecond component of the time.
          format: int32
        minute:
          type: integer
          description: An integer representing the minute component of the time.
          format: int32
        month:
          type: integer
          description: An integer representing the month component of the date.
          format: int32
        second:
          type: integer
          description: An integer representing the second component of the time.
          format: int32
        timeType:
          type: string
          description: >-
            A string indicating the type of time reference, typically set to
            'DATE'.
          default: DATE
          enum:
            - DATE
        timezoneSource:
          type: string
          description: A string representing the source of the timezone information.
        year:
          type: integer
          description: An integer representing the year component of the date.
          format: int32
        zoneId:
          type: string
          description: A string specifying the identifier for the timezone.
      x-hubspot-sub-type-impl: true
    PublicIndexedTimePoint:
      title: INDEXED
      required:
        - indexReference
        - timeType
        - zoneId
      type: object
      properties:
        indexReference:
          description: >-
            An object that defines the reference point for the indexed time,
            which can be one of several predefined references like 'now',
            'today', or a specific fiscal period.
          oneOf:
            - $ref: '#/components/schemas/PublicNowReference'
            - $ref: '#/components/schemas/PublicTodayReference'
            - $ref: '#/components/schemas/PublicWeekReference'
            - $ref: '#/components/schemas/PublicFiscalQuarterReference'
            - $ref: '#/components/schemas/PublicFiscalYearReference'
            - $ref: '#/components/schemas/PublicYearReference'
            - $ref: '#/components/schemas/PublicQuarterReference'
            - $ref: '#/components/schemas/PublicMonthReference'
        offset:
          $ref: '#/components/schemas/PublicIndexOffset'
        timeType:
          type: string
          description: >-
            A string indicating the type of time point, with a default value of
            'INDEXED'.
          default: INDEXED
          enum:
            - INDEXED
        timezoneSource:
          type: string
          description: A string representing the source of the timezone information.
        zoneId:
          type: string
          description: A string specifying the ID of the timezone.
      x-hubspot-sub-type-impl: true
    PublicPropertyReferencedTime:
      title: PROPERTY_REFERENCED
      required:
        - property
        - referenceType
        - timeType
        - zoneId
      type: object
      properties:
        property:
          type: string
          description: >-
            A string representing the property that is used to reference the
            time.
        referenceType:
          type: string
          description: >-
            A string indicating the type of reference, with a default value of
            'PROPERTY_REFERENCE'.
        timeType:
          type: string
          description: >-
            A string indicating the type of time reference. It defaults to
            'PROPERTY_REFERENCE'.
          default: PROPERTY_REFERENCED
          enum:
            - PROPERTY_REFERENCED
        timezoneSource:
          type: string
          description: A string representing the source of the timezone information.
        zoneId:
          type: string
          description: A string specifying the ID of the timezone.
      x-hubspot-sub-type-impl: true
    PublicNowReference:
      title: NOW
      required:
        - referenceType
      type: object
      properties:
        hour:
          type: integer
          description: An integer representing the hour part of the current time.
          format: int32
        millisecond:
          type: integer
          description: An integer representing the millisecond part of the current time.
          format: int32
        minute:
          type: integer
          description: An integer representing the minute part of the current time.
          format: int32
        referenceType:
          type: string
          description: >-
            A string that indicates the type of reference. The default value is
            'NOW', and it is used to specify that the reference is to the
            current time.
          default: NOW
          enum:
            - NOW
        second:
          type: integer
          description: An integer representing the second part of the current time.
          format: int32
      x-hubspot-sub-type-impl: true
    PublicTodayReference:
      title: TODAY
      required:
        - referenceType
      type: object
      properties:
        hour:
          type: integer
          description: An integer representing the hour of the day.
          format: int32
        millisecond:
          type: integer
          description: An integer representing the millisecond within the second.
          format: int32
        minute:
          type: integer
          description: An integer representing the minute within the hour.
          format: int32
        referenceType:
          type: string
          description: >-
            A string indicating the type of reference, which is 'TODAY' by
            default.
          default: TODAY
          enum:
            - TODAY
        second:
          type: integer
          description: An integer representing the second within the minute.
          format: int32
      x-hubspot-sub-type-impl: true
    PublicWeekReference:
      title: WEEK
      required:
        - dayOfWeek
        - referenceType
      type: object
      properties:
        dayOfWeek:
          type: string
          description: An integer representing the day of the week.
          enum:
            - FRIDAY
            - MONDAY
            - SATURDAY
            - SUNDAY
            - THURSDAY
            - TUESDAY
            - WEDNESDAY
        hour:
          type: integer
          description: An integer representing the hour of the day.
          format: int32
        millisecond:
          type: integer
          description: An integer representing the millisecond of the second.
          format: int32
        minute:
          type: integer
          description: An integer representing the minute of the hour.
          format: int32
        referenceType:
          type: string
          description: >-
            A string indicating the type of reference, which is 'WEEK' for this
            component.
          default: WEEK
          enum:
            - WEEK
        second:
          type: integer
          description: An integer representing the second of the minute.
          format: int32
      x-hubspot-sub-type-impl: true
    PublicFiscalQuarterReference:
      title: FISCAL_QUARTER
      required:
        - day
        - month
        - referenceType
      type: object
      properties:
        day:
          type: integer
          description: An integer representing the day of the month.
          format: int32
        hour:
          type: integer
          description: An integer representing the hour of the day.
          format: int32
        millisecond:
          type: integer
          description: An integer representing the millisecond within the second.
          format: int32
        minute:
          type: integer
          description: An integer representing the minute within the hour.
          format: int32
        month:
          type: integer
          description: An integer representing the month of the year.
          format: int32
        referenceType:
          type: string
          description: >-
            A string indicating the type of reference, which is
            'FISCAL_QUARTER'.
          default: FISCAL_QUARTER
          enum:
            - FISCAL_QUARTER
        second:
          type: integer
          description: An integer representing the second within the minute.
          format: int32
      x-hubspot-sub-type-impl: true
    PublicFiscalYearReference:
      title: FISCAL_YEAR
      required:
        - day
        - month
        - referenceType
      type: object
      properties:
        day:
          type: integer
          description: An integer representing the day of the month.
          format: int32
        hour:
          type: integer
          description: An integer representing the hour of the day.
          format: int32
        millisecond:
          type: integer
          description: An integer representing the millisecond within the second.
          format: int32
        minute:
          type: integer
          description: An integer representing the minute within the hour.
          format: int32
        month:
          type: integer
          description: An integer representing the month of the fiscal year.
          format: int32
        referenceType:
          type: string
          description: >-
            A string that indicates the type of reference, which is
            'FISCAL_YEAR'.
          default: FISCAL_YEAR
          enum:
            - FISCAL_YEAR
        second:
          type: integer
          description: An integer representing the second within the minute.
          format: int32
      x-hubspot-sub-type-impl: true
    PublicYearReference:
      title: YEAR
      required:
        - day
        - month
        - referenceType
      type: object
      properties:
        day:
          type: integer
          description: An integer representing the day of the month.
          format: int32
        hour:
          type: integer
          description: An integer representing the hour of the day.
          format: int32
        millisecond:
          type: integer
          description: An integer representing the millisecond within the second.
          format: int32
        minute:
          type: integer
          description: An integer representing the minute within the hour.
          format: int32
        month:
          type: integer
          description: An integer representing the month of the year.
          format: int32
        referenceType:
          type: string
          description: >-
            A string that specifies the type of reference, which is 'YEAR' by
            default.
          default: YEAR
          enum:
            - YEAR
        second:
          type: integer
          description: An integer representing the second within the minute.
          format: int32
      x-hubspot-sub-type-impl: true
    PublicQuarterReference:
      title: QUARTER
      required:
        - day
        - month
        - referenceType
      type: object
      properties:
        day:
          type: integer
          description: An integer representing the day of the month.
          format: int32
        hour:
          type: integer
          description: An integer representing the hour of the day.
          format: int32
        millisecond:
          type: integer
          description: An integer representing the millisecond within the second.
          format: int32
        minute:
          type: integer
          description: An integer representing the minute within the hour.
          format: int32
        month:
          type: integer
          description: An integer representing the month of the year.
          format: int32
        referenceType:
          type: string
          description: >-
            A string indicating the type of reference, which is 'QUARTER' for
            this component.
          default: QUARTER
          enum:
            - QUARTER
        second:
          type: integer
          description: An integer representing the second within the minute.
          format: int32
      x-hubspot-sub-type-impl: true
    PublicMonthReference:
      title: MONTH
      required:
        - day
        - referenceType
      type: object
      properties:
        day:
          type: integer
          description: An integer representing the day of the month.
          format: int32
        hour:
          type: integer
          description: An integer representing the hour of the day.
          format: int32
        millisecond:
          type: integer
          description: An integer representing the millisecond within the second.
          format: int32
        minute:
          type: integer
          description: An integer representing the minute within the hour.
          format: int32
        referenceType:
          type: string
          description: >-
            A string indicating the type of reference, with a default value of
            'MONTH'.
          default: MONTH
          enum:
            - MONTH
        second:
          type: integer
          description: An integer representing the second within the minute.
          format: int32
      x-hubspot-sub-type-impl: true
    PublicIndexOffset:
      type: object
      properties:
        days:
          type: integer
          description: An integer representing the number of days to offset.
          format: int32
        hours:
          type: integer
          description: An integer representing the number of hours to offset.
          format: int32
        milliseconds:
          type: integer
          description: An integer representing the number of milliseconds to offset.
          format: int32
        minutes:
          type: integer
          description: An integer representing the number of minutes to offset.
          format: int32
        months:
          type: integer
          description: An integer representing the number of months to offset.
          format: int32
        quarters:
          type: integer
          description: An integer representing the number of quarters to offset.
          format: int32
        seconds:
          type: integer
          description: An integer representing the number of seconds to offset.
          format: int32
        weeks:
          type: integer
          description: An integer representing the number of weeks to offset.
          format: int32
        years:
          type: integer
          description: An integer representing the number of years to offset.
          format: int32
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