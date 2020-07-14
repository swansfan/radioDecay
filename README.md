# Dash app to model radioactive decay

This was my first attempt at writing a Dash app with not much prior experience using python, HTML and CSS. 
You can view the finished app on [Heroku](https://radiodecay.herokuapp.com/).
 
I have made use of resources and ideas from the following:
* Based on ideas and presentation of decay processes by [Dr Chris Rowan](http://all-geo.org/chris_rowan/2018/01/simulating-radioactive-decay/). 
* How to use Github and Heroku to deploy courtesy of Austin Lasseter via his [tutorial repo](https://github.com/austinlasseter/plotly_dash_tutorial) on github.
* Dash reference information from [here](https://dash.plotly.com/). I also made use of some CSS styling from one of the Dash gallery apps via the github repo [here](https://github.com/plotly/dash-sample-apps/tree/master/apps/dash-oil-and-gas). 
* As a novice to these platforms, I found the Udemy course [Interactive Python Dashboards with Plotly and Dash](https://www.udemy.com/course/interactive-python-dashboards-with-plotly-and-dash/) by [Jose Portilla](https://www.udemy.com/course/interactive-python-dashboards-with-plotly-and-dash/#instructor-1) very helpful.
  
In the future, I intend to update this by using a three tab layout to allow students to review the relevant theory and then to test their knowledge using the simulation.  
  
## Additional notes:  
It looks as if global variables were being calculated TWICE. To address this, I specified `debug=False` for app.run_server but this did not fix the issue. It was fixed by setting `heroku config:set WEB_CONCURRENCY=1` [see here](https://stackoverflow.com/questions/25504149/why-does-running-the-flask-dev-server-run-itself-twice/58028314#58028314?newreg=2250018ca7844975938bc84c306684ea).
