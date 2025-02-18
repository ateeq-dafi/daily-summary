import streamlit as st
import openai

# Load API key from Streamlit secrets
api_key = st.secrets["openai"]["api_key"]

# Initialize OpenAI client correctly
client = openai.OpenAI(api_key=api_key)

# Function to generate structured task summary
def generate_summary(case_number, today_tasks, tomorrow_tasks, project_name):
    prompt = f"""
Here are some examples of structured task summaries. Follow this format when generating the task summary:

Case 1:
Summary (CrowdGen AI):
What I have done today?
1. I started working on credits integration part and its done and task is assigned to QA.
2. User profile update has been started and will be completed till tomorrow 4-5 PM.
What I will do tomorrow?
1. Continue work on User profile task and will be done till 5PM at max.
2. I will try my best to complete admin dashboard states integration by day end.

Case 2:
Summary (CrowdGen AI):
What I have done today?
1. I started working on credits integration part and its done and task is assigned to QA.
2. User profile update has been started and will be completed till tomorrow 4-5 PM.
What I will do tomorrow?
1. Continue work on User profile task and will be done till 5PM at max.
2. I do not have any further tasks.

Case 3:
Summary (CrowdGen AI):
What I have done today?
1. I started working on credits integration part and its done and task is assigned to QA.
2. I do not have any assigned further tasks
What I will do tomorrow?
1. Available for new tasks/project.

Case 4:
Summary (Emp Radar):
What I have done today?
1. I have done integration of user management screen. Build to test: https://app.clickup.com/t/86erf2gvw
2. I need an understanding on Radar screen with web team.
What I will do tomorrow?
1. @Johar Alam Need a meeting with web team to start new task.
2. Meeting with client at 8:30PM @Johar Alam

Case 5:
Summary (Emp Radar, CrowdGen AI):
What I have done today?
1. Tested User management screen and its QA passed and ready to move to production.
2. Tested NFT screen but it has some issues reported. Can't move to production.
What I will do tomorrow?
1. @Johar Alam Need a meeting on understanding of NFT flow for better testing.
2. @Sohail Anwar Dummy images are used in NFT so need real images tomorrow.

Case 6:
Summary (Emp Radar, CrowdGen AI):
What I have done today?
1. Email delivery issues fixed for Dafilabs site on AWS.
2. Crowdgen project deployed on staging and here is the link: https://app.clickup.com/t/86erf2gvw
What I will do tomorrow?
1. @Johar Alam Need GCP credentials for CrowdGen.
2. Configure ZOHO as new emails provider.

Now, based on the following tasks, generate the task summary:

Case {case_number}:
Summary ({project_name}):
What I have done today?
{today_tasks}

What I will do tomorrow?
{tomorrow_tasks}

Ensure the response is clear and follows the format.
"""

    # OpenAI API call
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI that formats task updates into structured reports."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=300,
    )
    
    return response.choices[0].message.content

st.set_page_config(
        page_title="Daily Summary Generator",
)

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Streamlit UI
def main():
    st.title("Daily Summary Generator")

    # Character limits
    PROJECT_NAME_LIMIT = 50
    TASKS_LIMIT = 1000

    # Input fields with validation
    project_name = st.text_input("Project Name(s)", value="CrowdGen AI, Emp Radar")
    if len(project_name) > PROJECT_NAME_LIMIT:
        st.error(f"Project Name should be at most {PROJECT_NAME_LIMIT} characters. Current length: {len(project_name)}")

    today_tasks = st.text_area("Tasks for Today", height=150)
    if len(today_tasks) > TASKS_LIMIT:
        st.error(f"Tasks for Today should be at most {TASKS_LIMIT} characters. Current length: {len(today_tasks)}")

    tomorrow_tasks = st.text_area("Tasks for Tomorrow", height=150)
    if len(tomorrow_tasks) > TASKS_LIMIT:
        st.error(f"Tasks for Tomorrow should be at most {TASKS_LIMIT} characters. Current length: {len(tomorrow_tasks)}")

    case_number = 7  # You can make this dynamic

    if st.button("Generate Report"):
        # Validate character length before processing
        if (
            len(project_name) > PROJECT_NAME_LIMIT or
            len(today_tasks) > TASKS_LIMIT or
            len(tomorrow_tasks) > TASKS_LIMIT
        ):
            st.error("Please ensure all inputs are within the character limits.")
        elif not today_tasks.strip() or not tomorrow_tasks.strip():
            st.error("Please provide tasks for both today and tomorrow.")
        else:
            with st.spinner("Generating report..."):
                try:
                    summary = generate_summary(case_number, today_tasks, tomorrow_tasks, project_name)
                    st.subheader("Generated Task Summary:")
                    st.markdown(summary.replace("\n", "  \n"))
                except Exception as e:
                    st.error(f"Error generating summary: {e}")

if __name__ == "__main__":
    main()
