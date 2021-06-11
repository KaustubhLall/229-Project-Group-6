Objectives and Key Results
==========================


**Objectives**:

1. Decide the dataset and features we will use as the main dataset.
 
2. Data preprocessing including cleaning and possible augmentation from other datasets/API if more information is needed.
 
3. Brainstorm and refine the functionality of the dashboard UI elements. Provide the user with visualization of distribution and the ability to choose features.

4. Set up a backend for the dashboard.

5. Set up the documentation and testing.

6. Presentation.

**For objective 1**:

1. Finalize the dataset our group will be using.

2. Think about the use cases and potential prediction tasks that we will perform based on the use cases.


**For objective 2**:

1. Preprocess the raw data and get rid of some initial dead entries (N/A, NaN).

2. Encoding the categorical data to the numerical data for better future data analysis.

3. Process the numerical data according to some metrics.

4. Choose an initial set of regressors, and use a  simple regression model.

5. Assess effectiveness of the regressors and make initial plots.

6. Look at data distribution and tune the regressors, and choose more.


**For objective 3**:

1. Create a list of required figures to display on the dashboard.

2. Design the initial layout of the figures.

3. Create a design document for the user interface.

4. Program the initial layout of the figures.

5. Investigate and make initial decisions on the infrastructure needed to host and run the product.

6. Discuss the potential improvements of the dashboard features.




**For objective 4**:

1. Choose which server on AWS that we will be using for deploying our dashboard specifically if AWS Amplify Console will support our dashboard, or if more infrastructure such as EC2 is required.

2. Tried a dummy deployment and succeeded.

3. will deploy as soon as some dash codes are done

**For objective 5**:

1. Do some research about the Sphinx package to have our documentation.

2. Do some research on the testing framework that we will be using. For example, pyTest.

3. Finish the report in Sphinx and publish it in AWS


**For Objective 6**:

1. Decide the presentation material as well as the speaker.




Obstacles and Problems
----------------------
Setting up the Dash app:
 
1. No previous experience with the Plotly Dash package. It took me an entire day to figure out the syntax and set up the structure for our dashboard.

2. Some dashboard components seem to interfere with other components. When I designed the initial layout and put the visualization in, there had been many weird errors coming out because of the interference between different components. 

3. The original code for the visualization had to be changed to fit the syntax of the Plotly Dash. Specially, the Plotly Dash is only compatible with backend ‘plotly’ but not ‘bokeh‘.
The code in jupyter notebook using ‘bokeh’ backend had to be adapted in line with ‘plotly’ backend because some figure stylings are not supported.

4. For the layout part, many styles were encoded as CSS format and It took me a while to properly adjust the layouts.


Deployment:
Docker exposing ports cannot test application locally (runs on localhost on our machine, but cannot access docker port 0.0.0.0 locally to test). Changing host to 0.0.0.0 led to a lot of difficulties until we properly configured the dockerfile, however led to a lot of confusion with AWS.



