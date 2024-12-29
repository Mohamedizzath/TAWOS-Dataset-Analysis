import mysql.connector
from db_connect import connect_to_database
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def fetch_data(query):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(query)
    colnames = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    if data:
        # Print column names
        print("\n Column Names:", colnames)
        # Print the project table data
        print("\n Table Data:")
        for project in data:
            print(project)
    else:
        print("No data found in the database.")
        
    cursor.close()
    return pd.DataFrame(data, columns=colnames)


# 1. Unbalanced Workload

# The overall purpose of this function is to analyze how tasks are distributed among team members within different projects. 
# It computes the standard deviation of tasks per project to understand whether the workload is unbalanced. 
# A higher standard deviation indicates that some team members may be overloaded while others have fewer tasks.

def analyze_workload():
    query = """
    SELECT 
        Assignee_ID, 
        COUNT(ID) AS Task_Count, 
        Project_ID
    FROM 
        Issue
    WHERE 
        Assignee_ID IS NOT NULL
    GROUP BY 
        Assignee_ID, 
        Project_ID
    ORDER BY
        Assignee_ID;
    """
    workload_df = fetch_data(query)
    workload_df['Deviation'] = workload_df.groupby('Project_ID')['Task_Count'].transform('std')
    print("\n workload_df['Deviation']:", workload_df['Deviation'])
    return workload_df


# 2. High Turnover Rate

# The function analyzes changes made to the "Assignee" field in issues, by month and project.
# It calculates how many changes were made in total for each month (across all authors), allowing you to understand the turnover rate (assignee changes).
# The results are grouped by project, author, and month, and the total changes per month are calculated and added to the DataFrame.
# Finally, the function returns the DataFrame, which could be used for further analysis or reporting.

def analyze_turnover():
    query = """
    SELECT 
        i.Project_ID, 
        cl.Author_ID AS Assignee_ID, 
        COUNT(*) AS Changes,
        DATE_FORMAT(cl.Creation_Date, '%Y-%m') AS Month
    FROM 
        Change_Log cl
    JOIN 
        Issue i ON cl.Issue_ID = i.ID
    WHERE 
        cl.Field = 'Assignee' AND cl.Author_ID IS NOT NULL
    GROUP BY 
        i.Project_ID, cl.Author_ID, Month
    ORDER BY 
        i.Project_ID, Month;
    """
    turnover_df = fetch_data(query)
    turnover_df['Monthly_Changes'] = turnover_df.groupby('Month')['Changes'].transform('sum')
    print("\n turnover_df['Monthly_Changes']:", turnover_df['Monthly_Changes'])
    return turnover_df


# 3. Experience Gaps

# This function is useful in tracking the progress and performance of team members within different projects. 
# It gives insights into how many issues were resolved or are in progress across various statuses.

def analyze_experience():
    statuses = [
            'Done', 'Closed', 'Resolved', 
            'Testing In Progress', 'Ready for Review'
        ]

    # Convert the list of statuses into a format suitable for SQL query (i.e., a comma-separated string)
    status_filter = ",".join([f"'{status}'" for status in statuses])

    query = f"""
    SELECT 
        Assignee_ID, 
        COUNT(ID) AS Resolved_Issues, 
        Project_ID,
        Status
    FROM 
        Issue
    WHERE 
        Assignee_ID IS NOT NULL AND Status IN ({status_filter})
    GROUP BY 
        Assignee_ID, Project_ID, Status;
    """
    experience_df = fetch_data(query)
    return experience_df

# Visualizations
def plot_workload(workload_df):
    sns.boxplot(x="Project_ID", y="Task_Count", data=workload_df)
    plt.title("Workload Distribution")
    plt.show()

def plot_turnover(turnover_df):
    sns.lineplot(x="Month", y="Monthly_Changes", data=turnover_df)
    plt.title("Turnover Over Time")
    plt.xticks(rotation=45, ha='right')
    plt.show()

def plot_experience(experience_df):
    sns.barplot(x="Assignee_ID", y="Resolved_Issues", data=experience_df)
    plt.title("Resolved Issues by Team Member")
    plt.show()


def categorize_risk(team_risk_score):
    # Define thresholds for risk categories
    bins = [0, 1.0, 1.5, float('inf')]  # Adjust thresholds based on your data
    labels = ['Low', 'Medium', 'High']
    
    # Create a new column for Risk Category
    team_risk_score['Risk_Category'] = pd.cut(team_risk_score['Risk_Score'], bins=bins, labels=labels, include_lowest=True)
    return team_risk_score

    
# Combine Risk Metrics
def compute_team_risk(workload_df, turnover_df, experience_df):
    # Normalize metrics
    workload_df['Normalized_Workload'] = workload_df['Deviation'] / workload_df['Deviation'].max()
    turnover_df['Normalized_Turnover'] = turnover_df['Monthly_Changes'] / turnover_df['Monthly_Changes'].max()
    experience_df['Normalized_Experience'] = 1 - (experience_df['Resolved_Issues'] / experience_df['Resolved_Issues'].max())

    # Merge data
    team_risk_score = pd.merge(workload_df, turnover_df, on='Assignee_ID', how='inner')
    team_risk_score = pd.merge(team_risk_score, experience_df, on='Assignee_ID', how='inner')

    # Compute Risk Score
    team_risk_score['Risk_Score'] = (
        team_risk_score['Normalized_Workload'] +
        team_risk_score['Normalized_Turnover'] +
        team_risk_score['Normalized_Experience']
    )
    
    return team_risk_score


# Main Function
def main():

    # Perform analyses
    workload_df = analyze_workload()
    turnover_df = analyze_turnover()
    experience_df = analyze_experience()

    # Visualize results
    plot_workload(workload_df)
    plot_turnover(turnover_df)
    plot_experience(experience_df)

    # Combine metrics and compute risk
    team_risk_score = compute_team_risk(workload_df, turnover_df, experience_df)
    # Categorize risk
    team_risk_score = categorize_risk(team_risk_score)
    
    print("Team Risk Scores:")
    print(team_risk_score.sort_values(by="Risk_Score", ascending=False))
    
    # Save the results to a CSV file
    output_file = "team_risk_scores.csv"
    team_risk_score.to_csv(output_file, index=False)
    print(f"Team risk scores have been saved to {output_file}")

if __name__ == "__main__":
    main()