# neo4jupyter

This is a tool to visualize graph database queries from Neo4j in the Jupyter Notebook.

#### Install
`pip install neo4jupyter`

<img width="921" alt="screen shot 2016-04-15 at 13 13 33" src="https://cloud.githubusercontent.com/assets/1485056/14559854/e2bca15a-030b-11e6-9b8f-9858143e4e40.png">


#### Docs

```python
import neo4jupyter
neo4jupyter.init_notebook_mode()
neo4jupyter.draw(graph_object_py2neo, {"Nodes_type": "Att", …})
```

#### Licence
The MIT License (MIT) | See LICENSE.md
Copyright (c) 2015, 2016 Gabi de Maeztu