import os
from app.main import App
from dotenv import load_dotenv

_ = load_dotenv()

from app import create_app  # pyright: ignore[reportImplicitRelativeImport]

app = create_app()

main = App(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "3001")))
