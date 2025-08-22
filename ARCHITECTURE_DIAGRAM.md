# Medical Chatbot - Architecture Diagrams

## High-Level System Architecture

```mermaid
graph TB
    subgraph "User Layer"
        U[👤 User]
        B[🌐 Web Browser]
    end
    
    subgraph "Frontend Layer"
        UI[🎨 Chat Interface<br/>HTML/CSS/JS]
        BS[📱 Bootstrap UI]
    end
    
    subgraph "Application Layer"
        FA[🐍 Flask App<br/>app.py]
        API[🔌 REST API<br/>/get endpoint]
    end
    
    subgraph "Processing Layer"
        LC[🔗 LangChain<br/>RAG Chain]
        HP[⚙️ Helper Module<br/>src/helper.py]
        PP[📝 Prompt Engine<br/>src/prompt.py]
    end
    
    subgraph "AI/ML Layer"
        EMB[🧠 HuggingFace<br/>Embeddings]
        LLM[🤖 OpenAI GPT-4o<br/>Language Model]
    end
    
    subgraph "Storage Layer"
        PC[🗄️ Pinecone<br/>Vector Database]
        PDF[📄 Medical PDFs<br/>data/]
    end
    
    subgraph "Infrastructure Layer"
        DOC[🐳 Docker<br/>Container]
        EC2[☁️ AWS EC2<br/>Compute]
        ECR[📦 AWS ECR<br/>Registry]
        GHA[🔄 GitHub Actions<br/>CI/CD]
    end
    
    U --> B
    B --> UI
    UI --> BS
    BS --> FA
    FA --> API
    API --> LC
    LC --> HP
    LC --> PP
    HP --> EMB
    LC --> LLM
    EMB --> PC
    LLM --> PC
    PDF --> HP
    FA --> DOC
    DOC --> EC2
    ECR --> EC2
    GHA --> ECR
    
    classDef userLayer fill:#e1f5fe
    classDef frontendLayer fill:#f3e5f5
    classDef appLayer fill:#e8f5e8
    classDef processLayer fill:#fff3e0
    classDef aiLayer fill:#fce4ec
    classDef storageLayer fill:#f1f8e9
    classDef infraLayer fill:#e3f2fd
    
    class U,B userLayer
    class UI,BS frontendLayer
    class FA,API appLayer
    class LC,HP,PP processLayer
    class EMB,LLM aiLayer
    class PC,PDF storageLayer
    class DOC,EC2,ECR,GHA infraLayer
```

## Data Flow Architecture

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Flask
    participant LangChain
    participant Pinecone
    participant OpenAI
    participant Response
    
    User->>Frontend: Types medical question
    Frontend->>Flask: POST /get with message
    Flask->>LangChain: Process query
    LangChain->>Pinecone: Generate query embedding
    Pinecone-->>LangChain: Return similar chunks (k=3)
    LangChain->>OpenAI: Send context + query
    OpenAI-->>LangChain: Generate response
    LangChain-->>Flask: Return answer
    Flask-->>Frontend: JSON response
    Frontend-->>User: Display chat message
```

## Document Processing Pipeline

```mermaid
flowchart LR
    subgraph "Input"
        PDF[📄 Medical Book PDF<br/>data/Medical_book.pdf]
    end
    
    subgraph "Processing"
        LOAD[📖 PyPDF Loader<br/>load_pdfs_from_directory()]
        FILTER[🔍 Filter Metadata<br/>filter_to_minimal_docs()]
        SPLIT[✂️ Text Splitter<br/>500 chars, 20 overlap]
        EMBED[🧠 Generate Embeddings<br/>all-MiniLM-L6-v2]
    end
    
    subgraph "Storage"
        PINE[🗄️ Pinecone Index<br/>medical-chatbot<br/>384 dimensions]
    end
    
    PDF --> LOAD
    LOAD --> FILTER
    FILTER --> SPLIT
    SPLIT --> EMBED
    EMBED --> PINE
    
    classDef input fill:#e3f2fd
    classDef process fill:#f3e5f5
    classDef storage fill:#e8f5e8
    
    class PDF input
    class LOAD,FILTER,SPLIT,EMBED process
    class PINE storage
```

## RAG (Retrieval-Augmented Generation) Flow

```mermaid
graph TD
    subgraph "Query Processing"
        Q[❓ User Query<br/>"What are diabetes symptoms?"]
        QE[🔄 Query Embedding<br/>384-dim vector]
    end
    
    subgraph "Retrieval Phase"
        VS[🔍 Vector Search<br/>Cosine similarity]
        TC[📝 Top Chunks<br/>k=3 most similar]
        CTX[📋 Context Assembly<br/>Combine chunks]
    end
    
    subgraph "Generation Phase"
        SP[🎯 System Prompt<br/>Medical assistant role]
        COMB[🔗 Combine<br/>Context + Query + Prompt]
        GPT[🤖 GPT-4o<br/>Generate response]
    end
    
    subgraph "Output"
        RESP[💬 Medical Response<br/>Max 3 sentences]
    end
    
    Q --> QE
    QE --> VS
    VS --> TC
    TC --> CTX
    CTX --> COMB
    SP --> COMB
    COMB --> GPT
    GPT --> RESP
    
    classDef query fill:#e1f5fe
    classDef retrieval fill:#f3e5f5
    classDef generation fill:#e8f5e8
    classDef output fill:#fff3e0
    
    class Q,QE query
    class VS,TC,CTX retrieval
    class SP,COMB,GPT generation
    class RESP output
```

## AWS Deployment Architecture

```mermaid
graph TB
    subgraph "Development"
        DEV[👨‍💻 Developer]
        GIT[📚 GitHub Repository]
    end
    
    subgraph "CI/CD Pipeline"
        GHA[🔄 GitHub Actions<br/>Workflow]
        BUILD[🔨 Docker Build]
        PUSH[📤 Push to ECR]
    end
    
    subgraph "AWS Cloud"
        subgraph "Container Services"
            ECR[📦 AWS ECR<br/>Container Registry]
        end
        
        subgraph "Compute Services"
            EC2[☁️ AWS EC2<br/>Ubuntu Instance]
            DOCKER[🐳 Docker Runtime]
        end
        
        subgraph "Security"
            IAM[🔐 IAM Roles<br/>EC2 + ECR Access]
            SG[🛡️ Security Groups<br/>Port 8080]
        end
    end
    
    subgraph "External Services"
        PINE[🗄️ Pinecone<br/>Vector Database]
        OPENAI[🤖 OpenAI API<br/>GPT-4o]
    end
    
    subgraph "Users"
        USERS[👥 End Users<br/>Web Interface]
    end
    
    DEV --> GIT
    GIT --> GHA
    GHA --> BUILD
    BUILD --> PUSH
    PUSH --> ECR
    ECR --> EC2
    EC2 --> DOCKER
    IAM --> EC2
    SG --> EC2
    DOCKER --> PINE
    DOCKER --> OPENAI
    USERS --> EC2
    
    classDef dev fill:#e3f2fd
    classDef cicd fill:#f3e5f5
    classDef aws fill:#fff3e0
    classDef external fill:#e8f5e8
    classDef users fill:#fce4ec
    
    class DEV,GIT dev
    class GHA,BUILD,PUSH cicd
    class ECR,EC2,DOCKER,IAM,SG aws
    class PINE,OPENAI external
    class USERS users
```

## Component Interaction Diagram

```mermaid
graph LR
    subgraph "Frontend Components"
        HTML[📄 chat.html<br/>Chat Interface]
        CSS[🎨 style.css<br/>Styling]
        JS[⚡ jQuery<br/>AJAX Calls]
    end
    
    subgraph "Backend Components"
        APP[🐍 app.py<br/>Flask Server]
        HELPER[⚙️ helper.py<br/>Document Processing]
        PROMPT[📝 prompt.py<br/>System Prompts]
        ENV[🔐 .env<br/>API Keys]
    end
    
    subgraph "Data Components"
        PDF[📄 Medical_book.pdf<br/>Source Data]
        INDEX[🗄️ store_index.py<br/>Vector Creation]
    end
    
    subgraph "External APIs"
        PINECONE[🗄️ Pinecone API<br/>Vector Storage]
        OPENAI[🤖 OpenAI API<br/>LLM Service]
        HF[🤗 HuggingFace<br/>Embeddings]
    end
    
    HTML --> JS
    CSS --> HTML
    JS --> APP
    APP --> HELPER
    APP --> PROMPT
    APP --> ENV
    HELPER --> PDF
    INDEX --> PDF
    INDEX --> PINECONE
    APP --> PINECONE
    APP --> OPENAI
    HELPER --> HF
    
    classDef frontend fill:#e1f5fe
    classDef backend fill:#f3e5f5
    classDef data fill:#e8f5e8
    classDef external fill:#fff3e0
    
    class HTML,CSS,JS frontend
    class APP,HELPER,PROMPT,ENV backend
    class PDF,INDEX data
    class PINECONE,OPENAI,HF external
```

## Security Architecture

```mermaid
graph TB
    subgraph "Security Layers"
        subgraph "Application Security"
            ENV[🔐 Environment Variables<br/>.env file]
            SECRETS[🔑 GitHub Secrets<br/>Production Keys]
        end
        
        subgraph "Network Security"
            HTTPS[🔒 HTTPS/TLS<br/>Encrypted Transport]
            CORS[🛡️ CORS Policy<br/>Cross-Origin Control]
        end
        
        subgraph "Infrastructure Security"
            IAM[👤 AWS IAM<br/>Role-based Access]
            SG[🛡️ Security Groups<br/>Firewall Rules]
            VPC[🏠 VPC<br/>Network Isolation]
        end
        
        subgraph "API Security"
            RATE[⏱️ Rate Limiting<br/>Request Throttling]
            AUTH[🔐 API Key Auth<br/>Service Authentication]
        end
    end
    
    subgraph "Data Protection"
        ENCRYPT[🔒 Data Encryption<br/>At Rest & Transit]
        PRIVACY[🔐 Privacy Controls<br/>No Conversation Storage]
        AUDIT[📊 Audit Logging<br/>Access Monitoring]
    end
    
    ENV --> SECRETS
    HTTPS --> CORS
    IAM --> SG
    SG --> VPC
    RATE --> AUTH
    ENCRYPT --> PRIVACY
    PRIVACY --> AUDIT
    
    classDef security fill:#ffebee
    classDef protection fill:#e8f5e8
    
    class ENV,SECRETS,HTTPS,CORS,IAM,SG,VPC,RATE,AUTH security
    class ENCRYPT,PRIVACY,AUDIT protection
```

## Performance Optimization Architecture

```mermaid
graph TB
    subgraph "Frontend Optimization"
        CDN[🌐 CDN<br/>Static Assets]
        CACHE[💾 Browser Cache<br/>CSS/JS Caching]
        COMPRESS[📦 Compression<br/>Gzip/Brotli]
    end
    
    subgraph "Application Optimization"
        ASYNC[⚡ Async Processing<br/>Non-blocking I/O]
        POOL[🏊 Connection Pooling<br/>Database Connections]
        QUEUE[📬 Message Queue<br/>Background Tasks]
    end
    
    subgraph "Database Optimization"
        INDEX[📇 Vector Indexing<br/>Optimized Search]
        BATCH[📦 Batch Processing<br/>Bulk Operations]
        REPLICA[🔄 Read Replicas<br/>Load Distribution]
    end
    
    subgraph "Infrastructure Optimization"
        LB[⚖️ Load Balancer<br/>Traffic Distribution]
        AUTO[📈 Auto Scaling<br/>Dynamic Resources]
        MONITOR[📊 Monitoring<br/>Performance Metrics]
    end
    
    CDN --> CACHE
    CACHE --> COMPRESS
    ASYNC --> POOL
    POOL --> QUEUE
    INDEX --> BATCH
    BATCH --> REPLICA
    LB --> AUTO
    AUTO --> MONITOR
    
    classDef frontend fill:#e3f2fd
    classDef app fill:#f3e5f5
    classDef database fill:#e8f5e8
    classDef infra fill:#fff3e0
    
    class CDN,CACHE,COMPRESS frontend
    class ASYNC,POOL,QUEUE app
    class INDEX,BATCH,REPLICA database
    class LB,AUTO,MONITOR infra
```

## Monitoring and Logging Architecture

```mermaid
graph TB
    subgraph "Application Monitoring"
        LOGS[📝 Application Logs<br/>Flask Logging]
        METRICS[📊 Performance Metrics<br/>Response Times]
        ERRORS[❌ Error Tracking<br/>Exception Handling]
    end
    
    subgraph "Infrastructure Monitoring"
        CPU[💻 CPU Usage<br/>EC2 Metrics]
        MEM[🧠 Memory Usage<br/>RAM Monitoring]
        DISK[💾 Disk Usage<br/>Storage Metrics]
        NET[🌐 Network I/O<br/>Bandwidth Usage]
    end
    
    subgraph "External Service Monitoring"
        API[🔌 API Response Times<br/>OpenAI/Pinecone]
        QUOTA[📊 API Quotas<br/>Usage Limits]
        HEALTH[❤️ Health Checks<br/>Service Status]
    end
    
    subgraph "Alerting System"
        ALERT[🚨 Alerts<br/>Threshold Breaches]
        NOTIFY[📧 Notifications<br/>Email/Slack]
        DASH[📈 Dashboard<br/>Real-time Metrics]
    end
    
    LOGS --> METRICS
    METRICS --> ERRORS
    CPU --> MEM
    MEM --> DISK
    DISK --> NET
    API --> QUOTA
    QUOTA --> HEALTH
    ERRORS --> ALERT
    HEALTH --> ALERT
    ALERT --> NOTIFY
    NOTIFY --> DASH
    
    classDef app fill:#e1f5fe
    classDef infra fill:#f3e5f5
    classDef external fill:#e8f5e8
    classDef alert fill:#ffebee
    
    class LOGS,METRICS,ERRORS app
    class CPU,MEM,DISK,NET infra
    class API,QUOTA,HEALTH external
    class ALERT,NOTIFY,DASH alert
```

---

## Diagram Legend

### Symbols Used
- 👤 User/Person
- 🌐 Web/Browser
- 🎨 Frontend/UI
- 🐍 Python/Backend
- 🤖 AI/ML Services
- 🗄️ Database/Storage
- ☁️ Cloud Services
- 🔐 Security/Authentication
- 📊 Monitoring/Analytics
- 🔄 Process/Workflow

### Color Coding
- **Blue** (`#e1f5fe`): User/Frontend Layer
- **Purple** (`#f3e5f5`): Application Layer
- **Green** (`#e8f5e8`): Processing/Storage Layer
- **Orange** (`#fff3e0`): Infrastructure Layer
- **Pink** (`#fce4ec`): AI/ML Layer
- **Red** (`#ffebee`): Security Layer

These diagrams provide a comprehensive visual representation of the Medical Chatbot architecture, showing how all components interact and the flow of data through the system.