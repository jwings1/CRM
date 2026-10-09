> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

---
id: 255ab3ca-f5f7-41d0-bedb-1b0050255184
---

# Update rules (Partial)

> Update the rules for a specific pipeline within a given object type in HubSpot. This operation allows you to modify governance validation rules and approval stages for the specified pipeline. It is useful for maintaining or altering the workflow rules associated with your pipelines.

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

````yaml specs/2026-09/crm-pipeline-governance-v2026-09.json PATCH /crm/pipelines-rules/2026-09/{objectTypeId}/{pipelineId}
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
  /crm/pipelines-rules/2026-09/{objectTypeId}/{pipelineId}:
    patch:
      tags:
        - Basic
      summary: Update rules (Partial)
      description: >-
        Update the rules for a specific pipeline within a given object type in
        HubSpot. This operation allows you to modify governance validation rules
        and approval stages for the specified pipeline. It is useful for
        maintaining or altering the workflow rules associated with your
        pipelines.
      operationId: patch-/crm/pipelines-rules/2026-09/{objectTypeId}/{pipelineId}
      parameters:
        - name: objectTypeId
          in: path
          description: >-
            The unique identifier of the object type for which the pipeline
            rules are being updated.
          required: true
          style: simple
          explode: false
          schema:
            type: string
        - name: pipelineId
          in: path
          description: The unique identifier of the pipeline whose rules are being updated.
          required: true
          style: simple
          explode: false
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PublicPipelineRulesPatchRequest'
        required: true
      responses:
        '200':
          description: successful operation
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PublicPipelineRules'
        default:
          $ref: '#/components/responses/Error'
          description: ''
      security:
        - oauth2:
            - crm.pipelines.governance.write
components:
  schemas:
    PublicPipelineRulesPatchRequest:
      type: object
      properties:
        approvalStage:
          type: object
          properties: {}
          description: >-
            A rule that defines the approval process for a specific pipeline
            stage. It is defined using the PublicApprovalStageRuleRequest
            schema.
        noBackwardsMovementRule:
          type: object
          properties: {}
          description: >-
            A rule that prevents moving backwards in the pipeline stages. It is
            defined using the PublicSequenceValidationRule schema.
        noSkippingStagesRule:
          type: object
          properties: {}
          description: >-
            A rule that prevents skipping stages in the pipeline. It is defined
            using the PublicSequenceValidationRule schema.
        objectCreationRule:
          type: object
          properties: {}
          description: >-
            A rule that specifies conditions for object creation within the
            pipeline. It is defined using the PublicObjectCreationRule schema.
    PublicPipelineRules:
      required:
        - createdAt
        - governanceValidationRules
        - id
        - objectTypeId
        - pipelineId
        - updatedAt
      type: object
      properties:
        approvalStage:
          $ref: '#/components/schemas/PublicApprovalStageRule'
        createdAt:
          type: string
          description: The date and time when the pipeline rule was created.
          format: date-time
        governanceValidationRules:
          $ref: '#/components/schemas/PublicGovernanceValidationRules'
        id:
          type: string
          description: The unique identifier for the pipeline rule.
        objectTypeId:
          type: string
          description: >-
            The identifier for the type of object the pipeline rule is
            associated with.
        pipelineId:
          type: string
          description: The unique identifier for the pipeline to which the rule applies.
        updatedAt:
          type: string
          description: The date and time when the pipeline rule was last updated.
          format: date-time
    PublicApprovalStageRule:
      required:
        - approvalMode
        - approverUserIds
        - pipelineStageId
      type: object
      properties:
        approvalComment:
          type: string
          description: >-
            A string that allows for an optional comment or note regarding the
            approval process.
        approvalMode:
          type: string
          description: >-
            Specifies the mode of approval required. It can be either 'ALL',
            meaning all approvers must approve, or 'ANY', meaning any one
            approver can approve. It is a string.
          enum:
            - ALL
            - ANY
        approverUserIds:
          type: array
          description: >-
            An array of user IDs representing the users who are designated as
            approvers for this stage. Each user ID is a string.
          items:
            type: string
        conditionalApprovalFilterBranch:
          description: >-
            Defines the conditions under which the approval is required. It can
            be one of several filter branch types, such as PublicOrFilterBranch
            or PublicAndFilterBranch, which determine the logical conditions for
            approval.
          oneOf:
            - $ref: '#/components/schemas/PublicOrFilterBranch'
            - $ref: '#/components/schemas/PublicAndFilterBranch'
            - $ref: '#/components/schemas/PublicNotAllFilterBranch'
            - $ref: '#/components/schemas/PublicNotAnyFilterBranch'
            - $ref: '#/components/schemas/PublicRestrictedFilterBranch'
            - $ref: '#/components/schemas/PublicUnifiedEventsFilterBranch'
            - $ref: '#/components/schemas/PublicAssociationFilterBranch'
        pipelineStageId:
          type: string
          description: >-
            The unique identifier for the pipeline stage that this approval rule
            applies to. It is a string.
    PublicGovernanceValidationRules:
      required:
        - noBackwardsMovementRule
        - noSkippingStagesRule
        - objectCreationRule
      type: object
      properties:
        noBackwardsMovementRule:
          $ref: '#/components/schemas/PublicSequenceValidationRule'
        noSkippingStagesRule:
          $ref: '#/components/schemas/PublicSequenceValidationRule'
        objectCreationRule:
          $ref: '#/components/schemas/PublicObjectCreationRule'
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
          description: A string representing the operator used in the filter branch.
        filterBranchType:
          type: string
          description: >-
            A string that specifies the type of filter branch, which is 'OR' by
            default.
          default: OR
          enum:
            - OR
        filterBranches:
          type: array
          description: >-
            An array of filter branches that can include various types of filter
            branches such as 'OR', 'AND', 'NOT_ALL', 'NOT_ANY', 'RESTRICTED',
            'UNIFIED_EVENTS', or 'ASSOCIATION'.
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
            An array of filters that can include different types of filters such
            as 'PublicPropertyFilter', 'PublicAssociationInListFilter',
            'PublicPageViewAnalyticsFilter', and others.
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
          description: >-
            A string representing the logical operator used in the filter
            branch.
        filterBranchType:
          type: string
          description: A string indicating the type of filter branch. Defaults to 'AND'.
          default: AND
          enum:
            - AND
        filterBranches:
          type: array
          description: >-
            An array of nested filter branches, which can include 'OR', 'AND',
            'NOT_ALL', 'NOT_ANY', 'RESTRICTED', 'UNIFIED_EVENTS', and
            'ASSOCIATION' filter branches.
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
            An array of filters that are applied within this branch. These can
            include various types of filters such as property filters, event
            filters, and subscription filters.
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
          description: >-
            A string representing the operator used to combine the filter
            branches.
        filterBranchType:
          type: string
          description: >-
            A string indicating the type of filter branch, which is 'NOT_ALL'
            for this component.
          default: NOT_ALL
          enum:
            - NOT_ALL
        filterBranches:
          type: array
          description: >-
            An array of filter branches that can include various types of filter
            branches such as 'OR', 'AND', 'NOT_ALL', etc.
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
            An array of filters that can include various types of filters such
            as property filters, association filters, and more.
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
          description: >-
            A string representing the logical operator used within the filter
            branch.
        filterBranchType:
          type: string
          description: >-
            A string indicating the type of filter branch, which is 'NOT_ANY'
            for this component.
          default: NOT_ANY
          enum:
            - NOT_ANY
        filterBranches:
          type: array
          description: >-
            An array of nested filter branches, each of which can be of various
            types including 'OR', 'AND', 'NOT_ALL', 'NOT_ANY', 'RESTRICTED',
            'UNIFIED_EVENTS', and 'ASSOCIATION'.
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
            An array of filters that can include different types such as
            property filters, association filters, and various analytics
            filters.
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
            A string indicating the type of the filter branch. Defaults to
            'RESTRICTED'.
          default: RESTRICTED
          enum:
            - RESTRICTED
        filterBranches:
          type: array
          description: >-
            An array of nested filter branches. Each item can be one of several
            types, including 'PublicOrFilterBranch', 'PublicAndFilterBranch',
            'PublicNotAllFilterBranch', 'PublicNotAnyFilterBranch',
            'PublicRestrictedFilterBranch', 'PublicUnifiedEventsFilterBranch',
            or 'PublicAssociationFilterBranch'.
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
            An array of filters applied within this branch. Each filter can be
            one of several types, such as 'PublicPropertyFilter',
            'PublicAssociationInListFilter', 'PublicPageViewAnalyticsFilter',
            'PublicCtaAnalyticsFilter', 'PublicEventAnalyticsFilter',
            'PublicFormSubmissionFilter', 'PublicFormSubmissionOnPageFilter',
            'PublicIntegrationEventFilter', 'PublicEmailSubscriptionFilter',
            'PublicCommunicationSubscriptionFilter', 'PublicSurveyMonkeyFilter',
            'PublicSurveyMonkeyValueFilter', 'PublicWebinarFilter',
            'PublicEmailEventFilter', 'PublicPrivacyAnalyticsFilter',
            'PublicAdsSearchFilter', 'PublicAdsTimeFilter',
            'PublicInListFilter', 'PublicUnifiedEventsFilter', or
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
            An optional refinement criterion that allows for additional
            filtering based on coalescing logic. This can be one of several
            predefined refinement schemas.
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
            A string representing the unique identifier for the event type that
            this filter branch is targeting.
        filterBranchOperator:
          type: string
          description: >-
            A string that specifies the operator used to combine multiple filter
            branches within this component.
        filterBranchType:
          type: string
          description: >-
            A string indicating the type of filter branch, which is
            'UNIFIED_EVENTS' for this component.
          default: UNIFIED_EVENTS
          enum:
            - UNIFIED_EVENTS
        filterBranches:
          type: array
          description: >-
            An array of nested filter branches, each of which can be a complex
            filter structure involving various logical operators.
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
            An array of filters that apply specific conditions to the unified
            events. Each filter can be one of several types, such as property
            filters or event analytics filters.
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
            A string that specifies the logical operator for the filter branch,
            with valid values including 'HAS_COMPLETED' and 'HAS_NOT_COMPLETED'.
          enum:
            - HAS_COMPLETED
            - HAS_NOT_COMPLETED
        pruningRefineBy:
          description: >-
            An optional refinement criterion that allows for additional
            filtering based on pruning logic. This can be one of several
            predefined refinement schemas.
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
          description: A string indicating the category of the association.
        associationTypeId:
          type: integer
          description: An integer representing the ID of the association type.
          format: int32
        filterBranchOperator:
          type: string
          description: >-
            A string representing the operator used to combine the filter
            branches.
        filterBranchType:
          type: string
          description: >-
            A string indicating the type of filter branch, which is
            'ASSOCIATION' by default.
          default: ASSOCIATION
          enum:
            - ASSOCIATION
        filterBranches:
          type: array
          description: >-
            An array of filter branches that can include various types of
            branches such as OR, AND, NOT_ALL, NOT_ANY, RESTRICTED,
            UNIFIED_EVENTS, and ASSOCIATION.
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
            An array of filters that can include different types of filters such
            as property filters, association filters, and various analytics
            filters.
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
            A string representing the ID of the object type involved in the
            association.
        operator:
          type: string
          description: A string representing the operator used in the filter branch.
      x-hubspot-sub-type-impl: true
    PublicSequenceValidationRule:
      required:
        - enabledForAllStages
        - pipelineStageIds
      type: object
      properties:
        enabledForAllStages:
          type: boolean
          description: >-
            A boolean indicating whether the validation rule is enabled for all
            stages in the pipeline.
        pipelineStageIds:
          type: array
          description: >-
            An array of strings representing the specific pipeline stage IDs for
            which the validation rule is applicable.
          items:
            type: string
    PublicObjectCreationRule:
      required:
        - pipelineStageIds
      type: object
      properties:
        pipelineStageIds:
          type: array
          description: >-
            An array of strings representing the IDs of pipeline stages where
            objects can be created.
          items:
            type: string
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
            A string indicating the type of filter. The default value is
            'PROPERTY'.
          default: PROPERTY
          enum:
            - PROPERTY
        operation:
          description: >-
            Defines the operation to be performed on the property. This can be
            one of several operation types, such as boolean, number, string,
            date, and more, each with its own specific behavior.
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
          description: A string representing the name of the property to be filtered.
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
          description: A string that specifies the category of the association.
        associationTypeId:
          type: integer
          description: An integer that identifies the type of association.
          format: int32
        coalescingRefineBy:
          description: >-
            An object that defines the criteria for refining the filter. It can
            be one of several types, such as PublicNumOccurrencesRefineBy or
            PublicTimePointOperation.
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
            A string that specifies the type of filter. The default value is
            'ASSOCIATION'.
          default: ASSOCIATION
          enum:
            - ASSOCIATION
        listId:
          type: string
          description: A string that identifies the list to which the filter is applied.
        operator:
          type: string
          description: A string that represents the operator used in the filter.
        toObjectType:
          type: string
          description: >-
            A string that specifies the type of the object to which the
            association is made.
        toObjectTypeId:
          type: string
          description: >-
            A string that specifies the type ID of the object to which the
            association is made.
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
            An optional refinement criterion that can be one of several
            predefined schemas, used to further refine the filter results.
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
          description: A boolean indicating whether tracking is enabled for this filter.
        filterType:
          type: string
          description: >-
            A string representing the type of filter. Default value is
            'PAGE_VIEW'.
          default: PAGE_VIEW
          enum:
            - PAGE_VIEW
        operator:
          type: string
          description: A string representing the operator used in the filter.
        pageUrl:
          type: string
          description: A string representing the URL of the page to be filtered.
        pruningRefineBy:
          description: >-
            An optional refinement criterion that can be one of several
            predefined schemas, used to prune the filter results.
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
            including occurrences and timestamp comparisons.
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
          description: A string representing the name of the Call-To-Action being filtered.
        filterType:
          type: string
          description: A string that specifies the type of filter, defaulting to 'CTA'.
          default: CTA
          enum:
            - CTA
        operator:
          type: string
          description: A string that defines the operation to be applied in the filter.
        pruningRefineBy:
          description: >-
            An optional refinement criterion used to narrow down data, similar
            to coalescingRefineBy, with options like occurrences and timestamp
            comparisons.
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
            An optional refinement criterion that can be one of several types,
            such as occurrences or timestamp comparisons, to further refine the
            filter results.
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
          description: A string that uniquely identifies the event to be filtered.
        filterType:
          type: string
          description: >-
            A string indicating the type of filter, which is always 'EVENT' for
            this component.
          default: EVENT
          enum:
            - EVENT
        operator:
          type: string
          description: >-
            A string representing the operation or condition applied in the
            filter.
        pruningRefineBy:
          description: >-
            An optional refinement criterion similar to coalescingRefineBy, used
            to prune the filter results based on specific conditions.
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
            An object used to refine the filter by coalescing criteria. It can
            be one of several types, such as occurrences or timestamp-based
            refinements.
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
            A string that specifies the type of filter. The default value is
            'FORM_SUBMISSION'.
          default: FORM_SUBMISSION
          enum:
            - FORM_SUBMISSION
        formId:
          type: string
          description: A string representing the unique identifier of the form.
        operator:
          type: string
          description: >-
            A string that specifies the operation to apply, with valid values
            being 'FILLED_OUT' or 'NOT_FILLED_OUT'.
          enum:
            - FILLED_OUT
            - NOT_FILLED_OUT
        pruningRefineBy:
          description: >-
            An object used to refine the filter by pruning criteria. It can be
            one of several types, such as occurrences or timestamp-based
            refinements.
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
            Criteria used to refine the filter by coalescing, which can include
            various timestamp operations.
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
            The type of filter being applied. Defaults to
            'FORM_SUBMISSION_ON_PAGE'.
          default: FORM_SUBMISSION_ON_PAGE
          enum:
            - FORM_SUBMISSION_ON_PAGE
        formId:
          type: string
          description: The unique identifier of the form being filtered.
        operator:
          type: string
          description: >-
            The operation to apply, which can be either 'FILLED_OUT' or
            'NOT_FILLED_OUT'.
          enum:
            - FILLED_OUT
            - NOT_FILLED_OUT
        pageId:
          type: string
          description: >-
            The unique identifier of the page where the form submission is being
            filtered.
        pruningRefineBy:
          description: >-
            Criteria used to refine the filter by pruning, which can include
            various timestamp operations.
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
            This property is used to specify which event type the filter applies
            to.
          format: int32
        filterLines:
          type: array
          description: >-
            An array of filter lines that contain the metadata for the event
            filter. Each item in the array is a detailed specification of the
            criteria used to filter events.
          items:
            $ref: '#/components/schemas/PublicEventFilterMetadata'
        filterType:
          type: string
          description: >-
            A string representing the type of filter. It is a required field and
            typically has a default value specific to the filter type.
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
            A string indicating the type of filter, which is
            'EMAIL_SUBSCRIPTION' for this component.
          default: EMAIL_SUBSCRIPTION
          enum:
            - EMAIL_SUBSCRIPTION
        subscriptionIds:
          type: array
          description: >-
            An array of strings representing the IDs of the subscriptions to be
            filtered.
          items:
            type: string
        subscriptionType:
          type: string
          description: A string representing the type of subscription.
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
            An array of strings representing the accepted opt-in states for the
            subscription.
          items:
            type: string
        businessUnitId:
          type: string
          description: >-
            A string representing the ID of the business unit associated with
            the subscription.
        channel:
          type: string
          description: >-
            A string indicating the communication channel associated with the
            subscription.
        filterType:
          type: string
          description: >-
            A string that indicates the type of filter. The default value is
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
          description: A string indicating the type of subscription.
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
            A string that specifies the type of filter being used. The default
            value is 'SURVEY_MONKEY', indicating that this filter is for
            SurveyMonkey data.
          default: SURVEY_MONKEY
          enum:
            - SURVEY_MONKEY
        operator:
          type: string
          description: >-
            A string that defines the operation or condition to apply when
            filtering the survey data.
        surveyId:
          type: string
          description: >-
            A string representing the unique identifier of the SurveyMonkey
            survey to be filtered.
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
            A string indicating the type of filter. Defaults to
            'SURVEY_MONKEY_VALUE'.
          default: SURVEY_MONKEY_VALUE
          enum:
            - SURVEY_MONKEY_VALUE
        operator:
          type: string
          description: >-
            A string that specifies the operator used in the filter, determining
            how the survey data is evaluated against the filter criteria.
        surveyAnswerColId:
          type: string
          description: >-
            A string representing the column identifier of the survey answer,
            used for filtering specific responses.
        surveyAnswerRowId:
          type: string
          description: >-
            A string representing the row identifier of the survey answer, used
            for filtering specific responses.
        surveyId:
          type: string
          description: >-
            A string representing the unique identifier of the SurveyMonkey
            survey.
        surveyQuestion:
          type: string
          description: >-
            A string specifying the question within the survey to filter
            responses by.
        valueComparison:
          description: >-
            An object that defines the operation for comparing survey answer
            values. It can be one of several types, such as number, string, or
            date operations.
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
            A string that specifies the type of filter. The default value is
            'WEBINAR'.
          default: WEBINAR
          enum:
            - WEBINAR
        operator:
          type: string
          description: A string representing the operator used in the filter.
        webinarId:
          type: string
          description: A string that uniquely identifies the webinar to be filtered.
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
            A string that identifies the application associated with the email
            event.
        clickUrl:
          type: string
          description: A string representing the URL that was clicked in the email event.
        emailId:
          type: string
          description: >-
            A string that uniquely identifies the email associated with the
            event.
        filterType:
          type: string
          description: >-
            A string that specifies the type of filter. The default value is
            'EMAIL_EVENT'.
          default: EMAIL_EVENT
          enum:
            - EMAIL_EVENT
        level:
          type: string
          description: A string representing the level of the email event.
        operator:
          type: string
          description: >-
            A string that defines the operation or event type for filtering.
            Valid values include 'LINK_CLICKED', 'MARKED_SPAM', 'OPENED',
            'OPENED_BUT_LINK_NOT_CLICKED', 'OPENED_BUT_NOT_REPLIED', 'REPLIED',
            'UNSUBSCRIBED', 'BOUNCED', 'RECEIVED', 'RECEIVED_BUT_NOT_OPENED',
            'SENT', 'SENT_BUT_LINK_NOT_CLICKED', and 'SENT_BUT_NOT_RECEIVED'.
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
            An object that specifies additional criteria for refining the
            filter, which can be one of several types such as
            'PublicNumOccurrencesRefineBy', 'PublicSetOccurrencesRefineBy',
            'PublicRelativeComparativeTimestampRefineBy',
            'PublicRelativeRangedTimestampRefineBy',
            'PublicAbsoluteComparativeTimestampRefineBy',
            'PublicAbsoluteRangedTimestampRefineBy', 'PublicAllHistoryRefineBy',
            'PublicTimePointOperation', or 'PublicRangedTimeOperation'.
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
            A string indicating the type of filter, which is 'PRIVACY' for this
            component.
          default: PRIVACY
          enum:
            - PRIVACY
        operator:
          type: string
          description: >-
            A string specifying the operator to be used in conjunction with the
            privacyName for filtering.
        privacyName:
          type: string
          description: >-
            A string representing the name of the privacy setting to be used in
            the filter.
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
          description: A string identifying the ad network where the search is performed.
        entityType:
          type: string
          description: A string representing the type of entity being filtered.
        filterType:
          type: string
          description: >-
            A string indicating the type of filter being applied. Default value
            is 'ADS_SEARCH'.
          default: ADS_SEARCH
          enum:
            - ADS_SEARCH
        operator:
          type: string
          description: >-
            A string that specifies the operation or condition applied to the
            filter.
        searchTermType:
          type: string
          description: A string specifying the type of search term used in the filter.
        searchTerms:
          type: array
          description: >-
            An array of strings containing the terms used to search within the
            ad network.
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
            A string that indicates the type of filter being applied. The
            default value is 'ADS_TIME'.
          default: ADS_TIME
          enum:
            - ADS_TIME
        pruningRefineBy:
          description: >-
            An object that defines the criteria for refining the filter based on
            time attributes. It can be one of several types, such as
            PublicNumOccurrencesRefineBy, PublicSetOccurrencesRefineBy, or
            various timestamp refine types.
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
          description: >-
            A string that specifies the type of filter being applied. The
            default value is 'IN_LIST'.
          default: IN_LIST
          enum:
            - IN_LIST
        listId:
          type: string
          description: >-
            A string representing the unique identifier of the list to be used
            in the filter.
        metadata:
          $ref: '#/components/schemas/PublicInListFilterMetadata'
        operator:
          type: string
          description: A string that defines the operator used in the filter.
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
            An object that specifies refinement criteria for coalescing events.
            It can be one of several predefined schemas such as
            PublicNumOccurrencesRefineBy or PublicTimePointOperation.
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
          description: A string representing the unique identifier for the event type.
        filterLines:
          type: array
          description: >-
            An array of objects, each conforming to the
            PublicEventFilterMetadata schema, representing the individual filter
            lines that make up the unified events filter.
          items:
            $ref: '#/components/schemas/PublicEventFilterMetadata'
        filterType:
          type: string
          description: >-
            A string indicating the type of filter. The default value is
            'UNIFIED_EVENTS'.
          default: UNIFIED_EVENTS
          enum:
            - UNIFIED_EVENTS
        pruningRefineBy:
          description: >-
            An object that specifies refinement criteria for pruning events. It
            can be one of several predefined schemas such as
            PublicNumOccurrencesRefineBy or PublicTimePointOperation.
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
            A string indicating the type of filter. It defaults to 'CONSTANT'
            and must be one of the predefined filter types.
          default: CONSTANT
          enum:
            - CONSTANT
        shouldAccept:
          type: boolean
          description: >-
            A boolean indicating whether the filter should accept the criteria
            it evaluates.
        source:
          type: string
          description: >-
            A string representing the origin or context from which the filter is
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
            'NUM_OCCURRENCES'.
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
          description: A string that specifies the set type for the occurrences refinement.
        type:
          type: string
          description: >-
            A string representing the type of refinement. The default value is
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
          description: A string representing the comparison operation to be performed.
        timeOffset:
          $ref: '#/components/schemas/PublicTimeOffset'
        type:
          type: string
          description: >-
            A string indicating the type of refinement, which is
            'RELATIVE_COMPARATIVE'.
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
          description: >-
            A string indicating the type of range being used for the timestamp
            refinement.
        type:
          type: string
          description: >-
            A string that specifies the type of the refine by operation, which
            is 'RELATIVE_RANGED'.
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
            A string representing the type of comparison to be made with the
            timestamp.
        timestamp:
          type: integer
          description: >-
            An integer representing the specific point in time to be used for
            the comparison, formatted as a Unix timestamp in milliseconds.
          format: int64
        type:
          type: string
          description: >-
            A string indicating the type of refinement, which is
            'ABSOLUTE_COMPARATIVE'.
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
            An integer representing the lower bound of the timestamp range,
            specified as a Unix timestamp in milliseconds.
          format: int64
        rangeType:
          type: string
          description: A string representing the type of range being defined.
        type:
          type: string
          description: >-
            A string that specifies the type of refine by operation. The default
            value is 'ABSOLUTE_RANGED'.
          default: ABSOLUTE_RANGED
          enum:
            - ABSOLUTE_RANGED
        upperTimestamp:
          type: integer
          description: >-
            An integer representing the upper bound of the timestamp range,
            specified as a Unix timestamp in milliseconds.
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
            A string representing the type of refinement. The default and only
            valid value is 'ALL_HISTORY'.
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
            A boolean indicating whether to include objects with no value set in
            the operation.
        operationType:
          type: string
          description: >-
            A string indicating the type of operation, defaulting to
            'TIME_POINT'.
          default: TIME_POINT
          enum:
            - TIME_POINT
        operator:
          type: string
          description: A string representing the operator used in the time point operation.
        propertyParser:
          type: string
          description: >-
            A string specifying the parser used for the property in the
            operation.
        timePoint:
          description: >-
            Defines the specific time point for the operation. It can be one of
            several types, including PublicDatePoint, PublicIndexedTimePoint, or
            PublicPropertyReferencedTime.
          oneOf:
            - $ref: '#/components/schemas/PublicDatePoint'
            - $ref: '#/components/schemas/PublicIndexedTimePoint'
            - $ref: '#/components/schemas/PublicPropertyReferencedTime'
        type:
          type: string
          description: A string representing the type of the time point operation.
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
            A boolean indicating whether to include objects that have no value
            set.
        lowerBoundEndpointBehavior:
          type: string
          description: >-
            A string that specifies the behavior of the lower bound endpoint in
            the time range.
        lowerBoundTimePoint:
          description: >-
            An object that defines the lower bound time point of the range. It
            can be a date point, indexed time point, or property-referenced
            time.
          oneOf:
            - $ref: '#/components/schemas/PublicDatePoint'
            - $ref: '#/components/schemas/PublicIndexedTimePoint'
            - $ref: '#/components/schemas/PublicPropertyReferencedTime'
        operationType:
          type: string
          description: A string that specifies the type of operation being performed.
        operator:
          type: string
          description: A string that defines the operator used in the time operation.
        propertyParser:
          type: string
          description: A string that indicates the property parser used in the operation.
        type:
          type: string
          description: >-
            A string that specifies the type of operation, with a default value
            of 'TIME_RANGED'.
          default: TIME_RANGED
          enum:
            - TIME_RANGED
        upperBoundEndpointBehavior:
          type: string
          description: >-
            A string that specifies the behavior of the upper bound endpoint in
            the time range.
        upperBoundTimePoint:
          description: >-
            An object that defines the upper bound time point of the range. It
            can be a date point, indexed time point, or property-referenced
            time.
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
            A string representing the type of operation. The default value is
            'BOOLEAN'.
          default: BOOL
          enum:
            - BOOL
        operator:
          type: string
          description: A string indicating the operator used in the boolean operation.
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
            A boolean indicating whether objects with no value set should be
            included in the operation.
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
          description: A number representing the value used in the operation.
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
            A boolean indicating whether objects without a value set for the
            property should be included in the operation.
        operationType:
          type: string
          description: >-
            A string indicating the type of operation, which is always 'STRING'
            for this component.
          default: STRING
          enum:
            - STRING
        operator:
          type: string
          description: >-
            A string representing the operator to be used in the operation. The
            specific operators are not detailed in the spec.
        value:
          type: string
          description: A string representing the value to be used in the operation.
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
            A boolean indicating whether objects without a set value should be
            included in the operation.
        operationType:
          type: string
          description: >-
            A string indicating the type of operation, which is always
            'DATETIME' for this component.
          default: DATETIME
          enum:
            - DATETIME
        operator:
          type: string
          description: A string representing the operator used in the datetime operation.
        requiresTimeZoneConversion:
          type: boolean
          description: >-
            A boolean specifying whether the datetime operation requires
            conversion based on time zones.
        timestamp:
          type: integer
          description: >-
            An integer representing the timestamp involved in the operation,
            formatted as an int64.
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
            A boolean indicating whether objects with no value set should be
            included.
        lowerBound:
          type: integer
          description: >-
            An integer representing the lower bound of the date range, in int64
            format.
          format: int64
        operationType:
          type: string
          description: >-
            A string that specifies the type of operation, with a default value
            of 'RANGED_DATE'.
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
            An integer representing the upper bound of the date range, in int64
            format.
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
          description: A string representing the name of the property to compare against.
        defaultComparisonValue:
          type: string
          description: >-
            An optional value used as a default for comparison if the comparison
            property is not set.
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether objects without a value set for the
            property should be included in the operation.
        operationType:
          type: string
          description: >-
            A string that specifies the type of operation. The default value is
            'COMPARATIVE_PROPERTY_UPDATED'.
          default: COMPARATIVE_PROPERTY_UPDATED
          enum:
            - COMPARATIVE_PROPERTY_UPDATED
        operator:
          type: string
          description: A string that defines the operator used in the comparison.
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
            A string representing the default value to be used for comparison if
            no other value is set.
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether objects with no value set should be
            included in the operation.
        operationType:
          type: string
          description: >-
            A string indicating the type of operation. The default value is
            'COMPARATIVE_DATE'.
          default: COMPARATIVE_DATE
          enum:
            - COMPARATIVE_DATE
        operator:
          type: string
          description: A string representing the operator used for comparison.
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
            value set for the property being operated on.
        numberOfDays:
          type: integer
          description: >-
            An integer specifying the number of days that define the rolling
            date range.
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
          description: A string representing the operator used in the operation.
        requiresTimeZoneConversion:
          type: boolean
          description: >-
            A boolean indicating whether the operation requires conversion based
            on time zone.
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
            A boolean indicating whether to include objects that have no value
            set for the property.
        numberOfDays:
          type: integer
          description: >-
            An integer specifying the number of days over which the rolling
            update operation is applied.
          format: int32
        operationType:
          type: string
          description: >-
            A string indicating the type of operation. The default value is
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
            A string representing the type of operation, defaulting to
            'ENUMERATION'.
          default: ENUMERATION
          enum:
            - ENUMERATION
        operator:
          type: string
          description: A string indicating the operator used in the operation.
        values:
          type: array
          description: >-
            An array of strings representing the values involved in the
            enumeration operation.
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
            A boolean indicating whether to include objects that have no value
            set for the property.
        operationType:
          type: string
          description: >-
            A string indicating the type of operation. The default and only
            valid value is 'ALL_PROPERTY_TYPES'.
          default: ALL_PROPERTY
          enum:
            - ALL_PROPERTY
        operator:
          type: string
          description: A string representing the operator to be used in the operation.
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
            A boolean indicating whether to include objects that do not have a
            value set.
        lowerBound:
          type: integer
          description: An integer representing the lower bound of the range.
          format: int64
        operationType:
          type: string
          description: >-
            A string that specifies the type of operation. The default value is
            'RANGED_NUMBER'.
          default: NUMBER_RANGED
          enum:
            - NUMBER_RANGED
        operator:
          type: string
          description: A string representing the operator used in the operation.
        upperBound:
          type: integer
          description: An integer representing the upper bound of the range.
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
            A string indicating the type of operation, which is 'MULTISTRING' by
            default.
          default: MULTISTRING
          enum:
            - MULTISTRING
        operator:
          type: string
          description: A string representing the operator used for the operation.
        values:
          type: array
          description: >-
            An array of strings representing the values to be used in the
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
          description: An integer representing the day involved in the date operation.
          format: int32
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether objects without a set value should be
            included in the operation.
        month:
          type: string
          description: A string representing the month involved in the date operation.
        operationType:
          type: string
          description: A string indicating the type of operation, which is always 'DATE'.
          default: DATE
          enum:
            - DATE
        operator:
          type: string
          description: A string representing the operator used in the date operation.
        year:
          type: integer
          description: An integer representing the year involved in the date operation.
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
            A string indicating the start month of the fiscal year. Valid values
            include 'JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE',
            'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', and
            'DECEMBER'.
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
            set for the property.
        operationType:
          type: string
          description: >-
            A string indicating the type of operation, which is always
            'CALENDAR_DATE'.
          default: CALENDAR_DATE
          enum:
            - CALENDAR_DATE
        operator:
          type: string
          description: A string representing the operator used in the operation.
        timeUnit:
          type: string
          description: A string specifying the unit of time for the operation.
        timeUnitCount:
          type: integer
          description: An integer specifying the count of the time units for the operation.
          format: int32
        useFiscalYear:
          type: boolean
          description: A boolean indicating whether the fiscal year should be used.
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
            The default value to be used for comparison if the property value is
            not set, represented as a string.
        includeObjectsWithNoValueSet:
          type: boolean
          description: >-
            A boolean indicating whether to include objects that have no value
            set for the property.
        operationType:
          type: string
          description: >-
            A string indicating the type of operation, which is
            'COMPARATIVE_STRING' by default.
          default: COMPARATIVE_STRING
          enum:
            - COMPARATIVE_STRING
        operator:
          type: string
          description: >-
            The operator used for the comparison operation. It is a string
            value.
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
            An object that defines the operation to be performed on the
            specified property. This operation can be one of several types, such
            as boolean, number, string, or date operations, among others.
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
            A string representing the specific property of the event that the
            filter is targeting.
    PublicInListFilterMetadata:
      required:
        - id
        - inListType
      type: object
      properties:
        id:
          type: string
          description: >-
            The unique identifier for the list. It is a string that specifies
            which list the filter is associated with.
        inListType:
          type: string
          description: >-
            A string representing the type of list used in the filter. This
            property defines the context or category of the list being
            referenced.
    PublicTimeOffset:
      required:
        - amount
        - offsetDirection
        - timeUnit
      type: object
      properties:
        amount:
          type: integer
          description: An integer specifying the amount of time units for the offset.
          format: int64
        offsetDirection:
          type: string
          description: >-
            A string indicating the direction of the time offset. Valid values
            are 'BEFORE' and 'AFTER'.
        timeUnit:
          type: string
          description: >-
            A string representing the unit of time for the offset, such as
            'DAYS', 'HOURS', 'MINUTES', etc.
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
          description: A string indicating the type of time representation.
          default: DATE
          enum:
            - DATE
        timezoneSource:
          type: string
          description: A string specifying the source of the timezone information.
        year:
          type: integer
          description: An integer representing the year component of the date.
          format: int32
        zoneId:
          type: string
          description: A string representing the identifier for the timezone.
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
            A reference point for indexing the time, which can be one of several
            predefined time references such as 'NOW', 'TODAY', 'WEEK', etc.
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
            A string representing the type of time point, which is always
            'INDEXED'.
          default: INDEXED
          enum:
            - INDEXED
        timezoneSource:
          type: string
          description: A string indicating the source of the timezone information.
        zoneId:
          type: string
          description: A string representing the identifier for the timezone.
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
            A string that denotes the property used as the reference for the
            time operation.
        referenceType:
          type: string
          description: A string indicating the type of reference used for the property.
        timeType:
          type: string
          description: >-
            A string indicating the type of time reference, which is
            'PROPERTY_REFERENCED' by default.
          default: PROPERTY_REFERENCED
          enum:
            - PROPERTY_REFERENCED
        timezoneSource:
          type: string
          description: A string representing the source of the timezone information.
        zoneId:
          type: string
          description: A string specifying the identifier for the timezone.
      x-hubspot-sub-type-impl: true
    PublicNowReference:
      title: NOW
      required:
        - referenceType
      type: object
      properties:
        hour:
          type: integer
          description: An integer representing the hour of the current time.
          format: int32
        millisecond:
          type: integer
          description: An integer representing the millisecond of the current time.
          format: int32
        minute:
          type: integer
          description: An integer representing the minute of the current time.
          format: int32
        referenceType:
          type: string
          description: >-
            A string that indicates the type of reference, which is always 'NOW'
            for this component.
          default: NOW
          enum:
            - NOW
        second:
          type: integer
          description: An integer representing the second of the current time.
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
          description: >-
            A string representing the day of the week. Valid values include
            'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY',
            'SUNDAY'.
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
          description: An integer representing the millisecond within the second.
          format: int32
        minute:
          type: integer
          description: An integer representing the minute within the hour.
          format: int32
        referenceType:
          type: string
          description: >-
            A string indicating the type of reference, which is 'WEEK' by
            default.
          default: WEEK
          enum:
            - WEEK
        second:
          type: integer
          description: An integer representing the second within the minute.
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
          description: >-
            An integer representing the day of the month within the fiscal
            quarter.
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
          description: An integer representing the month of the fiscal quarter.
          format: int32
        referenceType:
          type: string
          description: >-
            A string indicating the type of reference, which is 'FISCAL_QUARTER'
            by default.
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
        referenceType:
          type: string
          description: >-
            A string that specifies the type of reference, defaulting to
            'FISCAL_YEAR'.
          default: FISCAL_YEAR
          enum:
            - FISCAL_YEAR
        second:
          type: integer
          description: An integer representing the second component of the time.
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
            A string that indicates the type of reference, which is 'YEAR' by
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
          description: An integer representing the day within the month.
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
          description: An integer representing the month within the quarter.
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
            A string indicating the type of reference, which is 'MONTH' by
            default.
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
          description: An integer representing the number of days for the offset.
          format: int32
        hours:
          type: integer
          description: An integer representing the number of hours for the offset.
          format: int32
        milliseconds:
          type: integer
          description: An integer representing the number of milliseconds for the offset.
          format: int32
        minutes:
          type: integer
          description: An integer representing the number of minutes for the offset.
          format: int32
        months:
          type: integer
          description: An integer representing the number of months for the offset.
          format: int32
        quarters:
          type: integer
          description: An integer representing the number of quarters for the offset.
          format: int32
        seconds:
          type: integer
          description: An integer representing the number of seconds for the offset.
          format: int32
        weeks:
          type: integer
          description: An integer representing the number of weeks for the offset.
          format: int32
        years:
          type: integer
          description: An integer representing the number of years for the offset.
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
            crm.pipelines.approval.read: ''
            crm.pipelines.governance.read: ''
            crm.pipelines.governance.write: ''
            crm.pipelines.stage_permissions.read: ''
            crm.pipelines.stage_permissions.write: ''

````