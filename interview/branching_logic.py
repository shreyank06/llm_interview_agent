class BranchingLogic:
    def __init__(self):
        pass

    def adjust_topic_based_on_answer(self, evaluation):
        """
        Adjust topic or difficulty based on the user's answer evaluation.
        The next question can be customized based on clarity, accuracy, and depth.
        """
        clarity_score = evaluation.get("clarity", 0)
        accuracy_score = evaluation.get("accuracy", 0)
        depth_score = evaluation.get("depth", 0)
        
        # Adjusting difficulty based on clarity, accuracy, and depth
        if clarity_score < 4:
            return "Beginner-level questions (focus on clarity)"
        elif accuracy_score < 5:
            return "Intermediate-level questions (focus on accuracy)"
        elif depth_score < 6:
            return "Intermediate-level questions (focus on depth)"
        elif clarity_score >= 7 and accuracy_score >= 7 and depth_score >= 7:
            return "Advanced-level topics (strong performer)"
        else:
            return "Intermediate-level questions (balanced difficulty)"
