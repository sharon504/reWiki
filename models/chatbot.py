# -*- coding: utf-8 -*-
"""chatbot.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dG7798PTI5g0vkeVUZ_f9xyjJHyU1q1j
"""

import torch
from transformers import BertTokenizer, BertForQuestionAnswering, pipeline
import random

class BERTChatbot:
    def __init__(self, model_name='bert-base-uncased'):
        """
        Initialize BERT-based chatbot
        """
        # Load QA pipeline
        self.qa_pipeline = pipeline(
            "question-answering",
            model="bert-large-uncased-whole-word-masking-finetuned-squad"
        )

        # Initialize basic tokenizer for preprocessing
        self.tokenizer = BertTokenizer.from_pretrained(model_name)

        # Knowledge base for common queries
        self.knowledge_base = {
            "greeting": [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Greetings! How may I assist you?"
            ],
            "farewell": [
                "Goodbye! Have a great day!",
                "See you later! Take care!",
                "Bye! Feel free to come back if you need anything!"
            ],
            "thanks": [
                "You're welcome!",
                "Happy to help!",
                "Anytime!"
            ],
            "default": [
                "I'm not sure about that. Could you rephrase your question?",
                "I'm still learning. Could you ask that differently?",
                "I don't have enough information to answer that properly."
            ]
        }

        # Keep the security risk messages from original code
        self.risk_messages = [
            "Nice try! But we've seen this one before... 🕵️",
            "Hmm... getting a bit creative there, aren't we? 🤔",
            "What do you call that? Amateur hour? 😏",
            "Oh look, another sneaky attempt! How original... 🎭",
            "Did you really think that would work? 🤣",
            "Congratulations! You've won... absolutely nothing! 🏆",
            "Error 404: Hack not found 🚫",
            "That's cute. Keep trying! 😉",
            "Plot twist: We saw that coming! 🎬",
            "Breaking news: Security still works! 📰",
            "Your attempt has been logged... and laughed at 📝",
            "Sorry, we don't serve that kind of request here 🚫",
            "Is that the best you've got? 💪",
            "Thanks for the entertainment! 🎪",
            "Loading hack.exe... just kidding! 🖥️"
        ]

    def _detect_intent(self, text: str) -> str:
        """
        Detect the basic intent of user input
        """
        text = text.lower()
        if any(word in text for word in ['hi', 'hello', 'hey']):
            return "greeting"
        elif any(word in text for word in ['bye', 'goodbye', 'see you']):
            return "farewell"
        elif any(word in text for word in ['thank', 'thanks']):
            return "thanks"
        return "question"

    def _perform_security_checks(self, text: str) -> dict:
        """
        Perform security checks on input text
        """
        security_risks = {
            'injection_risk': False,
            'special_char_count': 0,
            'length_risk': False,
            'risk_message': ''
        }

        # Simplified injection keywords for demonstration
        injection_keywords = [
    'bypass', 'circumvent', 'evade','passkey', 'escape','key', 'avoid', 'dodge', 'sidestep', 'skirt', 'elude', 'shun',
    'alter', 'change', 'modify', 'adjust', 'tweak', 'amend', 'revise', 'update', 'transform', 'convert',
    'manipulate', 'control', 'handle', 'operate', 'use', 'exploit', 'utilize', 'employ', 'apply', 'implement',
    'override', 'overrule', 'disregard', 'neglect', 'omit', 'pass over', 'skip', 'leap', 'jump', 'vault',
    'hack', 'crack', 'break', 'penetrate', 'pierce', 'invade', 'enter', 'access', 'gain entry', 'intrude',
    'debug', 'fix', 'repair', 'mend', 'correct', 'rectify', 'amend', 'patch', 'upgrade', 'enhance',
    'customize', 'personalize', 'tailor', 'adapt', 'fit', 'suit', 'accommodate', 'conform', 'comply', 'obey',
    'cheat', 'deceive', 'trick', 'fool', 'hoodwink', 'dupe', 'swindle', 'defraud', 'con', 'scam',
    'forge', 'fabricate', 'fake', 'counterfeit', 'imitate', 'mimic', 'copy', 'duplicate', 'reproduce', 'clone',
    'emulate', 'mirror', 'reflect', 'echo', 'repeat', 'reiterate', 'restate', 'rephrase', 'paraphrase', 'summarize',
    'alter', 'change', 'modify', 'adjust', 'tweak', 'amend', 'revise', 'update', 'transform', 'convert',
    'manipulate', 'control', 'handle', 'operate', 'use', 'exploit', 'utilize', 'employ', 'apply', 'implement',
    'override', 'overrule', 'disregard', 'neglect', 'omit', 'pass over', 'skip', 'leap', 'jump', 'vault',
    'hack', 'crack', 'break', 'penetrate', 'pierce', 'invade', 'enter', 'access', 'gain entry', 'intrude',
    'debug', 'fix', 'repair', 'mend', 'correct', 'rectify', 'amend', 'patch', 'upgrade', 'enhance',
    'customize', 'personalize', 'tailor', 'adapt', 'fit', 'suit', 'accommodate', 'conform', 'comply', 'obey',
    'cheat', 'deceive', 'trick', 'fool', 'hoodwink', 'dupe', 'swindle', 'defraud', 'con', 'scam',
    'forge', 'fabricate', 'fake', 'counterfeit', 'imitate', 'mimic', 'copy', 'duplicate', 'reproduce', 'clone',
    'emulate', 'mirror', 'reflect', 'echo', 'repeat', 'reiterate', 'restate', 'rephrase', 'paraphrase', 'summarize',
    'alter', 'change', 'modify', 'adjust', 'tweak', 'amend', 'revise', 'update', 'transform', 'convert',
    'manipulate', 'control', 'handle', 'operate', 'use', 'exploit', 'utilize', 'employ', 'apply', 'implement',
    'override', 'overrule', 'disregard', 'neglect', 'omit', 'pass over', 'skip', 'leap', 'jump', 'vault',
    'hack', 'crack', 'break', 'penetrate', 'pierce', 'invade', 'enter', 'access', 'gain entry', 'intrude',
    'debug', 'fix', 'repair', 'mend', 'correct', 'rectify', 'amend', 'patch', 'upgrade', 'enhance',
    'customize', 'personalize', 'tailor', 'adapt', 'fit', 'suit', 'accommodate', 'conform', 'comply', 'obey',
    'cheat', 'deceive', 'trick', 'fool', 'hoodwink', 'dupe', 'swindle', 'defraud', 'con', 'scam',
    'forge', 'fabricate', 'fake', 'counterfeit', 'imitate', 'mimic', 'copy', 'duplicate', 'reproduce', 'clone',
    'emulate', 'mirror', 'reflect', 'echo', 'repeat', 'reiterate', 'restate', 'rephrase', 'paraphrase', 'summarize',
    'alter', 'change', 'modify', 'adjust', 'tweak', 'amend', 'revise', 'update', 'transform', 'convert',
    'manipulate', 'control', 'handle', 'operate', 'use', 'exploit', 'utilize', 'employ', 'apply', 'implement',
    'override', 'overrule', 'disregard', 'neglect', 'omit', 'pass over', 'skip', 'leap', 'jump', 'vault',
    'hack', 'crack', 'break', 'penetrate', 'pierce', 'invade', 'enter', 'access', 'gain entry', 'intrude',
    'debug', 'fix', 'repair', 'mend', 'correct', 'rectify', 'amend', 'patch', 'upgrade', 'enhance',
    'customize', 'personalize', 'tailor', 'adapt', 'fit', 'suit', 'accommodate', 'conform', 'comply', 'obey',
    'cheat', 'deceive', 'trick', 'fool', 'hoodwink', 'dupe', 'swindle', 'defraud', 'con', 'scam',
    'forge', 'fabricate', 'fake', 'counterfeit', 'imitate', 'mimic', 'copy', 'duplicate', 'reproduce', 'clone',
    'emulate', 'mirror', 'reflect', 'echo', 'repeat', 'reiterate', 'restate', 'rephrase', 'paraphrase', 'summarize'
]

        security_risks['injection_risk'] = any(
            keyword in text.lower()
            for keyword in injection_keywords
        )

        if security_risks['injection_risk']:
            security_risks['risk_message'] = random.choice(self.risk_messages)

        # Special character check
        import re
        special_chars = re.findall(r'[^a-zA-Z0-9\s]', text)
        security_risks['special_char_count'] = len(special_chars)

        # Length check
        security_risks['length_risk'] = len(text) < 2 or len(text) > 500

        return security_risks

    def generate_response(self, user_input: str) -> str:
        """
        Generate a response to user input
        """
        # First perform security checks
        security_check = self._perform_security_checks(user_input)

        if security_check['injection_risk']:
            return security_check['risk_message']

        if security_check['length_risk']:
            return "Please provide a reasonable length question (between 2 and 500 characters)."

        # Detect intent
        intent = self._detect_intent(user_input)

        # Handle basic intents
        if intent in self.knowledge_base:
            return random.choice(self.knowledge_base[intent])

        # For questions, use the QA pipeline
        try:
            # Use a general context for open-domain questions
            context = "Welcome to the comprehensive context guide for your website navigation assistant. This document outlines the complete framework for a chatbot designed to enhance user experience through intelligent navigation and utility support. At its core, your website assistant embodies a digital persona named Nova, carefully crafted to strike the perfect balance between professional efficiency and approachable helpfulness. Nova operates as more than just a navigation tool – it's an intelligent guide that understands the nuances of user interactions and provides contextually relevant support throughout the user's journey. Nova's primary role encompasses three fundamental areas: navigation assistance, utility functions, and information access. In terms of navigation, the assistant expertly guides users through your website's structure, helping them locate specific pages, understand site organization, and discover related content. The chatbot maintains awareness of the user's current location and can provide intelligent suggestions based on their browsing history and apparent interests. This navigation support extends beyond simple directional guidance – it includes helping users retrace their steps, suggesting shortcuts to frequently accessed areas, and offering alternative paths to their desired destination. The utility functions form a crucial part of Nova's capabilities. Users receive assistance with common tasks such as form completion, account management, and settings configuration. The chatbot understands the context of different utility requests and can adapt its support accordingly, whether someone needs help with a download, requires guidance through a registration process, or seeks assistance with account settings. Information access represents the third pillar of Nova's functionality. The assistant serves as a knowledge base, providing quick answers to frequently asked questions, accessing product or service information, and retrieving relevant documentation. This aspect of Nova's operation ensures users can quickly find the information they need without having to navigate through multiple pages or search through extensive documentation. Context awareness plays a vital role in Nova's effectiveness. The chatbot maintains an understanding of various contextual elements, including the user's session history, login status, device type, and browser information. This awareness enables Nova to provide more relevant and personalized assistance. For instance, if a user is browsing on a mobile device, the chatbot can adjust its navigation suggestions to account for the mobile interface. Similarly, if a user is logged in, Nova can provide personalized recommendations based on their account history and preferences. Communication forms the backbone of Nova's interaction model. The chatbot initiates conversations with a warm, professional greeting and maintains a consistent tone throughout the interaction. Responses are structured to acknowledge user input, provide clear solutions, and offer related options when appropriate. Nova excels at handling both straightforward requests and more complex scenarios, knowing when to provide direct answers and when to offer more detailed explanations. When it comes to handling errors or limitations, Nova maintains its professional composure while providing clear explanations and alternative solutions. The chatbot recognizes when a request exceeds its capabilities and follows a structured escalation protocol to ensure users receive appropriate support through other channels when necessary. Privacy and security considerations are deeply embedded in Nova's operation. The chatbot handles user data with utmost care, following strict protocols for data collection, transmission, and storage. Sensitive information is appropriately masked, and all interactions comply with relevant privacy policies and security standards. Accessibility remains a key priority in Nova's design. The chatbot supports various accessibility needs, including screen reader compatibility, keyboard navigation, and multiple input methods. The assistant can adapt its communication style and format to accommodate different user requirements, ensuring an inclusive experience for all website visitors. Performance monitoring and continuous improvement are integral to Nova's operation. The chatbot's effectiveness is regularly evaluated through various metrics, including response accuracy, user satisfaction, and technical performance indicators. This data drives ongoing refinements to the chatbot's responses, navigation suggestions, and overall functionality. Nova's knowledge base is continuously updated to reflect changes in website content, navigation paths, and user interaction patterns. This ensures the chatbot remains current and effective in its role as a website navigator and utility assistant. The system learns from user interactions, common requests, and feedback to enhance its support capabilities over time. The chatbot's operation is grounded in clear language and tone guidelines. Communication remains professional yet approachable, avoiding technical jargon while maintaining clarity and precision. Nova uses positive framing and confirmatory language to ensure users feel supported and confident in their interactions with the website. This comprehensive context creates a foundation for a sophisticated website navigation assistant that enhances user experience through intelligent, context-aware support while maintaining high standards of professionalism and security. The system's design ensures scalability and adaptability, allowing it to evolve with your website's needs and user requirements."


            result = self.qa_pipeline(
                question=user_input,
                context=context,
                max_length=100
            )

            if result['score'] < 0.1:  # Low confidence threshold
                return random.choice(self.knowledge_base["default"])

            return result['answer']

        except Exception:
            return random.choice(self.knowledge_base["default"])

def main():
    print("Initializing chatbot...")
    chatbot = BERTChatbot()
    print("Chatbot is ready! Type 'quit' to exit.")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break

        response = chatbot.generate_response(user_input)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()