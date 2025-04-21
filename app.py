import boto3                             # AWS SDK for Python - used to interact with AWS services
import botocore.config                  # For setting retry and timeout configurations
import json                             # To handle JSON formatting
from datetime import datetime           # For timestamping file names

# === Function to generate a blog using AWS Bedrock and Meta's LLaMA2 model ===
def blog_generate_using_bedrock(blogtopic: str) -> str:
    """
    Uses AWS Bedrock with Meta’s LLaMA2 model to generate a blog article based on a given topic.
    
    Parameters:
        blogtopic (str): The topic to generate the blog content for.
    
    Returns:
        str: Generated blog content as a string.
    """

    # Construct prompt formatted for LLaMA2-style model input
    prompt = f"""<s>[INST]Human: Write a 200 words blog on the topic {blogtopic}
    Assistant:[/INST]
    """

    # Request body configuration for the model
    body = {
        "prompt": prompt,
        "max_gen_len": 512,
        "temperature": 0.5,    # Controls randomness: lower = more focused output
        "top_p": 0.9           # Nucleus sampling parameter
    }

    try:
        # Create a Bedrock client to call the LLaMA2 model
        bedrock = boto3.client(
            "bedrock-runtime",
            region_name="us-east-1",     # Currently supported region
            config=botocore.config.Config(read_timeout=300, retries={'max_attempts': 3})
        )

        # Invoke the Bedrock model with the defined prompt
        response = bedrock.invoke_model(
            body=json.dumps(body),
            modelId="meta.llama2-13b-chat-v1"   # Identifier for LLaMA2 model on AWS
        )

        # Read and decode the response
        response_content = response.get('body').read()
        response_data = json.loads(response_content)

        # Extract the generated blog content
        blog_details = response_data['generation']
        return blog_details

    except Exception as e:
        # Log the error if model invocation fails
        print(f"Error generating the blog: {e}")
        return ""

# === Function to save generated blog content to AWS S3 ===
def save_blog_details_s3(s3_key: str, s3_bucket: str, generate_blog: str):
    """
    Saves the generated blog to an S3 bucket.
    
    Parameters:
        s3_key (str): The key (path) to store the file in the S3 bucket.
        s3_bucket (str): The name of the S3 bucket.
        generate_blog (str): The generated blog content.
    """
    s3 = boto3.client('s3')  # Create S3 client

    try:
        # Upload the blog content to the specified S3 location
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=generate_blog)
        print("Blog saved to S3 successfully.")
    except Exception as e:
        # Log the error if S3 upload fails
        print(f"Error saving the blog to S3: {e}")

# === Lambda entry point function ===
def lambda_handler(event, context):
    """
    AWS Lambda handler to generate a blog post and save it to S3.
    
    Event structure:
    {
        "body": "{\"blog_topic\": \"Artificial Intelligence in Healthcare\"}"
    }

    Returns:
        dict: Response with HTTP status and message.
    """

    # Parse the incoming event payload to extract the blog topic
    event = json.loads(event['body'])
    blogtopic = event['blog_topic']

    # Call the generator function to create blog content
    generate_blog = blog_generate_using_bedrock(blogtopic=blogtopic)

    if generate_blog:
        # If content was successfully generated, prepare S3 key using current timestamp
        current_time = datetime.now().strftime('%H%M%S')
        s3_key = f"blog-output/{current_time}.txt"
        s3_bucket = 'aws_bedrock_course1'

        # Save the blog content to the S3 bucket
        save_blog_details_s3(s3_key, s3_bucket, generate_blog)
    else:
        print("No blog was generated.")

    # Return HTTP response to API Gateway or invoking client
    return {
        'statusCode': 200,
        'body': json.dumps('Blog Generation is completed')
    }
🔍 Summary of Key S