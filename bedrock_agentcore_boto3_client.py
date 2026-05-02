import boto3
import json
import uuid

client = boto3.client("bedrock-agentcore", region_name="eu-west-1")
payload = json.dumps({"prompt": "Data tell me who created you!"})

session_id = str(uuid.uuid4()) + str(uuid.uuid4())
print(session_id)

response = client.invoke_agent_runtime(
    agentRuntimeArn="arn:aws:bedrock-agentcore:eu-west-1:339712939282:runtime/luna-31rJni7cl4",
    runtimeSessionId=session_id,  # Must be 33+ char. Every new SessionId will create a new MicroVM
    payload=payload,
    qualifier="DEFAULT",
    # This is Optional. When the field is not provided, Runtime will use DEFAULT endpoint
)
response_body = response["response"].read()
response_data = json.loads(response_body)
print("Agent Response:", response_data)
