# AWS Deployment Guide for BookBrain

This guide will help you deploy BookBrain on AWS using App Runner.

## Prerequisites

1. **AWS Account**: You need an active AWS account
2. **AWS CLI**: Install and configure AWS CLI
3. **Docker**: Install Docker Desktop (for local testing)

## Method 1: AWS App Runner (Recommended)

### Step 1: Prepare Your Repository

1. Make sure your repository is pushed to GitHub
2. Ensure you have the following files in your repo:
   - `Dockerfile`
   - `requirements.txt`
   - `streamlit_app.py`

### Step 2: Deploy on AWS App Runner

1. **Go to AWS Console**
   - Navigate to [AWS App Runner](https://console.aws.amazon.com/apprunner/)
   - Click "Create service"

2. **Source Configuration**
   - Choose "Source code repository"
   - Connect your GitHub account
   - Select your BookBrain repository
   - Choose the main branch

3. **Build Configuration**
   - Build command: Leave empty (Docker will handle this)
   - Port: `8080`
   - Runtime: `Docker`

4. **Service Configuration**
   - Service name: `bookbrain-app`
   - CPU: `1 vCPU`
   - Memory: `2 GB`
   - Environment variables:
     - `OPENAI_API_KEY`: Your API key
     - `OPENROUTER_MODEL`: (Optional) Model name

5. **Deploy**
   - Click "Create & deploy"
   - Wait for deployment (5-10 minutes)

### Step 3: Access Your App

- Once deployed, you'll get a URL like: `https://bookbrain-app.awsapprunner.com`
- Share this URL in your README and demo video

## Method 2: AWS Elastic Beanstalk

### Step 1: Create Application Files

1. **Create `.ebextensions/01_packages.config`**:
```yaml
packages:
  yum:
    git: []
    gcc: []
    python3-devel: []
```

2. **Create `.ebextensions/02_commands.config`**:
```yaml
container_commands:
  01_install_playwright:
    command: "playwright install --with-deps"
```

### Step 2: Deploy

1. Install EB CLI: `pip install awsebcli`
2. Initialize: `eb init`
3. Create environment: `eb create bookbrain-env`
4. Deploy: `eb deploy`

## Method 3: AWS ECS with Fargate

### Step 1: Create ECS Task Definition

1. Go to ECS Console
2. Create a new task definition
3. Use the provided Dockerfile
4. Set environment variables
5. Configure networking and security

### Step 2: Deploy

1. Create ECS service
2. Configure load balancer
3. Deploy and access via ALB URL

## Environment Variables

Set these in your AWS service:

- `OPENAI_API_KEY`: Your OpenRouter or OpenAI API key
- `OPENROUTER_MODEL`: (Optional) Model name like "mistralai/mistral-7b-instruct"

## Cost Estimation

- **App Runner**: ~$13/month for 1 vCPU, 2GB RAM
- **Elastic Beanstalk**: ~$20-30/month
- **ECS Fargate**: ~$15-25/month

## Troubleshooting

### Common Issues:

1. **Port Issues**: Ensure your app listens on port 8080
2. **Memory Issues**: Increase memory allocation if needed
3. **Timeout Issues**: Increase timeout settings
4. **API Key Issues**: Verify environment variables are set correctly

### Logs:

- App Runner: Check "Logs" tab in console
- Elastic Beanstalk: Use `eb logs`
- ECS: Check CloudWatch logs

## Security Best Practices

1. **Use IAM Roles**: Don't hardcode AWS credentials
2. **Environment Variables**: Store sensitive data in environment variables
3. **VPC Configuration**: Use private subnets for database connections
4. **HTTPS**: Always use HTTPS in production

## Monitoring

1. **CloudWatch**: Set up alarms for errors and performance
2. **X-Ray**: Enable tracing for debugging
3. **Health Checks**: Configure proper health check endpoints

## Scaling

- **App Runner**: Auto-scales based on traffic
- **Elastic Beanstalk**: Configure auto-scaling groups
- **ECS**: Use Application Auto Scaling

---

For more help, check the [AWS App Runner documentation](https://docs.aws.amazon.com/apprunner/). 