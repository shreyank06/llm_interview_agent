# AI-Powered Interview Agent
This project is an AI-powered technical interview agent designed to simulate a short, interactive interview. The agent dynamically generates technical questions based on the selected topic, evaluates the user's answers, and provides performance feedback.

## Technologies USed
Python, langchain, docker, llm

## Interview Flow

1. **Topic Selection**:  
   The user selects a topic for the interview (e.g., JavaScript, Python).

2. **Dynamic Question Generation**:  
   The agent generates questions based on the selected topic using LLM chain.

3. **Answer Evaluation**:  
   Each answer is scored on clarity, accuracy, and depth, which adjusts the flow of the interview.

4. **Branching Logic**:  
   If answers are weak, the agent adjusts the difficulty or topic. Strong answers lead to more advanced questions.

5. **Feedback & Evaluation**:  
   At the end, the agent provides feedback on clarity, accuracy, and depth, followed by an interview summary with strengths and improvement suggestions.

## Optional Features
**Answer Scoring:** The agent provides a detailed evaluation of answers, including scores for clarity, accuracy, and depth, helping the candidate identify areas for improvement.
## Execution
clone this repo and go to latest branch 
```
git checkout latest
```
go to
```
https://platform.openai.com/api-keys
```
create new secret api key and
go to main.py and 
on line 12 replace this line 
```
OPENAI_API_KEY = "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"
```
dont forget to paste your own personal openai api key here
```
OPENAI_API_KEY = "your personal api key"
```

install docker
```
sudo apt-get install docker-compose 
```
build docker image
```
sudo docker-compose build --no-cache
```

after the docker image is built, enter the docker env
```
docker-compose run --rm ai_interview_app
```