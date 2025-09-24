class FeedbackManager:
    def __init__(self):
        pass

    def provide_feedback(self, evaluation):
        """Provide feedback based on evaluation messages (AI response)"""
        # Extract the AI's message from the evaluation (last AI message)
        ai_message = evaluation['messages'][-1].content  # AI message
        
        # Clean and format feedback for readability
        return f"AI Feedback: {ai_message}"

    def summarize_performance(self, evaluations):
        """Summarize overall performance from multiple answers"""
        total_score = 0
        total_questions = len(evaluations)
        performance_summary = []

        for evaluation in evaluations:
            # Get clarity, accuracy, and depth scores
            clarity_score = evaluation.get("clarity", 0)
            accuracy_score = evaluation.get("accuracy", 0)
            depth_score = evaluation.get("depth", 0)
            
            # Append individual scores to the summary
            performance_summary.append(
                f"Clarity: {clarity_score}/10, Accuracy: {accuracy_score}/10, Depth: {depth_score}/10"
            )
            
            # Sum the scores for each answer
            total_score += clarity_score + accuracy_score + depth_score
        
        # Calculate average score for the performance
        average_score = total_score / (total_questions * 3)  # 3 aspects per answer
        
        # Append overall performance to the summary
        performance_summary.append(f"\nOverall Performance: {average_score:.2f}/10")
        
        return "\n".join(performance_summary)
