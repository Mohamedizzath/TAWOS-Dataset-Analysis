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

# # Team Size Query
# team_size_query = """
#     SELECT p.Name, COUNT(u.ID) AS Team_Size
#     FROM User u
#     JOIN Project p ON u.Project_ID = p.ID
#     GROUP BY p.Name;
# """
# team_size_df = fetch_data(team_size_query)

# # Visualizations
# sns.set(style="whitegrid")

# # Team Size Visualization
# plt.figure(figsize=(10, 6))
# sns.barplot(x="Name", y="Team_Size", data=team_size_df, palette="viridis")
# plt.title("Team Size by Project")
# plt.xlabel("Project Name")
# plt.ylabel("Team Size")
# plt.xticks(rotation=45, ha='right')
# plt.show()


# # Turnover Query
# turnover_query = """
#     SELECT p.Name, COUNT(cl.To_Value) AS Contributors
#     FROM Change_Log cl
#     JOIN Issue i ON cl.Issue_ID = i.ID
#     JOIN Project p ON i.project_id = p.ID
#     WHERE cl.Field = 'Assignee'
#     GROUP BY p.Name, i.project_id
#     ORDER BY i.project_id;
# """
# turnover_df = fetch_data(turnover_query)

# # Turnover Visualization
# plt.figure(figsize=(10, 6))
# sns.barplot(x="Name", y="Contributors", data=turnover_df, palette="coolwarm")
# plt.title("Team Member Turnover by Project")
# plt.xlabel("Project ID")
# plt.ylabel("Number of Contributors changes")
# plt.xticks(rotation=45, ha='right')
# plt.show()



# Task Distribution Query
task_distribution_query = """
    SELECT Assignee_ID, COUNT(ID) AS Task_Count, Project_ID
    FROM Issue
    GROUP BY Assignee_ID, Project_ID;
"""
task_dist_df = fetch_data(task_distribution_query)

# Task Distribution Visualization
plt.figure(figsize=(12, 6))
sns.boxplot(x="Project_ID", y="Task_Count", data=task_dist_df, palette="Set2")
plt.title("Task Distribution Across Projects")
plt.xlabel("Project ID")
plt.ylabel("Task Count per Assignee")
# plt.xticks(rotation=45, ha='right')

plt.show()
