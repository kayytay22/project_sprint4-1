# project_sprint4
Building a web page for sprint 4 project in tripleten

This project was based around developing and deploying a web application to a cloud service so that it is accessible to the public.
We worked with a dataset on car sales advertisements, keep in mind that the tools used here are to simulate random events and that this is an older dataset.

The project is started by creating accounts on Github and Render, both sites neccessary to get the application up and running smoothly. We chose Github as our primary version control site because it's such a sophisticated system that maintains a detailed history of every modification made to our project files. After our repository has been created on Github, an important step is to create a .gitignore file within it and choose the python template. From there we installed a few packages in our new Python environment, including but not limited to pandas, streamlit, plotly.express, and altair. 

We then used git to clone our new project's git repository to our local machine which is where it will be worked on. The changes made will be committed and pushed back to the repository as we go through it. VS Code must be installed and synced to our Github account so that we can load the project into it. VS Code is an optimal text editor for testing and executing code. Make sure the Python interpreter is set to the one used by the virtual environment and that the packages that are chosen to be used are installed here as well. 

Next we will download the car advertisement dataset (vehicles_us.csv) and place the dataset in the root directory of the project.

An EDA.ipynb Jupyter notebook should be created in VS Code to do our exploratory data analysis, save it to the notebooks directory. This is where we did some basic data cleanup, corrected datatypes in columns, filled missing values where it was needed, and renamed some columns for easier code development. A function was also created to go through the dataset row by row and determine the brand of the car based on the model name. We did this because the model names sometimes included the brand name but also the nickname for the brand. There were also so many unique values for model names that it made grouping accurately near impossible. To fix that, our function created a new 'brand' column that makes grouping and searching through the dataset much easier. 

We also did some price filtering to search for any possible scams, when searching for the min and max of the price range there was an absurb amount of cars priced for $1-100. All of the cars being newer models, these were definitely just click-bait ads and not real cars for sale. On the opposite end there were well over 30 cars that were priced above $110,000. Looking at the model year and odometer reading, not a single one of these cars even came close to $40,000 on the market for their age and use. Not really sure what the people behing the ads were expecting but I think it's safe to say that we can dismiss those ads as well. We capped it at $110,000 because there was a chevy corvette for sale for $109,999. While this might seem high, it's listed as a new car with only 35 miles on it, so it seems likely that this is just a really expensice brand new sports car. 

Now on to the visuals, since we had to come up with some more original ideas for histograms and charts we had to experiment with some variables. It seemed like a good idea to come up with a distribution comparison of fuel types amongst the brands. Seaborn was used to display a comparable graph and the information is not as useful as we thought. A value_counts() check confirmed that the difference is so wide between gas cars and the other types, that there's not much of a distribution to compare. However, some variables that are more common and spreadout in the dataset are odometer readings vs the condition of the car. Another plot that we came up with was a scatter plot based on the model year of the cars vs price, but differentiated by brand. A scatter plot was a good choice since there is so many data points to plot. We can clearly see a positive correlation between the price vs model year which makes sense. The newer the car, the higher the price. 

Once the EDA was done we have to put our code into the app.py file (the main python file that Render will pull from) and implement our streamlit library. We have to copy and paste some of our neccessary code from the EDA notebook to read in the dataset and correct any errors we found, as well as our function to help filter the dataset since brands will be a huge part of our visuals. 

To start the process of building the app we started with a simple header created with st.header() to create a title for the site. 
In any st.markdown() cell the three hyphens indicate a solid horizontal line through the page, which can help differentiate what the user is looking at. In any of the st.write() cells a small description of the following visuals is briefly explained, sometimes containing instructions on how to better the user's interactive experience. 

The first visual will be the dataframe itself displayed with st.dataframe(), but a sidebar was created with st.sidebar() with multiple filtering options so the user can look at the adds based on what they want to see. The user can filter based on model year, price, whether the car is 4WD or not, brand, condition, and fuel type. To filter on the model year we used a selectbox, (st.sidebar.selectbox()) with conditions set on which box they select. The price filter was created with st.sidebar.sliderbar(), with a range of lowest to highest prices. The 4WD filter was created with st.sidebar.checkbox(), this was the easiet option since that column is Boolean, returning True for 4WD and False if not. So, a checkbox made the most sense for this situation by clicking it to select all True values. Brand, condition, and fuel type filters were created with st.sidebar.multiselect() by filtering each selections unique names for the user to choose from.

The next visual was our Odometer Reading vs Condition of vehicle Histogram. We used st.multiselect() again to filter the unique condition statuses, and then used pyplot from matplotlib to display a simple histogram with all of the conditions overlapping in different colors. The user can select however many conditions to view to compare the distributions, and the histogram will change in time with the selection on both axes so that the data is easier to read and view. We used st.pyplot() to launch it.

Our last visual, the scatter plot, was created with plotly.express since we want it to be just a bit more interactive with a legend that can be clicked on to filter the plot. We included instructions to double click on the brand they want to see by itself, or they can click on a brand to remove it from the overall plot to better see comparisons. Once the plot was created we used st.plotly_chart() to launch it. 

Once the app.py file is finished and you can successfully run your app through your local machine (go to terminal - project folder - type 'streamlit run app.py'), make sure that you create 2 new files in your repository. The first being a requirement.txt file that lists all of the libaries used to create the app.

Second, we need to add the configuration file to the git repository. Create the .streamlit directory, then add the config.toml file there, the following content must be present in the .streamlit/config.toml file:

[server]
headless = true
port = 10000

[browser]
serverAddress = "0.0.0.0"
serverPort = 10000

This configuration file will tell Render where to look in order to listen to our Streamlit app when hosting it on its servers.

Next we'll go to Render.com and creat a new web service that is linked to our Github repository.
When configuring the web service, add 'pip install streamlit & pip install -r requirements.txt' to the build command. And add 'streamlit run app.py' to the start command. Finally, deploy to Render and wait for the build to succeed. 


