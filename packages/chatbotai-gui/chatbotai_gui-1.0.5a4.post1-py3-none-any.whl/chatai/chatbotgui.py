import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import openai
import google.generativeai as genai
import os
from meta_ai_api import MetaAI

class SoftwareInterpreter:
    def __init__(self, ai_type="meta", api_key=None, font="Arial",openai_maxtoken=250):
        self.ai_type = ai_type
        self.font = font
        self.api_key = api_key # API key for the AI model
        self.configure_ai()
        self.muted = False  # Initialize mute status
        self.openai_maxtoken = openai_maxtoken
        # List of available fonts
        self.fonts_list = self.get_installed_fonts()

    def configure_ai(self):
        if self.ai_type == "gemini":
            genai.configure(api_key=self.api_key)
        elif self.ai_type == "meta":
            self.meta_ai = MetaAI()
        elif self.ai_type == "chatgpt":
            openai.api_key = self.api_key
        else:
            raise ValueError("Unsupported AI type. Choose from 'gemini', 'meta', or 'chatgpt'.")

    def get_installed_fonts(self):
        """Returns a list of all installed fonts on the system."""
        fonts = list(tkfont.families())
        return sorted(fonts)

    def get_response(self, prompt):
        if self.muted:
            return "The bot is muted. Please unmute to receive responses."
        
        if self.ai_type == "gemini":
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return response.text
        elif self.ai_type == "meta":
            response = self.meta_ai.prompt(message=prompt)
            return response['message']
        elif self.ai_type == "chatgpt":
            response = openai.OpenAI(api_key=self.api_key).chat.completions.create(
                model="gpt-4o-mini",
                max_tokens=self.openai_maxtoken,
                messages=[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": prompt}]
            )
            return response.choices[0].message
    def toggle_mute(self):
        """Toggles the mute status.""" 
        self.muted = not self.muted
        return "Bot muted." if self.muted else "Bot unmuted."

    def change_font(self, font_name):
        """Change the font of the chat interface and update the GUI."""
        font_name = font_name.strip('"')
        
        if font_name in self.fonts_list:
            self.font = font_name
            return f"Font changed to {font_name}."
        else:
            return f"Font {font_name} is not available. Available fonts are: {', '.join(self.fonts_list)}"

    def set_api_key(self, api_key):
        """Sets a new API key and reconfigures the AI."""
        self.api_key = api_key
        self.configure_ai()  # Ensure the new API key is used
        return "API key updated successfully."

    def switch_bot(self, bot_type):
        """Switch between bots."""
        if bot_type in ["gemini", "meta", "chatgpt"]:
            self.ai_type = bot_type
            self.configure_ai()
            return f"Switched to {bot_type} bot."
        else:
            return "Invalid bot type. Choose from 'gemini', 'meta', or 'chatgpt'."

    def show_font_help(self):
        """Returns help text for the font command."""
        return (
            "/font set <font_name> - Change the font to the specified font name (e.g., 'Arial').\n"
            "/font list - List all available fonts installed on your system.\n"
            "Note: Fonts are case-sensitive and must match the exact name."
        )

    def show_help(self):
        """Returns general help text."""
        return (
            "/mute - Mute or unmute the bot.\n"
            "/say <message> - Send a custom message without bot processing.\n"
            "/font <set/list> - Change or list the fonts.\n"
            "/apikey <API_KEY> - Set or view the current API key.\n"
            "/switch <bot_name> - Switch between 'gemini', 'meta', or 'chatgpt' bots.\n"
            "/help - Show this help message."
        )


class ChatbotApp:
    def __init__(self, root=None):
        self.root = root or tk.Tk()  # If root is provided, use it; otherwise create a new Tk instance.
        self.root.title("Chatbot Interface")

        # Create the chat area and set it to be non-editable
        self.chat_area = tk.Text(self.root, state=tk.DISABLED, wrap=tk.WORD, height=20, width=50)
        self.chat_area.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        
        # Input field for user to type messages
        self.entry = tk.Entry(self.root, font=("Arial", 14))
        self.entry.pack(fill=tk.X, padx=10, pady=10)
        self.entry.bind("<Return>", self.send_message)
        
        self.chatbot = SoftwareInterpreter()

    def display_message(self, message, side="left"):
        """Displays the message in the chat area."""
        self.chat_area.config(state=tk.NORMAL)
        if side == "left":
            self.chat_area.insert(tk.END, f"Bot: {message}\n")
        else:
            self.chat_area.insert(tk.END, f"You: {message}\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

    def send_message(self, event):
        """Handles sending the user's message and receiving the bot's response."""
        user_message = self.entry.get().strip()
        
        if user_message:  # Only send non-empty messages
            self.display_message(user_message, side="right")  # Show user's message
            
            # Check for special commands
            if user_message.startswith("/mute"):
                bot_response = self.chatbot.toggle_mute()
            elif user_message.startswith("/say"):
                bot_response = user_message[5:].strip() if len(user_message) > 5 else "Usage: /say <message>"
            elif user_message.startswith("/font set"):
                font_name = user_message[9:].strip()
                bot_response = self.chatbot.change_font(font_name)
                # Update the font in the input field and chat area after the font change
                self.entry.config(font=(self.chatbot.font, 14))
                self.chat_area.config(font=(self.chatbot.font, 14))
            elif user_message.startswith("/font list"):
                bot_response = "\n".join(self.chatbot.fonts_list)
            elif user_message.startswith("/font"):
                bot_response = self.chatbot.show_font_help()
            elif user_message.startswith("/apikey"):
                new_api_key = user_message[8:].strip()
                if new_api_key:
                    bot_response = self.chatbot.set_api_key(new_api_key)
                else:
                    bot_response = f"Current API key: {self.chatbot.api_key if self.chatbot.api_key else 'Not set'}"
            elif user_message.startswith("/switch"):
                bot_type = user_message[8:].strip()
                bot_response = self.chatbot.switch_bot(bot_type)
            elif user_message.startswith("/help"):
                bot_response = self.chatbot.show_help()
            else:
                bot_response = self.chatbot.get_response(user_message)  # Get bot response
            
            self.display_message(bot_response, side="left")  # Show bot's response
        
        self.entry.delete(0, tk.END)  # Clear the input field after sending the message

    def run(self):
        """Starts the tkinter GUI main loop."""
        self.root.mainloop()


if __name__ == "__main__":
    app = ChatbotApp()
    app.run()
