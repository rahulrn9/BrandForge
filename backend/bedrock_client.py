import boto3

REGION = "us-east-1"
bedrock = boto3.client('bedrock-runtime', region_name=REGION)

def generate_content(prompt, context):
    input_text = f"Context: {context}\nPrompt: {prompt}"
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        body=input_text.encode('utf-8')
    )
    output = response['body'].read().decode()
    return output
