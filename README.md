# EduGenie – AI-Powered Educational Learning Assistant

## Project Overview

EduGenie is an AI-powered educational learning assistant designed to simplify and improve the learning experience for students. It allows users to ask academic questions, understand complex concepts through simplified explanations, summarize lengthy educational content, generate quizzes, and receive personalized learning recommendations.

The system is developed using FastAPI as the backend, HTML and CSS for the frontend, Google Gemini API for generative AI capabilities, and LaMini-Flan-T5-783M for concept explanation. EduGenie provides an accessible and lightweight learning environment that supports learners at different academic levels.

## Eight Project Phases

### 1. Brainstorming & Ideation Phase

The brainstorming and ideation phase focused on developing the idea of EduGenie as an AI-powered educational assistant. The main goal was to simplify learning by allowing students to ask questions, receive smart answers, understand complex concepts through simple explanations, generate quizzes, summarize educational content, and receive personalized learning recommendations.

### 2. Requirement Analysis Phase

This phase focused on identifying the software, frameworks, AI services, and technologies required for EduGenie. The main technologies include Python 3.10+, FastAPI, HTML, CSS, Google Gemini API, Uvicorn, and Jinja2. Different AI models and services were identified for question answering, summarization, quiz generation, learning recommendations, and concept explanation.

### 3. Project Design Phase

The project design phase focused on designing the system architecture and folder structure. EduGenie uses FastAPI as the backend and HTML/CSS as the frontend. The system contains separate modules for concept explanation, question answering, quiz generation, summarization, and learning recommendations. This modular structure supports organized development and future upgrades.

### 4. Project Planning Phase

The project planning phase organized the development activities into systematic milestones. The workflow included AI model selection, architecture design, core functionality development, frontend development, integration, and deployment. Google Gemini was planned for question answering, summarization, quiz generation, and learning paths, while LaMini-Flan-T5-783M was planned for concept explanation.

### 5. Project Development Phase

The development phase involved implementing the main EduGenie functionalities. The Explanation Module uses LaMini-Flan-T5 for simplified educational explanations. The QnA Module uses Gemini for academic and general question answering. The Quiz Module generates multiple-choice questions, while the Summary Module converts lengthy educational passages into concise versions. The Learning Path Module provides structured recommendations from beginner to advanced levels.

The project also includes FastAPI RESTful endpoints such as:

- `/qa`
- `/explain`
- `/quiz`
- `/summarize`
- `/learn/recommendations`

The frontend was developed using HTML and CSS and integrated with the backend.

### 6. Project Testing Phase

The testing phase focused on verifying the functional behavior of the EduGenie application. The application was run locally using Uvicorn and tested through the web interface. Testing included question answering, concept explanation, quiz generation, content summarization, and personalized learning recommendations.

The Quiz Module also handles JSON parsing and provides error messages when generation or parsing problems occur. Testing and fine-tuning helped improve AI-generated responses, user experience, and application performance.

### 7. Project Documentation Phase

The documentation phase recorded the complete details of the EduGenie project, including the project description, prerequisites, architecture, workflow, folder structure, modules, API endpoints, frontend integration, deployment procedure, testing activities, results, challenges, conclusion, and future enhancements.

The documentation also describes challenges such as improving AI response accuracy, maintaining performance across devices, prompt fine-tuning, UI clarity, and data privacy considerations.

### 8. Project Demonstration Phase

The demonstration phase focuses on presenting the working EduGenie application and its major features. The demonstration shows how users can ask questions, obtain simplified explanations, summarize lengthy content, generate quizzes, and receive learning recommendations from beginner to advanced levels.

The application also provides learning resources and step-by-step guidance as part of its recommendations. The demonstration showcases how all the developed modules work together through the web interface to provide an interactive AI-powered learning experience.

## Technologies Used

- Python 3.10+
- FastAPI
- Google Gemini API
- LaMini-Flan-T5-783M
- HTML
- CSS
- Jinja2
- Uvicorn

## Main Features

- AI-powered Question Answering
- Simplified Concept Explanation
- Quiz Generation
- Educational Content Summarization
- Personalized Learning Recommendations
- Learning Resources
- Beginner-to-Advanced Learning Guidance
- Interactive Web Interface
