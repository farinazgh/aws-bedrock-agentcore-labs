agentcore configure -e .\luna.py
agentcore deploy
agentcore status

$env:OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE"
agentcore launch --env OPENAI_API_KEY=$env:OPENAI_API_KEY

$payload = @{ prompt = "Data, who was Lal?" } | ConvertTo-Json -Compress
agentcore invoke $payload


#Next steps:
#  • Run 'agentcore configure --entrypoint <file>' to set up a new agent
#  • Run 'agentcore deploy' to deploy to Bedrock AgentCore

# Pool ID: eu-west-1_evUpJWE9u
# Discovery URL: https://cognito-idp.eu-west-1.amazonaws.com/eu-west-1_evUpJWE9u/.well-known/openid-configuration
# Client ID: 7uulv7ejpvci97e2cu5ebteu6a
# Bearer Token: "bearer token here"

 agentcore invoke $payload --bearer-token="bearer-token"