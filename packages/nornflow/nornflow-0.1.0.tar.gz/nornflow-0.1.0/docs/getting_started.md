# Getting Started with NornFlow

## Installation

You can install NornFlow in a number of ways.

### Using pip

```sh
pip install nornflow
```


### Using poetry

```sh
poetry add nornflow
```


### Using uv

```sh
uv pip install nornflow
```

or

```sh
uv add nornflow
```

> Note: From a development point of view, NornFlow uses uv for dependency and environment management.

## Basic Usage
Once `nornflow` has been installed in your environment, you can do:

```shell
 $nornflow init
+----------------------------------------------------------------------------+
| The 'init' command creates directories, and samples for configs, tasks and |
| workflows files, all with default values that you can modify as desired.   |
| No customization of 'init' parameters available yet.                       |
|                                                                            |
| Do you want to continue?                                                   |
+----------------------------------------------------------------------------+
Do you want to continue? [Y/n]:
```

> *As of now, `nornflow init` just attempts to create minimal assets required by NornFlow, including a 'nornflow.yaml' file, as well as a 'tasks' and 'workflows' folders in the same directory where the command was ran.  
> If files and/or directories with the same names already exist, they are just skipped.  
> If created by the init CLI, the 'tasks' and 'worlflows' folders will also contain some sample files in them.*

Assuming the user chooses to continue, if the following output appears, it means NornFlow was successfully initialzed in the directory:
```shell
NornFlow will be initialized at /Users/neteng
Created directory: /Users/netauto/nornir_configs
Created a sample 'nornir_configs' directory: /Users/netauto/nornir_configs
Created a sample 'nornflow.yaml': /Users/netauto/nornflow.yaml
Created directory: /Users/netauto/tasks
Created a sample 'hello_world' task: /Users/netauto/tasks/hello_world.py
Created directory: /Users/netauto/workflows
Created a sample 'hello_world' workflow: /Users/netauto/workflows/hello_world.yaml


          NORNFLOW SETTINGS
╭──────────────────────┬────────────────────────────╮
│       Setting        │ Value                      │
├──────────────────────┼────────────────────────────┤
│  nornir_config_file  │ nornir_configs/config.yaml │
├──────────────────────┼────────────────────────────┤
│   local_tasks_dirs   │ ['tasks']                  │
├──────────────────────┼────────────────────────────┤
│ local_workflows_dirs │ ['workflows']              │
├──────────────────────┼────────────────────────────┤
│  imported_packages   │ []                         │
├──────────────────────┼────────────────────────────┤
│       dry_run        │ False                      │
╰──────────────────────┴────────────────────────────╯


                             TASKS CATALOG
╭─────────────┬───────────────────┬─────────────────────────────────────╮
│  Task Name  │ Description       │ Location                            │
├─────────────┼───────────────────┼─────────────────────────────────────┤
│ hello_world │ Hello World task. │ /Users/netauto/tasks/hello_world.py │
╰─────────────┴───────────────────┴─────────────────────────────────────╯


                          WORKFLOWS CATALOG
╭──────────────────┬───────────────────────────────────┬────────────────────────────╮
│  Workflow Name   │ Description                       │ Location                   │
├──────────────────┼───────────────────────────────────┼────────────────────────────┤
│ hello_world.yaml │ A simple workflow that just works │ workflows/hello_world.yaml │
╰──────────────────┴───────────────────────────────────┴────────────────────────────╯
```

Notice the files and folders the `norflow init` command created:
- `nornflow.yaml` file: Contains the settings that dictate NornFlow's behaviors and where it should look for Nornir Tasks and Worflows to include in it's 'catalog'. The output exihibts the contents of this file in the `NORNFLOW SETTINGS` table. You can check the contents of this file [here](../nornflow/cli/samples/nornflow.yaml).
- `nornir_configs` folder: Contains Nornir .yaml files with trivial configs employing Nornir's 'SimpleInventory', a single host and group for the localhost (127.0.0.1), as well as fake credentials for login. Evidently, for most real-world scenarios, these files will have to be reworked. You can check how those files will look like [here](../nornflow/cli/samples/nornir_configs/).
- `tasks` folder: Contains a single `hello_world.py` file in it, which in turn contains a sigle 'hello_world' Nornir Task defined in it. Check it [here](../nornflow/cli/samples/hello_world.py).
- `workflows` folder: Contains a single `hellow_world.yaml` 

Nornflow relies on its settings file to work properly. All madatory and optional settings are explained in the [Configurations](./configurations.md) section.