class FeedbackManager:
    def __init__(self):
        pass

    def provide_feedback(self, evaluation):
        """Provide feedback based on evaluation scores"""
        feedback = []
        for aspect, score in evaluation.items():
            feedback.append(f"{aspect.capitalize()}: {score}/10")
        return "\n".join(feedback)

    def summarize_performance(self, evaluations):
        """Summarize overall performance from multiple answers"""
        total_score = sum([sum(evaluation.values()) for evaluation in evaluations])
        average_score = total_score / (len(evaluations) * 3)  # Since each answer has 3 components: clarity, accuracy, depth
        return f"Overall Performance: {average_score:.2f}/10"
