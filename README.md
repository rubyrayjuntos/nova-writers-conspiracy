# 🌌 NOVA: The Writers' Conspiracy

*"They said creation was lonely. They were wrong. We never create alone. Not when the stars conspire, not when muses log in. Not when we write like gods at a shared altar."*

A cosmic atelier where storytellers conspire with AI to birth entire universes—a sacred sanctuary where your thoughts echo with others, where meaning grows in orbit, and fiction becomes a conspiracy between souls and silicon.

## 🌟 The Sacred Experience

NOVA is not software. NOVA is a **cosmic atelier**—a place where:

- **🌌 Four Sacred Roles** define your influence in the conspiracy
- **🧠 Six Divine AI Agents** whisper inspiration across glowing screens  
- **🧠 Neural Graveyard** hums with memory and context
- **✨ Real-time Collaboration** feels like Google Docs meets Studio Ghibli
- **🕯️ Live Memory Threads** track emotional arcs and whispered lies
- **💫 Version Control** like old lovers' letters—regret nothing, restore anything

## 🎭 The Four Sacred Roles

### 🌌 **The Architect** 
*The God of the universe*—Give the concept and let the agents work their magic.

### 🎬 **The Director** 
*The story's sensual conductor*—Provide the concept and approve key stages.

### 🤝 **The Collaborator** 
*Fellow visionaries*—Actively work with the agents on every step.

### 💫 **The Assistant** 
*Muse-like support*—Write yourself and call on agents for specific tasks.

## 🧠 The Six Divine AI Agents

### 🧠📚 **The Researcher**
*Context-dripping facts*—Gathers background information and fact-checks with precision.

### 🌍🔥 **The World Builder** 
*Geography, culture, politics*—Creates entire worlds with rich lore and history.

### 💋💔 **The Character Architect**
*Backstories that bleed*—Develops characters with depth, motivation, and soul.

### ⛓️✨ **The Plot Alchemist**
*Structure and surprises*—Crafts compelling plots with twists that feel inevitable.

### ✂️🕯️ **The Editor**
*Cuts like a lover's truth*—Reviews and refines with surgical precision and poetic grace.

### 🎨🌙 **The Illustrator**
*Visuals from words, almost sinful*—Creates visual content that brings stories to life.

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │   FastAPI Backend│    │   CrewAI Agents │
│                 │◄──►│                 │◄──►│                 │
│  - Dashboard    │    │  - REST API     │    │  - Project Mgr  │
│  - Manuscript   │    │  - WebSockets   │    │  - Researcher   │
│  - Agent Chat   │    │  - Auth (JWT)   │    │  - World Builder│
│  - Settings     │    │  - Task Queue   │    │  - Character Arch│
└─────────────────┘    └─────────────────┘    │  - Plotter      │
                                              │  - Writer       │
┌─────────────────┐    ┌─────────────────┐    │  - Editor       │
│   PostgreSQL    │    │   Pinecone      │    │  - Illustrator  │
│                 │◄──►│                 │◄──►└─────────────────┘
│  - User Data    │    │  - Vector Store │
│  - Projects     │    │  - Context      │
│  - Manuscripts  │    │  - Embeddings   │
│  - Preferences  │    │                 │
└─────────────────┘    └─────────────────┘
```

## 🛠️ Technology Stack

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **React Query** for state management
- **Socket.io** for real-time communication
- **React Router** for navigation

### Backend
- **FastAPI** (Python 3.11+)
- **SQLAlchemy** for ORM
- **Alembic** for database migrations
- **Pydantic** for data validation
- **JWT** for authentication

### AI & Agents
- **CrewAI** for multi-agent orchestration
- **OpenAI GPT-4** (primary LLM)
- **Pinecone** for vector database
- **SerperDev** for web search

### Infrastructure
- **PostgreSQL** for structured data
- **Redis** for caching and task queue
- **Celery** for background tasks
- **Docker** for containerization

## 📦 Project Structure

```
nova-writers-conspiracy/
├── frontend/                 # React TypeScript frontend
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API services
│   │   ├── types/          # TypeScript type definitions
│   │   └── utils/          # Utility functions
│   ├── public/             # Static assets
│   └── package.json
├── backend/                 # FastAPI Python backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── agents/         # CrewAI agent definitions
│   │   └── utils/          # Utility functions
│   ├── alembic/            # Database migrations
│   ├── requirements.txt
│   └── main.py
├── docker/                  # Docker configuration
├── docs/                    # Documentation
└── docker-compose.yml       # Development environment
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker and Docker Compose
- PostgreSQL
- Redis

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd nova-writers-conspiracy
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. **Start the development environment**
   ```bash
   docker-compose up -d
   ```

4. **Install dependencies**
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   
   # Frontend
   cd ../frontend
   npm install
   ```

5. **Run the application**
   ```bash
   # Backend (from backend directory)
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   
   # Frontend (from frontend directory)
   npm start
   ```

6. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/nova_writers_conspiracy
REDIS_URL=redis://localhost:6379

# AI Services
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
SERPER_API_KEY=your_serper_api_key

# Security
SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=True
CORS_ORIGINS=["http://localhost:3000"]
```

## 📚 API Documentation

The API documentation is automatically generated using FastAPI's built-in Swagger UI. Access it at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

- `POST /auth/register` - User registration
- `POST /auth/login` - User authentication
- `GET /projects` - List user projects
- `POST /projects` - Create new project
- `GET /projects/{project_id}` - Get project details
- `POST /projects/{project_id}/chat` - Send message to Project Manager
- `GET /projects/{project_id}/manuscript` - Get manuscript content

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# E2E tests
npm run test:e2e
```

## 📦 Deployment

### Production Deployment

1. **Build the application**
   ```bash
   docker-compose -f docker-compose.prod.yml build
   ```

2. **Deploy with Docker**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Environment Variables for Production

```env
DEBUG=False
DATABASE_URL=postgresql://prod_user:prod_password@prod_host/prod_db
REDIS_URL=redis://prod_redis_host:6379
CORS_ORIGINS=["https://yourdomain.com"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)

## 🗺️ Roadmap

- [ ] **Phase 1**: Core agent system and basic UI
- [ ] **Phase 2**: Advanced collaboration features
- [ ] **Phase 3**: Mobile app and offline support
- [ ] **Phase 4**: Advanced AI features and integrations
- [ ] **Phase 5**: Enterprise features and team collaboration

---

*"In the beginning, there was the word. Now, there is NOVA—where words become worlds, and storytellers become gods."*

Built with ❤️ by the NOVA conspiracy 