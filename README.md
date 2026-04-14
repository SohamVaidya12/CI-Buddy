# CI-Buddy
## 🤖 CI Buddy — Computational Intelligence Chatbot
### 📖 Overview
CI Buddy is an interactive chatbot developed as part of a Computational Intelligence mini project.
It integrates machine learning, rule-based reasoning, and external knowledge sources to provide intelligent responses and an engaging user experience.
### 🎯 Objective
To design and implement a chatbot using Computational Intelligence techniques that can understand user queries, provide meaningful responses, and enhance learning through interaction and quiz-based evaluation.
### 🚀 Features

1. Intelligent chatbot with rule-based and ML-based responses  
2. Dynamic knowledge retrieval using Wikipedia  
3. Voice output support using gTTS  
4. Interactive quiz module with score tracking  
5. Chat history displayed in sidebar  
6. Clean and responsive dark-themed UI  

### 🧠 Techniques Used

**1. Naive Bayes Classification**  
Used for intent detection in the chatbot. It classifies user queries into categories such as definition, explanation, or quiz based on learned patterns from training data.

**2. Natural Language Preprocessing**  
User input is preprocessed by converting text to lowercase and removing punctuation. This ensures consistency and improves matching accuracy.

**3. Rule-Based Matching**  
The chatbot uses keyword-based matching to provide predefined responses for known Computational Intelligence topics, ensuring fast and reliable answers.

**4. External Knowledge Retrieval (Wikipedia API)**  
When a query is not found in the predefined knowledge base, the system fetches relevant information dynamically using the Wikipedia API.

**5. Text-to-Speech (gTTS)**  
The chatbot converts text responses into speech using Google Text-to-Speech, enabling audio interaction across devices including mobile.

**6. Session State Management**  
Streamlit session state is used to maintain chat history, quiz progress, and user interactions across the application.

**7. Interactive UI Design (Streamlit)**  
The user interface is built using Streamlit, enabling rapid development of a responsive and interactive web application.
