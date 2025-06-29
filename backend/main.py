from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from auth import authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from bedrock_client import generate_content
from llamaindex_client import get_context
from dynamo_client import store_content, log_event, assign_ab_variant
from datetime import timedelta, datetime
from fastapi.responses import StreamingResponse
import io
import csv

app = FastAPI()

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["user_id"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/generate")
async def generate(request: Request, current_user: dict = Depends(get_current_user)):
    data = await request.json()
    user_input = data['prompt']
    user_id = current_user['user_id']
    variant = assign_ab_variant(user_id)
    context = get_context(user_id, prompt=user_input)
    content = generate_content(user_input, context)
    store_content(user_id, content, {'input': user_input, 'context': context, 'variant': variant})
    log_event(user_id, "generate_content", {'prompt': user_input, 'variant': variant, 'timestamp': datetime.utcnow().isoformat()})
    return {"content": content, "variant": variant}

@app.post("/feedback")
async def feedback(request: Request, current_user: dict = Depends(get_current_user)):
    data = await request.json()
    feedback_value = data.get("feedback")
    variant = data.get("variant")
    prompt = data.get("prompt")
    if feedback_value not in [0, 1]:
        raise HTTPException(status_code=400, detail="Feedback must be 0 or 1")
    user_id = current_user['user_id']
    timestamp = datetime.utcnow().isoformat()
    metadata = {"feedback": feedback_value, "variant": variant, "prompt": prompt, "timestamp": timestamp}
    log_event(user_id, "feedback", metadata)
    return {"message": "Feedback received", "status": "success"}

def is_admin_user(user):
    return user.get("is_admin", False)

@app.get("/admin/feedback")
async def download_feedback(current_user: dict = Depends(get_current_user)):
    if not is_admin_user(current_user):
        raise HTTPException(status_code=403, detail="Admins only")
    import boto3
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('AnalyticsTable')
    response = table.scan(
        FilterExpression="event_type = :event",
        ExpressionAttributeValues={":event": "feedback"}
    )
    rows = response['Items']
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=['user_id', 'timestamp', 'metadata'])
    writer.writeheader()
    for row in rows:
        writer.writerow({
            "user_id": row["user_id"],
            "timestamp": row["timestamp"],
            "metadata": row["metadata"]
        })
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=feedback.csv"})
