# <img src="https://www.spartaquant.com/assets/img/spartaquant/icon-color.png" width="60px" alt="SpartaQube icon" class="logo-default"> SpartaQube

[SpartaQube](https://www.spartaqube.com) is a plug and play solution to visualize your data and build web components

Use SpartaQube to
1. Access your data through already built-in connectors
2. Apply transformations to your data using the SpartaQube notebook
3. Create charts and web components by dragging & dropping your transformed data

The rich user interface makes it easy to visualize and retrieve all your components

You can expose and share them with a simple html snippet code

## Installation

#### PIP INSTALL

Install the package via pip with code below:

```python
pip install spartaqube
```

To Upgrade:


```python
pip install --upgrade spartaqube
```

#### DOCKER INSTALL

Install the application via docker with the code below:

```python
docker run -p 8664:8664 spartaqube/spartaqube
```

At ths stage, the application runs locally and is accessible in your browser at http://localhost:8664

You can change the listening port 8664 to any available port you want. For instance, if you want to assign it to port 9000, you can run the following command:
```python
docker run -p 9000:8664 spartaqube/spartaqube
```

Here, the application runs locally and is accessible in your browser at http://localhost:9000


Get more information regarding the docker application at:
https://hub.docker.com/r/spartaqube/spartaqube


## Jupyter Notebook Integration

SpartaQube can be embedded within your usual Jupyter notebooks

Interact with your data with drag & drop and build your web components in few clicks

1. Import library
```python
from spartaqube import Spartaqube as Spartaqube
spartaqube_obj = Spartaqube()
```

Get your app token and run the API with a registered account:
```python
from spartaqube import Spartaqube as Spartaqube
spartaqube_obj = Spartaqube(app_token)
```

2. List available components
```python
spartaqube_obj.get_widgets()
```

3. Get a specific SpartaQube widget
```python
spartaqube_obj.get_widget("<widget_id>")
```

4. Create a new component using the interactive plot editor
```python
spartaqube_obj.iplot(variable1, variable2, ...)
```

Check out the documentation of the API at https://spartaqube.com/api for more information

