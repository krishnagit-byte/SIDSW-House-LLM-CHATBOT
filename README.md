-----------------------------------------------   RASA  LLM CHARBOT   --------------------------------------------------------

This project is a Rasa-based conversational chatbot integrated with large language models (LLMs) for enhanced interaction capabilities. It collects user information (name, city, phone number) through a form and supports natural language queries by leveraging external LLMs like OpenAI's GPT-3.5-turbo and a local Ollama server (Mistral model). The chatbot is designed for testing and can be extended for production use.

Features





---->   User Information Collection: Uses a form (user_info_form) to collect and validate user details:





 1.Name 



 2.City 



 3.Phone number 



----->  LLM Integration:





OpenAI: Processes natural language queries using GPT-3.5-turbo via the action_search custom action.



Ollama: Handles queries locally using the Mistral model via the action_chat_with_ollama action.



Custom Actions: Validates user input and saves data (currently logged, with placeholder for database integration).



Conversational Flow: Supports intents like greet, inform, ask_llm, and more, with responses defined in domain.yml.

-----> Project Structure





actions.py: Defines custom actions for form validation (validate_user_info_form), saving user data (action_save_user_info), and LLM interactions (action_chat_with_ollama, action_search).



config.yml: Configures the NLU pipeline (e.g., DIETClassifier, WhitespaceTokenizer) and policies (e.g., TEDPolicy, RulePolicy) for intent recognition and dialogue management.



domain.yml: Defines intents (greet, inform, ask_llm, etc.), entities (name, city, phone), slots, responses, forms, and actions.



credentials.yml: Configures communication channels (REST API, local Rasa server at http://localhost:5005/api).



endpoints.yml: Specifies the action server endpoint (http://localhost:5055/webhook) for custom actions.





HOW  ITS  WORKS



User (sends message)  
   │
   ▼
─────
     Rasa NLU Pipeline

1. WhitespaceTokenizer → splits text
2. Featurizers (Regex, Lexical, CountVectors) → turn text into numbers
3. DIETClassifier → predicts intent + entities
4. ResponseSelector (if FAQ) → retrieves canned response
5. FallbackClassifier → checks if confidence too low


   │ 
          ▼
─────
     Rasa Core Policies
  
6. MemoizationPolicy → checks if story memorized
7. RulePolicy → checks fixed rules (like fallback rules)
8. TEDPolicy → predicts next best action
9. UnexpecTEDIntentPolicy → handles unexpected input



   │
   ▼
─────
     Action Chosen
  
10. If normal intent → reply from domain.yml responses
11. If custom intent → run custom action (actions.py)




       │
       ▼
─────
     Groq API (in actions.py)

12. Your code:
       - Prepares url, headers, payload
       - Sends request → requests.post()
       - Groq model generates text (LLM response)
13. Parse Groq JSON response
14. Return AI-generated reply back to Rasa



   │
   ▼
─────
     Bot Reply to User

15. Dispatcher sends final message back to user
