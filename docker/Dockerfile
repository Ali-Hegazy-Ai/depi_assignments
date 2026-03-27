FROM python:3.11-slim

LABEL description="DEPI Data Engineering Assignment Environment"

WORKDIR /workspace

# Install dependencies once; Docker layer cache avoids re-downloading
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create persistent data directories
RUN mkdir -p data/raw data/processed data/output

# Expose Jupyter port
EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", \
     "--no-browser", "--allow-root", "--NotebookApp.token=''", \
     "--NotebookApp.password=''"]
# NOTE: Token/password auth is disabled for convenience on trusted local networks.
# To enable authentication, remove the token/password flags above.
