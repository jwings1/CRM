> ## Documentation Index
> Fetch the complete documentation index at: https://developers.hubspot.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

---
id: 7c889823-e788-46b4-97f9-75988c8a983d
---

# Error handling

> Learn how to handle common API errors when developing with HubSpot's APIs.

Unless specified otherwise, most HubSpot endpoints will return a `200` OK response upon success. Any endpoints returning a different status code will specify the returned response in its documentation.

## Common error responses

The table below provides error responses are common to multiple HubSpot APIs:

| Error | Details |
| - | - |
| `207 Multi-Status` | Returned when there are different statuses (e.g., errors and successes), which occurs when you've enabled [multi-status error handling](#multi-status-errors) for the object API batch create endpoints. |
| `401 Unauthorized` | Returned when the authentication provided is invalid. See the [authentication overview](/docs/apps/developer-platform/build-apps/authentication/overview) for details on authenticating API requests. |
| `403 Forbidden` | Returned when the authentication provided does not have the proper permissions to access the specific URL. For example, an [OAuth token](/docs/apps/developer-platform/build-apps/authentication/oauth/working-with-oauth) that only has the `content` scope authorized would get a `403` when attempting to retrieve records from the Deals API (which requires the `crm.objects.deals.read` scope). <br /> <br /> If you've confirmed that your app has the necessary [scopes](/docs/apps/developer-platform/build-apps/authentication/scopes), please reach out to [HubSpot support](https://knowledge.hubspot.com/help-and-resources/get-help-with-hubspot) for assistance. |
| `414` | Returned in the following scenarios: <ul><li>The request URI is too long (e.g., the length of the request URL exceeds certain limits). Try shortening the URL by reducing the number of query parameters or the payload size of any associated values.</li><li>The response includes the message `Cannot have more than 250 identities on a profile`, which occurs when attempting to merge two records that were previously involved in a combined total of 250+ merges. Learn more about this behavior on the [HubSpot Knowledge Base](https://knowledge.hubspot.com/records/merge-records#merge-limit).</li></ul> |
| `423 Locked` | Returned when attempting to sync a large volume of data (e.g., upserting thousands of company records in a very short period of time). Locks will last for 2 seconds, so if you receive a `423` error, you should include a delay of at least 2 seconds between your API requests. |
| `429 Too many requests` | Returned when your account or app is over its API [rate limits](/docs/developer-tooling/platform/usage-guidelines). Find suggestions on working within those limits [here](/docs/developer-tooling/platform/usage-guidelines#Address-rate-limit-issues). |
| `477 Migration in Progress` | Returned when a HubSpot account is currently being [migrated between data hosting locations](https://www.hubspot.com/data-centers). HubSpot will return a [Retry-After](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Retry-After) response header indicating how many seconds to wait before retrying the request (typically up to 24 hours). |
| `502/504 timeouts` | Returned when HubSpot's processing limits have been met. These limits are in place to prevent a single client from causing degraded performance. <br /> <br /> These timeout responses occur when making a large number of requests over a sustained period. If you get one of these responses, you should pause your requests for a few seconds, then retry. |
| `503 service temporarily unavailable` | Returned when HubSpot is temporarily unavailable. If you receive this response, you should pause your requests for a few seconds, then retry. |
| `521 web server is down ` | Returned when HubSpot's server is down, this should be a temporary issue. If you receive this response, you should pause your requests for a few seconds, then retry. |
| `522 connection timed out` | Returned when the connection between HubSpot and your application has timed out. If you've received this response, please reach out to [HubSpot support](https://knowledge.hubspot.com/help-and-resources/get-help-with-hubspot) for assistance. |
| `523 origin is unreachable` | Returned when HubSpot is unable to contact your application. If you receive this response, you should pause your requests for a few seconds, then retry. |
| `524 timeout` | Returned when a response is not received within 100 seconds. This can occur when the HubSpot's server is overloaded, such as with a large data query. If you receive this response, you should pause your requests for a few seconds, then retry. |
| `525/526 SSL issues` | Returned when the SSL certificate is invalid or the SSL handshake fails. If you've received this response, please reach out to [HubSpot support](https://knowledge.hubspot.com/help-and-resources/get-help-with-hubspot) for assistance. |

Aside from these general errors, HubSpot error responses are intended to be human-readable. Most endpoints don't return error codes, but return a JSON formatted response with details about the error.

* For [CRM object APIs](/docs/api-reference/latest/crm/understanding-the-crm), error responses will include detailed `message`, `code`, and `context` fields, which will provide additional information on required properties that were not included in your request, as well as any issues with malformed properties in your request.
* More details for endpoint-specific errors can be found on the reference pages for the endpoint.

The code block below provides the structure of an example error from HubSpot:

```json theme={null}
{
  "status": "error",
  "message": "This will be a human readable message with details about the error.",
  "errors": [
    {
      "message": "discount was not a valid number",
      "code": "INVALID_INTEGER",
      "context": {
        "propertyName": ["discount"]
      }
    }
  ],
  "category": "VALIDATION_ERROR",
  "correlationId": "a43683b0-5717-4ceb-80b4-104d02915d8c"
}
```

<Warning>
  **Please note:** the fields in the example response above should all be treated as optional in any error parsing. The specific fields included can vary between different APIs, so any error parsing should allow for specific fields to be missing from the response.
</Warning>

## Multi-status errors

For the [object APIs'](/docs/api-reference/latest/crm/understanding-the-crm) batch create endpoints, you can enable multi status responses that include partial failures. This means the response will show which records were created and which were not. To do so, include a unique `objectWriteTraceId` value for each input in your request. The `objectWriteTraceId` can be any unique string.

For example, a request to create tickets could look like:

```json theme={null}
{
    "inputs": [
        {
            "objectWriteTraceId": "549b1c2a9350",
            "properties": {
                "hs_pipeline_stage": "1"
            }
        },
        {
            "objectWriteTraceId": "549b1c2a9351",
            "properties": {
                "missing": "1"
            }
        }
    ]
}
```

In the response, statuses are grouped so you can see which creates were successful and which failed. For the above request, your response would look like:

```json theme={null}
{
  "status": "COMPLETE",
  "results": [
    {
      "id": "1145814089",
      "properties": {
        "createdate": "2024-08-15T17:09:13.648Z",
        "hs_helpdesk_sort_timestamp": "2024-08-15T17:09:13.648Z",
        "hs_last_message_from_visitor": "false",
        "hs_lastmodifieddate": "2024-08-15T17:09:13.648Z",
        "hs_object_id": "1145814089",
        "hs_object_source": "API",
        "hs_object_source_label": "INTERNAL_PROCESSING",
        "hs_pipeline": "0",
        "hs_pipeline_stage": "1",
        "hs_ticket_id": "1145814089"
      },
      "createdAt": "2024-08-15T17:09:13.648Z",
      "updatedAt": "2024-08-15T17:09:13.648Z",
      "archived": false
    }
  ],
  "numErrors": 1,
  "errors": [
    {
      "status": "error",
      "category": "VALIDATION_ERROR",
      "message": "Property values were not valid: [{\"isValid\":false,\"message\":\"Property \\\"missing\\\" does not exist\",\"error\":\"PROPERTY_DOESNT_EXIST\",\"name\":\"missing\",\"localizedErrorMessage\":\"Property \\\"missing\\\" does not exist\",\"portalId\":891936587}]",
      "context": {
        "objectWriteTraceId": ["549b1c2a9351"]
      }
    }
  ],
  "startedAt": "2024-08-15T17:09:13.610Z",
  "completedAt": "2024-08-15T17:09:13.910Z"
}
```

## Retries

If your app or integration provides an endpoint that HubSpot will call, such as webhook subscriptions, any errors that your endpoint throws will cause HubSpot to retry the request.

### Webhooks

If your service has problems handling notifications at any time, HubSpot will attempt to resend failed notifications up to 10 times.

HubSpot will retry in the following cases:

* **Connection failed:** HubSpot cannot open an HTTP connection to the provided webhook URL.
* **Timeout:** Your service takes longer than 5 seconds to send back a response to a batch of notifications
* **Error codes:** Your service responds with any HTTP status code (`4xx` or `5xx`)

Workflows **will not** retry after receiving 4XX series response status codes. One exception to this rule is 429 rate limit errors; workflows will automatically retry after receiving a 429 response, and will respect the `Retry-After` header if present. Note that the `Retry-After` value is in milliseconds.

Notifications will be retried up to 10 times. These retries will be spread out over the next 24 hours, with varying delays between requests. Individual notifications will have some randomization applied, to prevent a large number of concurrent failures from being retried at the exact same time.

### Custom code workflow actions

If you're creating a [custom code action](/docs/api-reference/latest/automation/workflow-actions/custom-code-actions) in a workflow, and an API call in your action fails due to a rate limiting error, or a `429` or `5XX` error from `axios` or `@hubspot/api-client`, HubSpot will reattempt to execute your action for up to three days, starting one minute after failure. Subsequent failures will be retried at increasing intervals, with a maximum gap of eight hours between tries.
