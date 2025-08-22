# Medical Chatbot - Complete Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Component Details](#component-details)
5. [Data Flow](#data-flow)
6. [Setup and Installation](#setup-and-installation)
7. [API Documentation](#api-documentation)
8. [Deployment Architecture](#deployment-architecture)
9. [Security Considerations](#security-considerations)
10. [Performance Optimization](#performance-optimization)
11. [Troubleshooting](#troubleshooting)

## Project Overview

The Medical Chatbot is an intelligent conversational AI system designed to provide medical information and answer health-related queries. Built using state-of-the-art Large Language Models (LLMs), vector databases, and modern web technologies, it offers accurate and contextual responses based on medical literature.

### Key Features
- **Intelligent Q&A**: Provides accurate medical information using RAG (Retrieval-Augmented Generation)
- **Real-time Chat Interface**: Interactive web-based chat interface
- **Vector Search**: Semantic search through medical documents using embeddings
- **Scalable Architecture**: Cloud-ready deployment with AWS integration
- **Secure**: Environment-based configuration for API keys and sensitive data

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              MEDICAL CHATBOT ARCHITECTURE                        │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   USER LAYER    │    │  FRONTEND LAYER │    │ APPLICATION     │
│                 │    │                 │    │ LAYER           │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│  Web Browser    │◄──►│   Flask App     │◄──►│  LangChain      │
│  Mobile App     │    │  (chat.html)    │    │  RAG Chain      │
│                 │    │  Bootstrap UI   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │                 │    │                 │
                       │  Static Assets  │    │  Helper Module  │
                       │  (CSS/JS)       │    │  (src/helper.py)│
                       │                 │    │                 │
                       └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PROCESSING LAYER                                    │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│ Document        │    │ Text Splitter   │    │ Embedding       │
│ Loader          │    │ (Chunking)      │    │ Generation      │
│ (PyPDF)         │    │                 │    │ (HuggingFace)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│ PDF Documents   │───►│ Text Chunks     │───►│ Vector          │
│ (Medical Book)  │    │ (500 chars)     │    │ Embeddings      │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              STORAGE LAYER                                       │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│ Pinecone        │    │ Vector Index    │    │ Similarity      │
│ Vector DB       │    │ (medical-       │    │ Search          │
│                 │    │ chatbot)        │    │ (k=3)           │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│ Serverless      │    │ 384 Dimensions  │    │ Retrieved       │
│ Infrastructure  │    │ Cosine Metric   │    │ Context         │
│ (AWS)           │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              AI/ML LAYER                                         │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│ OpenAI GPT-4o   │    │ Prompt          │    │ Response        │
│ Language Model  │    │ Engineering     │    │ Generation      │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│ Context-Aware   │    │ System Prompt   │    │ Medical         │
│ Generation      │    │ + User Query    │    │ Response        │
│                 │    │ + Context       │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DEPLOYMENT LAYER                                    │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│ Docker          │    │ AWS ECR         │    │ AWS EC2         │
│ Container       │    │ (Image Registry)│    │ (Compute)       │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│ GitHub Actions  │    │ CI/CD Pipeline  │    │ Load Balancer   │
│ (CI/CD)         │    │                 │    │ (Optional)      │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Technology Stack

### Backend Technologies
- **Python 3.10+**: Core programming language
- **Flask 3.1.1**: Web framework for API endpoints
- **LangChain 0.3.26**: Framework for LLM applications
- **OpenAI GPT-4o**: Large Language Model for response generation
- **HuggingFace Transformers**: Embedding model (all-MiniLM-L6-v2)

### Vector Database
- **Pinecone**: Managed vector database for semantic search
- **Sentence Transformers**: Text embedding generation
- **384-dimensional vectors**: Optimized for semantic similarity

### Frontend Technologies
- **HTML5/CSS3**: Structure and styling
- **Bootstrap 4.1.3**: Responsive UI framework
- **jQuery 3.3.1**: JavaScript library for DOM manipulation
- **Font Awesome**: Icon library

### Document Processing
- **PyPDF 5.6.1**: PDF document parsing
- **RecursiveCharacterTextSplitter**: Text chunking strategy

### Deployment & DevOps
- **Docker**: Containerization
- **AWS EC2**: Cloud compute instances
- **AWS ECR**: Container registry
- **GitHub Actions**: CI/CD pipeline
- **Ubuntu**: Server operating system

## Component Details

### 1. Document Processing Pipeline (`src/helper.py`)

```python
# Key Functions:
- load_pdfs_from_directory(): Loads PDF documents from data directory
- filter_to_minimal_docs(): Filters document metadata
- text_split_documents(): Splits text into 500-character chunks with 20-char overlap
- download_embeddings(): Initializes HuggingFace embedding model
```

**Purpose**: Converts raw PDF medical documents into searchable vector embeddings.

### 2. Vector Storage (`store_index.py`)

```python
# Process Flow:
1. Load medical PDFs from data/ directory
2. Split documents into manageable chunks
3. Generate embeddings using sentence-transformers
4. Store vectors in Pinecone index "medical-chatbot"
5. Configure serverless infrastructure on AWS
```

### 3. Chat Application (`app.py`)

```python
# Core Components:
- Flask web server on port 8080
- PineconeVectorStore for retrieval
- ChatOpenAI for response generation
- RAG chain combining retrieval + generation
- REST API endpoints for chat functionality
```

### 4. Prompt Engineering (`src/prompt.py`)

```python
system_prompt = (
    "You are a Medical assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)
```

### 5. User Interface (`templates/chat.html`)

**Features**:
- Real-time chat interface
- Message timestamps
- Responsive design
- Bootstrap styling
- AJAX-based communication

## Data Flow

### 1. Indexing Phase (One-time Setup)
```
PDF Documents → Text Extraction → Chunking → Embedding Generation → Vector Storage (Pinecone)
```

### 2. Query Processing Phase (Runtime)
```
User Query → Embedding Generation → Vector Search → Context Retrieval → LLM Processing → Response Generation → UI Display
```

### Detailed Flow:

1. **User Input**: User types medical question in chat interface
2. **Query Processing**: Flask receives POST request with user message
3. **Embedding**: User query converted to 384-dimensional vector
4. **Similarity Search**: Pinecone finds top 3 most similar document chunks
5. **Context Assembly**: Retrieved chunks combined with system prompt
6. **LLM Generation**: GPT-4o generates response using context
7. **Response Delivery**: Answer sent back to frontend via AJAX
8. **UI Update**: Chat interface displays bot response with timestamp

## Setup and Installation

### Prerequisites
- Python 3.10+
- Conda/Miniconda
- OpenAI API Key
- Pinecone API Key
- Git

### Local Development Setup

```bash
# 1. Clone Repository
git clone https://github.com/entbappy/Build-a-Complete-Medical-Chatbot-with-LLMs-LangChain-Pinecone-Flask-AWS.git
cd Medical_Chatbot_LLMs_LangChain_Pinecone_Flask_AWS

# 2. Create Conda Environment
conda create -n medibot python=3.10 -y
conda activate medibot

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Environment Configuration
# Create .env file with:
PINECONE_API_KEY="your_pinecone_api_key"
OPENAI_API_KEY="your_openai_api_key"

# 5. Initialize Vector Database
python store_index.py

# 6. Run Application
python app.py
```

### Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8080

CMD ["python", "app.py"]
```

## API Documentation

### Endpoints

#### GET `/`
- **Description**: Serves the main chat interface
- **Response**: HTML page with chat UI
- **Content-Type**: text/html

#### POST `/get`
- **Description**: Processes chat messages and returns AI responses
- **Request Body**: 
  ```
  Content-Type: application/x-www-form-urlencoded
  msg=<user_message>
  ```
- **Response**: Plain text AI response
- **Example**:
  ```bash
  curl -X POST http://localhost:8080/get \
    -d "msg=What are the symptoms of diabetes?"
  ```

### Response Format
- **Success**: Returns medical advice as plain text
- **Error**: Returns error message or "I don't know" for unclear queries

## Deployment Architecture

### AWS Infrastructure

```
┌─────────────────────────────────────────────────────────────────┐
│                        AWS CLOUD                                 │
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │
│  │                 │    │                 │    │              │ │
│  │   GitHub        │    │   AWS ECR       │    │   AWS EC2    │ │
│  │   Actions       │───►│   Container     │───►│   Instance   │ │
│  │   (CI/CD)       │    │   Registry      │    │   (Ubuntu)   │ │
│  │                 │    │                 │    │              │ │
│  └─────────────────┘    └─────────────────┘    └──────────────┘ │
│                                                        │         │
│                                                        ▼         │
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │
│  │                 │    │                 │    │              │ │
│  │   IAM Roles     │    │   Security      │    │   Docker     │ │
│  │   & Policies    │    │   Groups        │    │   Container  │ │
│  │                 │    │                 │    │              │ │
│  └─────────────────┘    └─────────────────┘    └──────────────┘ │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                             │
│                                                                 │
│  ┌─────────────────┐                    ┌─────────────────┐     │
│  │                 │                    │                 │     │
│  │   Pinecone      │                    │   OpenAI        │     │
│  │   Vector DB     │                    │   GPT-4o API    │     │
│  │   (Serverless)  │                    │                 │     │
│  │                 │                    │                 │     │
│  └─────────────────┘                    └─────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

### Deployment Steps

1. **IAM Setup**: Create user with EC2 and ECR permissions
2. **ECR Repository**: Create container registry
3. **EC2 Instance**: Launch Ubuntu instance with Docker
4. **GitHub Secrets**: Configure API keys and AWS credentials
5. **CI/CD Pipeline**: Automated deployment on code push

### Required AWS Permissions
- `AmazonEC2ContainerRegistryFullAccess`
- `AmazonEC2FullAccess`

### GitHub Secrets Configuration
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION
ECR_REPO
PINECONE_API_KEY
OPENAI_API_KEY
```

## Security Considerations

### API Key Management
- Environment variables for sensitive data
- No hardcoded credentials in source code
- Separate .env file for local development
- GitHub Secrets for production deployment

### Network Security
- HTTPS recommended for production
- Firewall rules for EC2 instances
- VPC configuration for enhanced security
- Rate limiting for API endpoints

### Data Privacy
- No persistent storage of user conversations
- Minimal data logging
- GDPR compliance considerations
- Secure vector database access

## Performance Optimization

### Vector Search Optimization
- **Index Configuration**: 384 dimensions, cosine similarity
- **Chunk Size**: 500 characters for optimal retrieval
- **Top-K Results**: Limited to 3 for response speed
- **Caching**: Consider Redis for frequent queries

### Application Performance
- **Async Processing**: Consider async Flask for better concurrency
- **Connection Pooling**: Database connection optimization
- **CDN**: Static asset delivery optimization
- **Load Balancing**: Multiple EC2 instances for high traffic

### Cost Optimization
- **Serverless Pinecone**: Pay-per-use pricing model
- **EC2 Instance Types**: Right-sizing for workload
- **OpenAI API**: Token usage monitoring
- **Auto-scaling**: Dynamic resource allocation

## Troubleshooting

### Common Issues

#### 1. Module Import Errors
```bash
# Solution: Ensure all dependencies are installed
pip install -r requirements.txt
```

#### 2. API Key Issues
```bash
# Check .env file exists and contains valid keys
cat .env
# Verify environment variables are loaded
python -c "import os; print(os.getenv('OPENAI_API_KEY'))"
```

#### 3. Pinecone Connection Issues
```bash
# Verify Pinecone index exists
# Check API key permissions
# Ensure correct region configuration
```

#### 4. Docker Build Failures
```bash
# Check Dockerfile syntax
# Verify base image availability
# Ensure all files are copied correctly
```

### Debugging Tips

1. **Enable Debug Mode**: Set `debug=True` in Flask app
2. **Check Logs**: Monitor application logs for errors
3. **Test Components**: Isolate and test individual components
4. **Network Connectivity**: Verify external API accessibility
5. **Resource Monitoring**: Check memory and CPU usage

### Performance Monitoring

```python
# Add logging to track performance
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Track response times
start_time = time.time()
response = rag_chain.invoke({"input": input})
end_time = time.time()
logger.info(f"Response time: {end_time - start_time:.2f} seconds")
```

## Future Enhancements

### Planned Features
1. **Multi-language Support**: Extend to support multiple languages
2. **Voice Interface**: Add speech-to-text and text-to-speech
3. **Medical Image Analysis**: Integrate computer vision capabilities
4. **User Authentication**: Add user accounts and conversation history
5. **Advanced Analytics**: Usage metrics and performance monitoring
6. **Mobile App**: Native mobile application development

### Scalability Improvements
1. **Microservices Architecture**: Break down into smaller services
2. **Message Queue**: Implement async processing with Redis/RabbitMQ
3. **Database Optimization**: Add caching layers and read replicas
4. **Auto-scaling**: Implement horizontal scaling based on load
5. **Multi-region Deployment**: Global content delivery network

---

## Support and Maintenance

For technical support or questions about this documentation, please refer to the project repository or contact the development team.

**Last Updated**: January 2025
**Version**: 1.0.0