# RAG Pipeline

A Python library for building Retrieval-Augmented Generation (RAG) systems using Azure OpenAI and FAISS.

## Features

- **Document Loading**: Supports loading `.txt` and `.pdf` files.
- **FAISS Indexing**: Efficient document retrieval using FAISS.
- **Azure OpenAI Integration**: Uses GPT-based models for text generation and summarization.
- **Summarization**: Generates concise summaries of loaded documents.

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/salimkhazem/rag-pipeline.git
cd rag-pipeline
pip install .
```

Alternatively, install dependencies manually:

```bash
pip install -r requirements.txt
```

## Dependencies

The following dependencies are required:

```
openai
faiss-cpu
numpy
pdfplumber
```

## Usage

### Indexing Documents

To index `.txt` and `.pdf` files in a directory:

```bash
python sample.py <directory_path>
```

Example:

```bash
python sample.py data/
```

### Summarization

To summarize documents in a directory:

```bash
python summarize.py <directory_path>
```

Example:

```bash
python summarize.py data/
```

### Sample Code

```python
from rag_pipeline import RAGPipeline

pipeline = RAGPipeline(
    azure_endpoint="your_azure_endpoint",
    api_key="your_api_key",
    api_version="your_api_version",
    embedding_deployment="text-embedding-ada-002",
    completion_deployment="gpt-4o-mini",
)

documents = [{"text": "Retrieval-Augmented Generation enhances AI capabilities."}]
pipeline.index_documents(documents)
```

## Running with Docker

### Build the Docker Image

```bash
docker build -t rag-pipeline .
```

### Run the Container with Your Folder

```bash
docker run --rm -v $(pwd)/../../Matcheen/fiches_postes:/app/data rag-pipeline /app/data
```

### Explanation:

- `--rm` → Removes the container after execution.
- `-v $(pwd)/../../Matcheen/fiches_postes:/app/data` → Mounts your local folder into `/app/data` inside the container.
- `/app/data` → Passed as an argument to `summarize.py`, which expects the directory path.

## Project Structure

```
rag-pipeline/
├── rag_pipeline/      # Main package
│   ├── __init__.py
│   ├── pipeline.py
│   ├── utils.py
│   ├── vector_stores.py
├── sample.py          # Indexing script
├── summarize.py       # Summarization script
├── setup.py           # Package setup file
├── requirements.txt   # Required dependencies
├── README.md          # Documentation
├── Dockerfile         # Docker setup
├── .gitignore
```

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-branch`
3. Commit your changes: `git commit -m "Added new feature"`
4. Push to the branch: `git push origin feature-branch`
5. Open a Pull Request.

## License

This project is licensed under the MIT License.

## Author

[Salim Khazem](mailto:salim.khazem@talan.com)

## Links

- Repository: [GitHub](https://github.com/salimkhazem/rag-pipeline)
