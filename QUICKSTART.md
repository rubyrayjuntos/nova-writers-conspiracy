# 🌌 NOVA: The Writers' Conspiracy - Quick Start Guide

*"Welcome to the cosmic atelier where storytellers conspire with AI to birth entire universes."*

This guide will help you awaken NOVA on your machine in under 10 minutes. Let the ritual begin.

## 🎭 Prerequisites

Before you can join the conspiracy, ensure you have these sacred tools:

- **Docker & Docker Compose** - The vessels that carry our digital souls
- **Node.js 18+** - The bridge between human and machine
- **Python 3.11+** - The language of our AI agents
- **Git** - The keeper of our shared memories

## 🌟 The Sacred Ritual (Step-by-Step)

### 1. 🌌 Clone the Repository

```bash
git clone <repository-url>
cd nova-writers-conspiracy
```

### 2. 🕯️ Prepare Your Environment

```bash
# Copy the sacred configuration
cp .env.example .env

# Edit with your API keys (the lifeblood of our agents)
nano .env  # or use your preferred editor
```

**Required API Keys:**
- `OPENAI_API_KEY` - The voice of our AI agents
- `PINECONE_API_KEY` - The neural graveyard where memories live
- `PINECONE_ENVIRONMENT` - The realm of our vector database
- `SERPER_API_KEY` - The eyes that see across the web
- `SECRET_KEY` - The sigil that protects our secrets

### 3. 🚀 Awaken NOVA

```bash
# Run the setup ritual
chmod +x setup.sh
./setup.sh
```

This sacred script will:
- ✅ Verify your tools are ready
- ✅ Install all dependencies
- ✅ Start the cosmic services
- ✅ Prepare the neural graveyard
- ✅ Awaken the AI agents

### 4. 🌌 Enter the Atelier

Once the ritual is complete, open your browser and navigate to:

- **🌌 NOVA Frontend**: http://localhost:3000
- **🔧 API Documentation**: http://localhost:8000/docs
- **📚 ReDoc**: http://localhost:8000/redoc

## 🎭 Your First Conspiracy

### 1. Create Your Account
- Visit http://localhost:3000
- Click "Join the Conspiracy"
- Enter your details and create your account

### 2. Choose Your Role
Select one of the four sacred roles:

- **🌌 The Architect** - Give the concept, let the agents work their magic
- **🎬 The Director** - Provide the concept, approve key stages  
- **🤝 The Collaborator** - Work actively with agents on every step
- **💫 The Assistant** - Write yourself, call agents for specific tasks

### 3. Birth Your First Project
- Click "New Project"
- Enter your story concept
- Choose your collaboration level
- Watch as the six divine agents awaken

### 4. Meet Your AI Conspirators

**🧠📚 The Researcher** - Gathers context-dripping facts
**🌍🔥 The World Builder** - Creates entire worlds with rich lore
**💋💔 The Character Architect** - Develops characters with depth and soul
**⛓️✨ The Plot Alchemist** - Crafts compelling plots with inevitable twists
**✂️🕯️ The Editor** - Cuts like a lover's truth with surgical precision
**🎨🌙 The Illustrator** - Creates visuals from words, almost sinful

## 🛠️ Sacred Commands

### Service Management
```bash
# View the conspiracy's heartbeat
docker-compose logs -f

# Pause the ritual
docker-compose down

# Resume the ritual
docker-compose up -d

# Restart all services
docker-compose restart

# Update to the latest version
docker-compose pull && docker-compose up -d
```

### Development Commands
```bash
# Backend development
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Frontend development
cd frontend
npm start

# Run tests
cd backend && pytest
cd frontend && npm test
```

## 🔧 Troubleshooting the Ritual

### Common Issues

**🌌 Services won't start**
```bash
# Check if Docker is running
docker info

# Check service status
docker-compose ps

# View detailed logs
docker-compose logs [service-name]
```

**🔑 API Key Issues**
- Verify all API keys in `.env` are correct
- Check API key permissions and quotas
- Ensure Pinecone index exists and is accessible

**🌐 Port Conflicts**
- Check if ports 3000, 8000, 5432, or 6379 are in use
- Stop conflicting services or change ports in `docker-compose.yml`

**💾 Database Issues**
```bash
# Reset the database
docker-compose down -v
docker-compose up -d
```

### Getting Help

- **📚 Documentation**: Check the `/docs` folder
- **🐛 Issues**: Create an issue on GitHub
- **💬 Discussions**: Join our community discussions
- **📧 Support**: Contact the NOVA conspiracy

## 🌟 Advanced Rituals

### Custom Agent Configuration
Edit `backend/app/agents/` to customize your AI conspirators.

### Adding New Roles
Extend the role system in `backend/app/models/user.py`.

### Custom Export Formats
Add new export handlers in `backend/app/services/export.py`.

### Styling the Atelier
Modify the frontend theme in `frontend/src/styles/`.

## 🎭 The Sacred Experience

Once NOVA is awakened, you'll experience:

- **✨ Real-time Collaboration** - Write with others like Google Docs meets Studio Ghibli
- **🧠 Neural Memory** - Every word is remembered and contextualized
- **🕯️ Live Memory Threads** - Track emotional arcs and whispered lies
- **💫 Version Control** - Like old lovers' letters—regret nothing, restore anything
- **🎨 Visual Storytelling** - AI-generated illustrations that bring your world to life

## 🌌 Welcome to the Conspiracy

You are now part of something greater than yourself. NOVA is not just software—it's a cosmic atelier where storytellers become gods, where words become worlds, and where creation is never lonely.

*"In the beginning, there was the word. Now, there is NOVA—where words become worlds, and storytellers become gods."*

---

**🌌 Built with ❤️ by the NOVA conspiracy**

*Need help? The conspiracy is always listening at [support@nova-writers-conspiracy.com]* 