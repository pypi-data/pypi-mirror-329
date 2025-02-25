# Ally AI Core

## How to use

### Config File

```yaml
llm:
  api_key: '<private-key>'
  api_version: "<api-version>"
  endpoint: "<endpoint>"
  model: "<model-name>"
  deployment_name: '<deployment-name>'
  temperature: 0.7
  streaming: true

embeddings:
  api_key: '<private-key>'
  api_version: "<api-version>"
  endpoint: "<endpoint>"
  model: "<model-name>"
  deployment_name: '<deployment-name>'
```



### Use Custom Settings

```yaml
my_llm:
  api_key: '<private-key>'
  api_version: "<api-version>"
```

```python
from ally_ai_core import Settings

settings = Settings(section='my_llm')

```

### Override Settings

```python
from ally_ai_core import Settings

settings = Settings(section='my_llm', api_key='<new-api-key>')
```

