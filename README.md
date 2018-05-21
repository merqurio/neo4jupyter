# neo4jupyter

A tool to visualize graph database queries from Neo4j in the Jupyter Notebook.

#### Install
`pip install neo4jupyter`

<img width="921" alt="screen shot 2016-04-15 at 13 13 33" src="https://cloud.githubusercontent.com/assets/1485056/14559854/e2bca15a-030b-11e6-9b8f-9858143e4e40.png">


#### Docs

First thing you must do is call the `neo4jupyter.init_notebook_mode()` to load all the javascript.

```python
import neo4jupyter
neo4jupyter.init_notebook_mode()
```

Drawing a graph it's as easy as giving the funcion `neo4jupyter.draw()` the [py2neo](http://py2neo.org/v3/) graph object and the parameters that you want to be displayed. An example of the settings for the [movie graph tutorial](https://neo4j.com/developer/example-project/), `options = {"Movie": "title", "Person": "name"}` will show the nodes `Person` and `Movie` by title and name consecutively and their connexions.

```python
neo4jupyter.draw(graph_object_py2neo, {"Nodes_type": "Att", …})
```

I encourage you to read the [neo4jupyter.py](https://github.com/merqurio/neo4jupyter/blob/master/neo4jupyter.py) file, is small and subject to be enhanced.

#### Licence
The MIT License (MIT) | See LICENSE.md
Copyright (c) 2015, 2016, 2017, 2018 Gabriel de Maeztu, Marcus Rehm, Bruce Lowther
