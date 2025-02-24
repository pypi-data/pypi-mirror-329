ChatbotAI-GUI
=============

**ChatbotAI-GUI** is a graphical user interface (GUI) chatbot that integrates multiple AI models, including OpenAI, Meta AI, and Google Generative AI. This package allows users to interact with different AI models seamlessly through a single application.

✨ Features
------------
- Supports **OpenAI**, **Meta AI API**, and **Google Generative AI**.
- Simple and intuitive GUI for easy interaction.
- Extensible and customizable for different chatbot implementations.

📦 Installation
----------------
Install the package using:

.. code-block:: sh

    pip install chatbotai-gui

🚀 Usage
---------
After installation, you can launch the chatbot GUI using:

.. code-block:: sh

    python -m chatai

Or in a Python script:

.. code-block:: python

    from chatai.chatbotgui import ChatbotApp

    app = ChatbotApp()
    app.run()

📝 Configuration
----------------
Using the software interpreter to process API keys and bot type on launch.

.. code-block:: python

    from chatai.chatbotgui import ChatbotApp, SoftwareInterpreter

    app = ChatbotApp()
    app.chatbot = SoftwareInterpreter(
        api_key="YOUR_API_KEY_HERE",
        ai_type="GEMINI",  # Choose from "GEMINI", "CHATGPT", "META"
        font="Arial",
        openai_maxtoken=250,
    )
    app.run()

📜 License
-----------
This project is licensed under **AGPL-3.0-or-later**. See the `LICENSE` file for more details.
