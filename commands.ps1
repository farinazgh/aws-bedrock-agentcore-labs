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