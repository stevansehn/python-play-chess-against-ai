## Play chess against AI! 

This project creates a single-player chess game using Pygame and utilizes the Google Gemini API to generate the opponent's moves.

You will play as White and the AI will play as Black. May the best player win!

### Dependencies

- Python 3.x
- An API Key from [Google AI Studio](https://aistudio.google.com/)

**Usage:**

1. Clone the project and navigate to the project directory:

    ```bash
    git clone https://github.com/stevansehn/python-play-chess-against-ai.git
    cd python-play-chess-against-ai
    ```

2. Create a virtual environment:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install the dependencies:

    ```bash
    pip3 install --upgrade pip
    pip3 install pygame
    pip3 install asyncio
    pip3 install google-generativeai
    ```

4. Set your API Key

    In main.js, replace "MY_API_KEY" with your API Key:

    ```
    GOOGLE_API_KEY = "MY_API_KEY"
    ```

5. Run the script:
    ```bash
    python3 main.js
    ```

### Warning
Generative AIs can't guarantee 100% accurate results. You may sometimes be prompted to complete the move for it. If this happens, simply move a black piece and resume your turn.
