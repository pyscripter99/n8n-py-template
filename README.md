# n8n_py

The n8n_py SDK connects the [n8n-nodes-python-function](https://www.npmjs.com/package/n8n-nodes-python-function) custom node with your python functions.

## Examples

### Hello World

Returns a hello world json response

```python
from n8n_py import expose_function, String

@expose_function("Hello World", "returns a friendly greeting", [
	"name": String(friendly_name="Name", description="Name of person to greet", required=True, default="Alice")
])
def hello_world(name: str): dict[str, str]: # Exposed functions must return a JSON serializable dictionary
	return {
		"greeting": f"Hello {name}!"
	}
```
