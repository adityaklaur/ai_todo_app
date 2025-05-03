import google.generativeai as genai

# Configure API key (you can also move this to a .env file for security)
genai.configure(api_key="AIzaSyAu3VT1JMCEeOr_0XuTrcdE-tYa7xVjHj4")  # Replace with your actual API key

# Load the Gemini model
model = genai.GenerativeModel('models/gemini-1.5-pro')

def classify_task_relative(task_name, all_task_names):
    # Join all task names for context
    tasks_string = "\n".join(f"- {name}" for name in all_task_names)
    
    # Prompt instructing the model to assign relative priority
    prompt = (
        f"Here is a list of tasks:\n{tasks_string}\n\n"
        f"Based on urgency and importance, assign a priority score from 1 (least important) to 10 (most important) "
        f"to the task: '{task_name}'. Only return a number."
    )
    
    response = model.generate_content(prompt)

    # Debug output
    print(f"Task: {task_name}, Raw response: {response.text}")

    try:
        score = int(response.text.strip())
    except ValueError:
        score = 5  # Default fallback
    return score

def prioritize_tasks(task_list):
    all_names = [task["name"] for task in task_list]
    for task in task_list:
        task["score"] = classify_task_relative(task["name"], all_names)
    return sorted(task_list, key=lambda x: x["score"], reverse=True)