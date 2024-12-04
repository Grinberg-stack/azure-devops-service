import base64
# Change Organization and project by your values.
AZURE_DEVOPS_API = 'https://dev.azure.com/Organization/project/_apis'

#Personal Token (like password) for access to Azure DevOps API.
PAT = 'Your Personal Token'

# Using headers for requests - (Authorization for access | Content-Type for format)
token = f":{PAT}"  # Formatting the token for Basic Authorization
b64_token = base64.b64encode(token.encode()).decode()  # Encoding the token to Base64

HEADERS = {
    "Content-Type": "application/json",  # Default data format for API requests
    "Authorization": f"Basic {b64_token}"  # Adding the Base64 encoded token for authorization
}
