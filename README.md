# generative-ai-blog-generator-aws


# Generative AI Blog Generator with AWS Bedrock

## 🚀 Project Overview
This project is a serverless application that uses **AWS Bedrock** with **Meta's LLaMA2 model** to generate 200-word blog articles based on a topic prompt. It is deployed using **AWS Lambda**, making it cost-effective and scalable.

## 🔧 Technologies Used
- 🧠 AWS Bedrock (Meta LLaMA2 model)
- ⚡ AWS Lambda
- ☁️ AWS IAM
- 🐍 Python
- 📦 Boto3
- 🧪 JSON

## 🎯 Features
- Accepts a blog topic and returns a generated blog post
- Uses LLaMA2 hosted on AWS Bedrock
- Can be integrated with a web interface or API Gateway
- Easily extensible to other models (Anthropic, AI21, etc.)

-  Summary of Key Sections:

Section	Purpose
blog_generate_using_bedrock()	Calls AWS Bedrock to generate blog content using Meta LLaMA2
save_blog_details_s3()	Uploads generated content to an S3 bucket
lambda_handler()	Lambda entry point, coordinates blog generation and storage

My blog post about this project : https://medium.com/@ach.chathuranga/generative-ai-with-aws-a3bea00b95dd
