# Integration Guides

## APIs For Integrating a cloud-hosted LLM agent into the REST API

If you have a remote llm, you can POST your ai result(s) back using this api:

::: client_aic.req.ai.create_ai_result.create_ai_result
    handler: python
    options:
      members:
      - create_ai_result

::: client_aic.req.ai.get_ai_result.get_ai_result

::: client_aic.req.ai.search_ai_results.search_ai_results

::: client_aic.req.ai.update_ai_result.update_ai_result
