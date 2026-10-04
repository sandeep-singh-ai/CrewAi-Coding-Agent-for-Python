#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from coding_agent.crew import CodingAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    app_topic = input("Enter the topic of the application: ")
    if not app_topic:
        raise Exception("Topic is required")
    inputs = {
        'topic': app_topic,
        'current_year': str(datetime.now().year)
    }

    try:
        CodingAgent().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")