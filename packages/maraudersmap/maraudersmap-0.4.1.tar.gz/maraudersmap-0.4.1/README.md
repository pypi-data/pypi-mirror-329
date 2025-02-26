
![splash](visualgrep.png)
**A visual "grep" of mmap. This is a large HPC Fortran solver codebase. Each function/subroutine is a circle, size proportional to the number os lines of code, aggregated in files, then folders. If the function contains a pragma "$!ACC", the circle is shown in red. The whole figure shows what parts of the code ported to GPU using OpenACC pragmas**

![splash2](callgraph.png)
**Global callgraph of a large HPC code, using the pyvis backend and a barnes-hut layout algorithm. The large inner structures of the code are emerging. In red, the NUMERICS parts, in blue the Lagrangian solver, in Green the boundary conditions.**


# Marauder's map

## About

Marauder's map is a python helper tool to create visual representations of the internal structure of python and Fortran packages.
Just like Harry Potter's Marauder's map, which can be asked different things and will adapt its response to the request, the Marauder's map is an automated solution developed to study software geography.

The online documentation is available on [the internal Cerfacs forge](http://opentea.pg.cerfacs.fr/maraudersmap/) (Credentials needed). Soon the package will be updated on Pypi with documentation on readthedocs.


---

## Installation

This is an open-source python package available on the Cerfacs Gitlab Forge [here](https://gitlab.com/cerfacs/maraudersmap.)
Soon, it will be released on Pypi.


## Basic usage:

The installation add the command `mmap` to your terminal:

```
>mmap
Usage: mmap [OPTIONS] COMMAND [ARGS]...

  Package maraudersmap v0.0.0

  ---------------    Marauders map  --------------------

      You are now using the Command line interface of Marauders map package,
      a set of tools created at CERFACS (https://cerfacs.fr). It creates
      callgraphs for python and fortran projects.

      This is a python package currently installed in your python environment.

      Usage: For all static callgraphs, use `>mmap anew` before others
      commands to create your project.     Then use `>mmap
      imports/cgstat/cgstat_ftn` to generate a JSON file storong the
      callgraph.     Finally use `>mmap show mycallgraph.json` to visualize
      your data.      The mmap.yml input file is the same for all commands, to
      ensure homogeneity btw analysis.

      For the python dynamic callgraph use >mmap `cgdyn --new` to create your
      monitoring function.

      Free ad.: if you just want to scan a Python module structure, try :
      https://pypi.org/project/code2flow/. Awsom' stuff.

Options:
  --help  Show this message and exit.

Commands:
  anew        Create a default input file.
  cgdyn       Python : dynamic callgraph from the eXecution of a function.
  cgstat      Python : static callgraph - all functions and methods.
  cgstat-ftn  Fortran: static callgraph - all functions and subroutines.
  imports     Python : static callgraph of modules - only imports.
  show        Visualize mmap callgraphs stored in a JSON_DATA file
```

Now, write the following command to create a default .yml input file that you will then edit. This is the starting point of using Marauder's map.

```
mmap anew
````

An input file has been created: *mmap_in.yml* which looks like this: 


```yaml
# the path where your sources are stored
path : /Users/desplats/TEST/flinter/Gitlab/Nek5000/core.py
# name of the package
package: Nek5000

# blacklist of unwanted nodes in the graph
remove_patterns :
  - "matplotlib*"
  - "numpy*"
  - "tkinter*"
  - "json*"
  - "PIL*"

soften_patterns :
  - "*BaseForm*"

# If rules is selected, then color_rules will be applied, otherwise chose size or ccn for example
color_by: "ccn"

# coloring rules to apply (last color prevail)
color_rules :
  acquisition_canvas: "#EEEEBB"
  utils: "grey"
  constants: "grey"
  base_canvas_object: "#EE8866"
  popups: "#222255"
  forms: "#77AADD"

###########################################################
# Static graphs
showparents: False      # add missing parent nodes
remove_hyperconnect: 5 #remove leaves with more than 5 parents

"mmap_in.yml" 34L, 840B
```

You need to edit the path towards your sources, name the package, and set the "colored_by" option to either "ccn" (coloration by complexity), "size" (coloration by size, in number of lines), or "rules" (customized coloration, with the rules to edit under). 


Free ad.: if you just want to scan a Python module structure, try : https://pypi.org/project/code2flow/. Aw som' stuff.
    

## Complete workflow

Here follows the data flow of marauder's map command, showing you all the possibilities at hand.
 

```bash
                            mmap_in.yml
                                 |
                                 |
                                 |
              +------------------+-----------+-----------+--------+
              |                              |           |        |
              |                         +----+---+       |        |
              |                         |treefile|       |        |
              |                         +----+---+       |    +---v---+
         +----+---+                          |           |    |imports|
         |treefunc|                          v           |    +---+---+
         +----+---+                    file_tree.json    |        |
              |                              |           |        v
              |                              |           |import_graphs.js
              v                              |           |   |    |
       func_tree.json-------------------+---|||------+   |   |    |
              |                         |    |       |   |   |    |
              |                         |    |       |   |   |    |
              |                         |    |      +v---v---v+   |
              |          +------------+ |    |      |callgraph|   |
              |          |regexp-input| |    |      +----+----+   |
              |          +-------+----+ |    |           |        |
              |                  |      |    |           |        |
+------+      |        +-----+   v      |    |           |        |
| grep <------+-------->score<-rules.yml|    |           |        |
+---+--+               +--+--+          |    |           |        |
    |                     |             |    |           v        |
    |        score<-------+             |    |    callgraph.json  |
    v                     |             |    |              |     |
graphical        stats<---+             |    |              |     |
 output                   |             |    |              |     |
                          v             |    |              |     |
                func_tree_score.json    |    |              |     |
                          |      +------+    |              |     |
                          +---+  |           |            +-v-----v-+
                              |  |  +--------+            |showgraph|
                              |  |  |                     +----+----+
                             +v--v--v-+                        |
                             |showtree|                        v
                             +---+----+                     graphical
                                 |                           output
                                 v
                              graphical
                               output
```


## Acknowledgements

Marauder's Map is a service created thanks to the [EXCELLERAT Center Of Excellence](https://www.excellerat.eu/wp/) (drifting from the flinter service). and is continued as part of the [EXCELLERAT P2 Center Of Excellence](https://www.excellerat.eu/).

It is also feeded by the community of the [COEC Center Of Excellence](https://coec-project.eu/). These projects ware funded by the European community.

![logo](https://www.excellerat.eu/wp-content/uploads/2020/04/excellerat_logo.png)
![logo](https://www.excellerat.eu/wp-content/uploads/2023/01/EXCELLERAT-P2_Logo.png)
![logo](https://www.hpccoe.eu/wp-content/uploads/2020/10/cnmlcLiO_400x400-e1604915314500-300x187.jpg)
