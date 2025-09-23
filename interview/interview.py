from interview.question_generation import QuestionGenerator
from interview.answer_evaluation import AnswerEvaluator
from interview.feedback import FeedbackManager
from interview.branching_logic import BranchingLogic

class TechnicalInterview:
    def __init__(self, llm, vector_store=None):
        self.llm = llm
        self.vector_store = vector_store
        self.question_generator = QuestionGenerator(llm, vector_store)
        self.answer_evaluator = AnswerEvaluator()
        self.feedback_manager = FeedbackManager()
        self.branching_logic = BranchingLogic()
        self.evaluations = []

    def start_interview(self, topic):
        print(f"Starting interview on {topic}...")
        
        for i in range(3):  # Ask 3 questions in total
            question = self.ask_question(topic)
            print(f"Question {i+1}: {question}")
            answer = input("Your answer: ")
            evaluation = self.answer_evaluator.evaluate(answer)
            self.evaluations.append(evaluation)
            
            feedback = self.feedback_manager.provide_feedback(evaluation)
            print("Feedback for your answer:")
            print(feedback)
            
            # Adjust the topic based on the answer evaluation (branching logic)
            topic = self.branching_logic.adjust_topic_based_on_answer(evaluation)
            
        self.summarize_performance()

    def ask_question(self, topic):
        # Attempt to retrieve questions from vector store or generate dynamically
        questions = self.question_generator.load_questions_from_vector_store(topic)
        if not questions:
            question = self.question_generator.generate_dynamic_question(topic)
        else:
            question = questions[0]  # Choose the first question from vector store
        return question

    def summarize_performance(self):
        summary = self.feedback_manager.summarize_performance(self.evaluations)
        print("\nInterview Summary:")
        print(summary)
