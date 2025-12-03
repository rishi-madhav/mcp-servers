"""Modal deployment configuration for StudyBuddy Gradio app."""

import modal
from pathlib import Path

# Create Modal app
app = modal.App("studybuddy")

# Define the image with all dependencies
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "gradio>=5.0.0",
        "google-generativeai>=0.8.0",
        "aiosqlite>=0.19.0",
        "python-dotenv>=1.0.0",
        "httpx>=0.27.0",
    )
)

# Mount the code
mounts = [
    modal.Mount.from_local_dir(
        Path(__file__).parent / "mcp_server",
        remote_path="/root/mcp_server"
    ),
    modal.Mount.from_local_dir(
        Path(__file__).parent / "gradio_app",
        remote_path="/root/gradio_app"
    ),
]

@app.function(
    image=image,
    mounts=mounts,
    secrets=[modal.Secret.from_name("studybuddy-secrets")],  # Create this in Modal dashboard
    allow_concurrent_inputs=10,
    container_idle_timeout=300,
)
@modal.asgi_app()
def gradio_app():
    """Launch the Gradio app on Modal."""
    import sys
    sys.path.insert(0, "/root")
    
    from gradio_app.app import demo
    return demo

@app.local_entrypoint()
def main():
    """Deploy the app."""
    print("🚀 Deploying StudyBuddy to Modal...")
    print("📝 Make sure you've created 'studybuddy-secrets' in Modal dashboard with:")
    print("   - GEMINI_API_KEY")
    print("\n🌐 Your app will be available at the URL shown below:")

# To deploy:
# 1. Install Modal: pip install modal
# 2. Authenticate: modal token new
# 3. Create secret in Modal dashboard: modal secret create studybuddy-secrets GEMINI_API_KEY=your_key
# 4. Deploy: modal deploy modal_deploy.py
# 5. Visit the URL provided!
