# Dash Basics: HTML and Core Components"}

### Objectives

After completing the lab you will be able to:

-   Create a dash application layout 
-   Add HTML H1, P, and Div components
-   Add core graph component
-   Add multiple charts

**Estimated time needed:** 30 minutes

### Dataset Used

[Airline Reporting Carrier On-Time Performance](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv)

::page{title="About Skills Network Cloud IDE"}

This Skills Network Labs Cloud IDE (Integrated Development Environment) provides a hands-on environment in your web browser for completing course and project related labs. It utilizes Theia, an open-source IDE platform, that can be run on desktop or on the cloud.
So far in the course you have been using Jupyter notebooks to run your python code. This IDE provides an alternative for editing and running your Python code. In this lab you will be using this alternative Python runtime to create and launch your Dash applications.

### Important Notice about this lab environment

Please be aware that sessions for this lab environment are not persisted. When you launch the Cloud IDE, you are presented with a 'dedicated computer on the cloud' exclusively for you. This is available to you as long as you are actively working on the labs.

Once you close your session or it is timed out due to inactivity,  you are logged off, and this ‘dedicated computer on the cloud’ is deleted along with any files you may have created, dowloaded or installed.  The next time you launch this lab, a new environment is created for you.

*If you finish only part of the lab and return later, you may have to start from the beginning. So, it is a good idea to plan to your time accordingly and finish your labs in a single session.*

::page{title="Let's start creating dash application"}

### Goal

Create a dashboard that displays the percentage of flights running under specific distance group. Distance group is the distance intervals, every 250 miles, for flight segment. If the flight covers to 500 miles, it will be under distance group 2 (250 miles + 250 miles). 

### Expected Output

Below is the expected result from the lab. Our dashboard application consists of three components:

- Title of the application
- Description of the application
- Chart conveying the proportion of distance group by month

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/labs/Module%204/images/basics_output.png)

### To do:

1.  Import required libraries and read the dataset
2.  Create an application layout
3.  Add title to the dashboard using HTML H1 component
4.  Add a paragraph about the chart using HTML P component
5.  Add the pie chart above using core graph component
6.  Run the app

::page{title="Get the tool ready"}

- Install python packages required to run the application. Copy and paste the below command to the terminal.

```
python3.8 -m pip install packaging
```

```
python3.8 -m pip install pandas dash
```

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/labs/Module%204/images/pandas_dash.PNG)

```
pip3 install httpx==0.20 dash plotly
```

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/labs/Module%204/images/install_httpx.PNG)

- Create a new python script, by clicking on the side tool bar **explorer** icon and selecting **new file** icon, as shown in the image below.

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/labs/Module%204/images/newfile1.PNG)


- Provide the file name as `dash_basics.py`

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/labs/Module%204/images/file2.png)

- Open a new terminal, by clicking on the menu bar and selecting **Terminal**->**New Terminal**, as in the image below.

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/labs/Module%204/images/terminal.png)

- Now, you have script and terminal ready to start the lab.

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/labs/Module%204/images/full.png)

::page{title="TASK 1 - Data Preparation"}

> **Note:** Throughout this lab, you will see placeholder text like ``'........'`` or `groupby(...........)`. These dots should be replaced with appropriate values such as column names ('Year', 'Vehicle_Type', etc.), grouping keys, or chart titles.
Refer to the comments and hints above each task to determine what needs to be filled in.

Let's start with

- Importing necessary libraries
- Reading and sampling 500 random data points 
- Get the chart ready

Copy the below code to the `dash_basics.py` script and review the code.

```
# Import required packages
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# Randomly sample 500 data points. Setting the random state to be 42 so that we get same result.
data = airline_data.sample(n=500, random_state=42)

# Pie Chart Creation
fig = px.pie(data, values='Flights', names='DistanceGroup', title='Distance group proportion by flights')
```

::page{title="TASK 2 - Create dash application and get the layout skeleton"}

Next, we create a skeleton for our dash application. Our dashboard application has three components as seen before:

- Title of the application
- Description of the application
- Chart conveying the proportion of distance group by month

Mapping to the respective Dash HTML tags:

- Title added using `html.H1()` tag
- Description added using `html.P()` tag
- Chart added using `dcc.Graph()` tag

Copy the below code to the `dash_basics.py` script and review the structure.

_NOTE_: Copy below the current code

```
# Create a dash application
app = dash.Dash(__name__)

# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 component
# Add description about the graph using HTML P (paragraph) component
# Finally, add graph component.
app.layout = html.Div(children=[html.H1(....),
                                html.P(....),
                                dcc.Graph(.....),
                                               
                    ])

# Run the application                   
if __name__ == '__main__':
    app.run()
```

::page{title="TASK 3 - Add the application title"}

Update the `html.H1()` tag to hold the application title. 

- Application title is `Airline Dashboard`
- Use style parameter provided below to make the title `center` aligned, with color code `#503D36`, and font-size as `40`

```
'Airline Dashboard',style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
```

After updating the `html.H1()` with the application title, the `app.layout` will look like:

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/labs/Module%204/images/1_h1.png)

::page{title="TASK 4 - Add the application description"}

Update the `html.P()` tag to hold the description of the application.

- Description is `Proportion of distance group (250 mile distance interval group) by flights.`
- Use style parameter to make the description `center` aligned and with color `#F57241`.

```
'Proportion of distance group (250 mile distance interval group) by flights.', style={'textAlign':'center', 'color': '#F57241'}
```

After updating the `html.H1()` with the application title, the `app.layout` will look like:

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/labs/Module%204/images/2_p1.png)

::page{title="TASK 5 - Update the graph"}

Update `figure` parameter of `dcc.Graph()` component to add the pie chart. We have created pie chart and assigned it to `fig`. Let's use that to update the `figure` parameter.

```
figure=fig
```

After updating the `dcc.Graph()` with the application title, the `app.layout` will look like:

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/labs/Module%204/images/3_graph.png)

Before running the application, save the file by clicking on **File -> Save** from the menu bar.

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/labs/Module%204/images/save.png)

You can Refer to the entire python code here

```

# Import required packages
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# Randomly sample 500 data points. Setting the random state to be 42 so that we get same result.
data = airline_data.sample(n=500, random_state=42)

# Pie Chart Creation
fig = px.pie(data, values='Flights', names='DistanceGroup', title='Distance group proportion by flights')

# Create a dash application
app = dash.Dash(__name__)

# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 component
# Add description about the graph using HTML P (paragraph) component
# Finally, add graph component.
app.layout = html.Div(children=[html.H1('Airline Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                                html.P('Proportion of distance group (250 mile distance interval group) by flights.', style={'textAlign':'center', 'color': '#F57241'}),
                                dcc.Graph(figure=fig),
                                               
                    ])

# Run the application                   
if __name__ == '__main__':
    app.run()

```

::page{title="TASK 6 - Run the application"}

- Run the python file using the following command in the terminal

```
python3.8 dash_basics.py
```

- Observe the port number shown in the terminal.

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/labs/Module%204/images/port.png)

- Click on the `Launch Application` option from the side menu bar.Provide the port number and click `OK`

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/labs/Module%204/images/launch_application_new.PNG)

The app will open in a new browser tab like below:

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/labs/Module%204/images/lab1_output.png)

### Congratulations, you have successfully created your first dash application!

::page{title="Exercise : Practice Tasks"}

You will practice some tasks to update the dashboard.

1.  > Change the title to the dashboard from "Airline Dashboard" to "Airline On-time Performance Dashboard" using HTML H1 component and font-size as 50.

     <details>
     <summary>Answer</summary>

    > html.H1('Airline On-time Performance Dashboard',style={'textAlign': 'center', 'color': '#503D36', 'font-size': 50}),

     </details>

2.  > Save the above changes and relaunch the dashboard application to see the updated dashboard title.

     <details>
     <summary>Answer</summary>

    > Click on file --> save file.Then go to terminal and Run the command python3 dash_basics.py to open the updated file again and relaunch     the application by entering the port number.The updated dashboard title will be seen. 

     </details>

3.  > Write a command to stop the running app in the terminal

     <details>
     <summary>Answer</summary>

    > Press `ctrl+c` inside the terminal to stop the dash application.

     </details>

## Author

[Saishruthi Swaminathan](https://www.linkedin.com/in/saishruthi-swaminathan?cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork-20297740&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ) 

<!--## Changelog

| Date       | Version | Changed by | Change Description                   |
| ---------- | ------- | ---------- | ------------------------------------ |
| 05-07-2021 | 1.1     | Saishruthi | Initial version created              |
| 24-08-2022 | 1.2     | Pratiksha  | Updated instructions                 |
| 29-08-2022 | 1.3     | Pratiksha Verma  | Updated Screenshot   |
| 06-07-2023 | 1.4    | Dr. Pooja| Code update   |
-->

## <h4 align="center"> © IBM Corporation. All rights reserved.<h4/>

