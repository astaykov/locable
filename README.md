# Locable — AI-Powered Website Builder

Locable is a low scale web development assistant that leverages *local* LLMs and vector retrieval to help you create professional websites *for free* using AI. It combines a builder agent with Bootstrap-based templates and a Chroma vector database for intelligent context retrieval.

## Features

- **AI-Powered Code Generation**: Uses local Ollama models (qwen2.5-coder by default) to generate HTML, CSS, and JavaScript
- **Bootstrap Integration**: Locally-stored Bootstrap CSS and JavaScript files for consistent, responsive design
- **Vector Retrieval (RAG)**: Chroma-backed vector store indexes Bootstrap documentation for context-aware code generation
- **Interactive CLI**: Chat-based interface to request websites and iterate on designs
- **Tool Execution**: Write, read, and list files directly from the agent
- **Local-First**: All processing happens locally, no cloud dependencies or API calls

## Project Structure

```
locable/
├── agent/                          # Agent orchestration
│   ├── agent.py                    # Tool implementations (write_file, read_file, list_files)
│   ├── builder_agent.py            # Main agent class with tool execution and model coordination
│   ├── final_model.py              # FinalModelClient wrapper for Ollama API
│   └── tools.json                  # Tool definitions (schemas for LLM)
├── rag/                            # Retrieval-Augmented Generation (RAG)
│   ├── chroma_store.py             # ChromaVectorStore class for local vector persistence
│   ├── embedding.py                # Embedding function using Ollama
│   ├── vectorstore.py              # LocalVectorStore adapter (compatibility wrapper)
│   ├── retriever.py                # Retriever class for document retrieval
│   └── __init__.py                 # Package exports
├── data/
│   ├── bootstrap/                  # Bootstrap library files
│   │   ├── bootstrap.bundle.min.js # Bootstrap JavaScript (bundled Popper.js)
│   │   └── bootstrap.min.css       # Bootstrap CSS
│   └── chroma/                     # Local vector store (auto-created)
│       ├── documents.json          # Document chunks
│       ├── ids.json                # Document IDs
│       ├── metadatas.json          # Document metadata
│       └── embeddings.npy          # Vector embeddings (NumPy binary)
├── site/                           # Generated website output
│   ├── index.html                  # Main HTML file
│   └── static/
│       ├── bootstrap.min.css       # Copy of Bootstrap CSS
│       ├── bootstrap.bundle.min.js # Copy of Bootstrap JS
│       ├── styles.css              # Custom styles
│       └── script.js               # Custom JavaScript
├── prompts/                        # LLM system prompts
│   └── system_prompt.txt           # Agent system instructions
├── .gitignore                      # Git ignore rules
├── LICENSE                         # MIT License
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Installation

### Prerequisites
- Python 3.10+
- Ollama with qwen2.5-coder:14b-instruct model (or compatible LLM)
- a lot of VRAM and/or RAM. Less means slower and less context but it would still work. recommended: 20 GB total memory and CUDA graphics card
- Windows, macOS, or Linux

### Setup

1. **Navigate to the project:**
   ```bash
   cd locable
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure Ollama is running:**
   
   In one terminal, start the Ollama server:
   ```bash
   ollama serve
   ```
   
   In another terminal, pull the default model:
   ```bash
   ollama pull qwen2.5-coder:14b-instruct
   ```

## Quick Start

### Step 1: Index Bootstrap Files (One-Time Setup)

This step chunks and embeds your Bootstrap CSS/JS files into a local Chroma vector database:

```bash
python -m rag.chroma_store
```

Expected output:
```
Chroma Vector Store Indexer
Indexed 391 chunks into Chroma collection 'bootstrap' at 'data/chroma'.
Done. Indexed 391 chunks.
```

This creates vector files in `data/chroma/` and enables retrieval-augmented generation.

### Step 2: Run the Builder Agent

Start the interactive CLI:

```bash
python -m agent.builder_agent
```

You should see:
```
Builder Agent CLI
Type a request (ex: 'Create a simple landing page')
You: 
```

### Step 3: Describe Your Website

Type a natural language description of what you want:

```
You: create a comprehensive sushi website with a hero, menu with 6 animated cards, and contact section
```

The agent will:
1. Query the vector store for Bootstrap examples
2. Generate HTML, CSS, and JavaScript using the LLM
3. Execute the `write_file` tool to save files to `site/`
4. Display completion status

#### Note
The agent has stict guidelines on what amount of information it needs to generate the website, to be able to generate detailed results. Tell it to use sample texts or ignore that, if you dont want to specify everything. Find the system prompt in [system prompt](prompts/system_prompt.txt)

### Step 4: View Your Website

Open the generated website in a browser:

```bash
# Windows
start site\index.html

# macOS
open site/index.html

# Linux
xdg-open site/index.html
```

## How It Works

### Agent Loop

1. **User Input**: Describe what website you want
2. **Retrieval**: Agent queries Chroma vector store for relevant Bootstrap patterns
3. **Model Call**: LLM (Ollama) generates HTML/CSS/JS based on request + retrieved context
4. **Tool Execution**: Agent executes `write_file` to save generated code
5. **Iteration**: Refine by asking for changes - limited by VRAM 

### Vector Store (RAG)

- **Chroma**: Local, persistent vector database
- **Embeddings**: Generated by Ollama's embedding model
- **Documents**: Bootstrap CSS/JS chunked into 1000-character pieces
- **Retrieval**: Top-3 relevant chunks injected into LLM context

### Tools Available to Agent

- `write_file(path, content)` — Write or create files
- `read_file(path)` — Read file contents
- `list_files()` — List files in the project

## Configuration

### Model Selection

Edit `agent/builder_agent.py` to use a different Ollama model:

```python
agent = BuilderAgent(
    model="llama2:13b",  # Change this
    host="http://localhost:11434"
)
```

Available models: `ollama list` or [ollama.ai/library](https://ollama.ai/library)
### Note
- the model needs to support tool calling
- better models can lead to way better results but need more system memory and vice versa

### Vector Store Settings

Edit `rag/chroma_store.py` to adjust chunking:

```python
indexed = store.index_bootstrap_files(
    source_dir="data/bootstrap",
    chunk_size=1000,      # Adjust chunk size
    overlap=200           # Adjust overlap
)
```

### System Prompt

Modify `prompts/system_prompt.txt` to change agent behavior and instructions.

## Troubleshooting

### Ollama Not Responding
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve
```

### Chroma Vector Store Empty
```bash
# Re-index Bootstrap files
python -m rag.chroma_store
```

### Model Context Overflow (500 Error)
- Restart Ollama: `taskkill /F /IM ollama.exe && ollama serve`
- Use a smaller model: `ollama pull qwen2.5-coder:7b-instruct`
- Reduce retrieval size in `builder_agent.py` `_append_retrieval_context(k=2)`

### Slow Generation
- Use a smaller/faster model
- Reduce vector retrieval count
- Ensure sufficient RAM/VRAM

## Example Requests

### Simple Landing Page
```
You: create a simple landing page for a tech startup with navbar, hero section, features, and footer
```

### Product Showcase
```
You: build a product showcase website with header, 6 product cards with descriptions, and contact form
```

### Restaurant Website
```
You: create a restaurant website with hero, menu section with 8 items, photos, and contact info
```

Generated output appears at `site/index.html`.

## Development

### Adding New Tools

1. Implement in `agent/agent.py`
2. Add schema to `agent/tools.json`
3. Register in `BuilderAgent.execute_tool()`

### Testing

```bash
# Test vector store
python -c "from rag.chroma_store import ChromaVectorStore; s = ChromaVectorStore(); print(s.query('button styles', n_results=3))"

# Test agent
python -m agent.builder_agent
```
by standart the chroma db is tested at the start of each agent run

## Performance

- **Indexing**: ~30 seconds for Bootstrap files
- **Model Response**: 30-120 seconds (depends on model and prompt)
- **Vector Retrieval**: <100ms
- **File I/O**: <100ms

## Limitations

- Local LLMs may produce less refined code than online alternatives
- Vector retrieval returns Bootstrap patterns only
- No image generation (uses placeholder URLs)
- No database/backend generation
- Single-page sites only

## Future Enhancements

- [ ] Multi-page site generation
- [ ] API endpoint scaffolding
- [ ] GUI on localhost + agent API

## License

MIT License — see `LICENSE` file for details.

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For issues or questions:
- Check Troubleshooting section above
- Review agent debug output (`[DEBUG]` logs)
- Ensure Ollama and dependencies are up-to-date
- Check that `data/chroma/` contains indexed files

## Acknowledgments

- **Bootstrap** — Frontend framework
- **Ollama** — Local LLM runtime
- **Chroma** — Vector database
- **Qwen** — Base LLM model

---

**Happy building!**
