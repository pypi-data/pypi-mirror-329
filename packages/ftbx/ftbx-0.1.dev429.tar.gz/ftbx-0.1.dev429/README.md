# FTBX - FLEX TOOLBOX

Just trying to make flex operations faster for all teams.

## Table of Contents

  - [Requirements](#requirements)  
  - [Installation](#installation)  
    - [Windows](#windows)  
    - [Linux](#linux)  
    - [macOS](#macos)
  - [Usage](#usage)
    - [ftbx update](#update)
    - [ftbx connect](#connect)  
    - [ftbx setup](#setup)
    - [ftbx query](#query)  
    - [ftbx list](#list)  
    - [ftbx pull](#pull)  
    - [ftbx create](#create)
    - [ftbx push](#push)  
    - [ftbx fail](#fail)
    - [ftbx restore](#restore)  
    - [ftbx compare](#compare)  
    - [ftbx assert](#assert)
    - [ftbx retry](#retry)  
    - [ftbx cancel](#cancel)
    - [ftbx launch](#launch)  
    - [ftbx workflowDesigner](#workflow-designer)
    - [ftbx metadataDesigner](#metadata-designer)
  - [Errors & fixes](#errors-fixes)  
    - [SSLCertVerificationError](#self-signed-certificates)  
  - [Contact](#contacts)  

## __Bug/Feature Bounty Hunters__

| Bounty Hunter          | Bugs found | Features suggested | PR merged | Bounties |
|------------------------|------------|--------------------|-----------|----------|
| **Elouan GOUINGUENET** | 1          | 5                  | 2         | 8        |
| **Gustavo BONASSO**    | 4          | 1                  | 2         | 7        |
| **Hugo TALBOT**        | 0          | 1                  | 3         | 4        |
| **Guillaume GAY**      | 1          | 2                  | 0         | 3        |
| **Bowen ZHANG**        | 1          | 0                  | 0         | 1        |
| **Julius SANTUA**      | 0          | 1                  | 0         | 1        |
| **Rémi MARCHAND**      | 1          | 0                  | 0         | 1        |
| **Julien PENVEN**      | 0          | 1                  | 0         | 1        |
| **TOTAL**              | **8**      | **11**             | **7**     | **26**   |

> See HUNT.md for full history

# REQUIREMENTS <a name="requirements"></a>

#### [Git (click here to download)](https://git-scm.com/downloads)

#### [Python 3.10 (click here to download)](https://www.python.org/downloads/release/python-31011/)

***

# INSTALLATION <a name="installation"></a>

## Install python

#### Windows <a name="windows"></a>

* link above

#### Linux <a name="linux"></a>

```shell
sudo apt install pipx
pipx ensurepath # verify pipx is in PATH
```

#### macOS <a name="macos"></a>

```shell
brew install pipx
pipx ensurepath # verify pipx is in PATH
```

## Install FTBX

```shell
pipx install ftbx
ftbx init
```

## Configure autocompletion

```shell
ftbx --install-completion
```

Then open a new terminal and you will get autocompletions by pressing 'tab'.

## Update FTBX

```shell
ftbx update
```
or 

```shell
pipx install ftbx --upgrade
```

# USAGE <a name="usage"></a>

You can use the flag `--help` with any command to show the command arguments (see below).  

```shell
$ ftbx --help
                                                                                                                               
 Usage: ftbx COMMAND [ARGS] [OPTIONS]...                                                                                    
                                                                                                                               
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                     │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.              │
│ --help                        Show this message and exit.                                                                   │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ assert             Asserts some statement(s) or condition(s). Returns 'True' or 'False'.                                    │
│ compare            Compares objects between environments. Saves the result(s) in 'compare_env1_env2/'.                      │
│ connect            Connects to an environment. Environment file is located at '~/.ftbx/environments'.                       │
│ create             Creates templated objects in an environment.                                                             │
│ env                Displays all available environments and their urls, aliases, versions and usernames.                     │
│ fail               Fail object instances (requirements: connection to the servers and `consul_host`/`consul_token`)         │
│ init               Initializes the flex-toolbox. This is the first command you must run upon installation.                  │
│ launch             Launches a job or workflow with the given parameters.                                                    │
│ list               Lists objects from an environment. Saves the results as CSV and JSON files in 'lists/'.                  │
│ metadataDesigner   Opens the metadata designer in your default web browser.                                                 │
│ pull               Pulls objects from environment(s) as files and folders.                                                  │
│ push               Creates or updates objects in one of multiple environments. Generates backups before pushing.            │
│ query              Queries an environment, useful as postman replacement. Saves the results in 'query.json'.                │
│ restore            Restores objects to a previous point in time.                                                            │
│ retry              Retries object instances in an environment either from API filters or from a file (csv or json).         │
│ setup              Setup the API documentation (in 'docs/') and the SDK (in 'sdks/') for a given flex version.              │
│ update             Updates the toolbox to the latest version.                                                               │
│ workflowDesigner   Opens the workflow designer for a given workflow in an environment.                                      │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

```shell
$ ftbx retry --help
                                                                                                                               
 Usage: ftbx retry OBJECT_TYPE [OPTIONS]                                                                   
                                                                                                                               
 Retries object instances in an environment either from API filters or from a file (csv or json).                              
 - ftbx retry jobs --in cs-sbx # retry all failed jobs                                                                         
 - ftbx retry jobs --filters 'name=ftbx-script' 'createdFrom=22 Jul 2024'                                                      
 - ftbx retry workflows --file 'lists/failed_workflows.csv' --in cs-sbx                                                        
                                                                                                                               
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    object_type      OBJECT_TYPE:{jobs|workflows}  [default: None] [required]                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --in             TEXT  [default: default]                                                                                   │
│ --filters        TEXT  ex: 'name=ftbx-script' 'createdFrom=22 Jul 2024'                                                     │
│ --file           TEXT  ex: 'lists/failed_jobs.csv' 'lists/failed_jobs.json' (from 'ftbx list') [default: None]              │
│ --help                 Show this message and exit.                                                                          │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

# Update <a name="update"></a>

```shell
$ ftbx update
```

This command fetches the latest version of the toolbox.

# Connect <a name="connect"></a>

```shell
$ ftbx connect --help
                                                                                                                               
 Usage: ftbx connect ENV_OR_URL [USERNAME] [PASSWORD] [OPTIONS]                                                             
                                                                                                                               
 Connects to an environment. Environment file is located at '~/.ftbx/environments'.                                            
 - ftbx connect 'https://sandbox.flex.support.dalet.cloud' my_user --alias cs-sbx --version 2024.5.0  # first time             
 - ftbx connect cs-sbx  # once you successfully connected                                                                      
                                                                                                                               
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    env_or_url      TEXT        ex: https://sandbox.flex.support.dalet.cloud [default: None] [required]                    │
│      username        [USERNAME]  [default: None]                                                                            │
│      password        [PASSWORD]  [default: None]                                                                            │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --alias          TEXT  ex: cs-sbx, wb-prod [default: None]                                                                  │
│ --version        TEXT  ex: 2022.5.7, 2024.4.5 [default: latest]                                                             │
│ --help                 Show this message and exit.                                                                          │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

> Note: If you're looking for how to connect to self-signed environments, see [here](#4-connect-to-self-signed-environments).

---

#### 1. Connect to a new environment

```shell
# connect without showing password (will prompt you to input password and hide characters)
ftbx connect "https://devstaging.flex.daletdemos.com" "username" --alias "devstaging" --version "2022.5.7"

# connect with plain password
ftbx connect "https://devstaging.flex.daletdemos.com" "username" "my_password" --alias "devstaging"
```

---

#### 2. Connect to a known environment (must be in `~/.ftbx/environments`)

```shell
ftbx connect "devstaging"

ftbx connect "cs-sbx"
```

---

#### 3. Display available default environments

```shell
ftbx env
```

```shell
DEFAULT       ALIAS       VERSION                          URL                             USERNAME  
   -           ae-preprod   latest           https://master.preprod.flex.aenetworks.com    masteruser
   -              ae-prod   latest                   https://master.flex.aenetworks.com    masteruser
   -           crown-prod   latest                 https://master.crownmedia.ooflex.net    masteruser
   -    cs-sandbox-master   latest           https://master.flex.support.cs.dalet.cloud    masteruser
   X               cs-sbx   latest          https://sandbox.flex.support.cs.dalet.cloud       dnaisse
   -              fm-prod   latest                 https://master.firstmedia.ooflex.net    masteruser
   -             hbo-prod   latest                        https://master.hbo.ooflex.net    masteruser
   -               hm-dev   latest https://development.flex-dev.cloud.hallmarkmedia.com       dnaisse
   -              hm-prod   latest https://production.flex-prod.cloud.hallmarkmedia.com       dnaisse
   -             ioc-prod   latest                   https://cio.images-mam.olympic.org dalet_support
   -             mbn-prod   latest                     https://master.flex.mbn-news.com    masteruser
   -             mse-prod   latest             https://master.prod.monumentalsports.com    masteruser
   -            pbsd-prod   latest                         https://master.colo.pbsd.org    masteruser
   -         peloton-prod   latest                      https://prod.mam.onepeloton.com       dnaisse
   -               wb-dev 2022.5.8            https://portal.dev.archive.warnerbros.com       dnaisse
   -              wb-prod 2022.5.7                 https://vault.archive.warnerbros.com       dnaisse
   -               wb-stg 2022.5.7             https://vault.stg.archive.warnerbros.com       dnaisse
```

#### 4. Connect to self-signed environments

Environments deployed with a self-signed certificate are not trusted by default. In order to trust this certification authority, set the environment variable `REQUESTS_CA_BUNDLE` to the path to the certificate of the root certification authority. Like:

```shell
# POSIX
export REQUESTS_CA_BUNDLE=/path/to/cert

# Windows - PowerShell
Set-Item Env:REQUESTS_CA_BUNDLE "path\to\cert"
```

#### Download Flex root certificate authority certificate

This can be done with most web browser. But here is a command for POSIX system.

```shell
echo quit | openssl s_client -showcerts -servername "devstaging.flex.daletdemos.com" -connect devstaging.flex.daletdemos.com:443 > cacert.pem
```

# Setup <a name="setup"></a>

```shell
$ ftbx setup --help
                                                                                                                               
 Usage: ftbx setup [OPTIONS]                                                                                                
                                                                                                                               
 Setups the API documentation (in 'docs/') and the SDK (in 'sdks/') for a given flex version.                                  
 - ftbx setup --version latest                                                                                                           
 - ftbx setup --version 2022.5.7                                                                                                         
                                                                                                                               
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version        TEXT  [default: latest]                                                                                    │
│ --help                 Show this message and exit.                                                                          │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

> Note: you have to be connected to the `dlt-fw-uk-UDP4-1120-full-config` VPN to be able to retrieve the SDK.

---

#### 1. Setup

```shell
# 2022.5.7
ftbx setup --version "2022.5.7"

# latest
ftbx setup --version "latest"
```

# Query <a name="query"></a> 

```shell
$ ftbx query --help
                                                                                                                                                                                                                   
 Usage: ftbx query METHOD URL [OPTIONS]                                                                                                                                                   
                                                                                                                                                                                                                   
 Queries an environment, useful as postman replacement. Saves the results in 'query.json'.                                                                                                                         
 - ftbx query GET 'assets/12345/annotations'                                                                                                                                                                         
 - ftbx query POST 'actions/3332/actions' --payload 'action=disable'  # disable an action                                                                                                                            
 - ftbx query GET 'collections' --from 'cs-sbx'                                                                                                                                                                        
                                                                                                                                                                                                                   
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    method      METHOD:{GET|PATCH|POST|PUT|DELETE}  [default: None] [required]                                                                                                                                 │
│ *    url         TEXT                          ex: 'assets/1234/annotations' 'actions/3332/configuration' [default: None] [required]                                                                            │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --from                      TEXT  [default: default]                                                                                                                                                            │
│ --payload                   TEXT  ex: 'action=enable' 'action=disable' or 'payload.json'                                                                                                                        │
│ --stdout     --no-stdout          Whether to display the result in the terminal [default: no-stdout]                                                                                                            │
│ --help                            Show this message and exit.                                                                                                                                                   │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

#### 1. Query absolutely everything

```shell
# GET
ftbx query GET "actions/410"
# Env alias
ftbx query GET "actions/410" --from "cs-sbx"
# Print query response to terminal
ftbx query GET "actions/410" --stdout

# POST/PUT (same args as above, plus --payload)
ftbx query PUT "actions/410/configuration" --payload "payload.json"

# Cancel a failed job with command line arguments
ftbx query POST "jobs/1213/actions" --payload "action=cancel"
```

# List <a name="list"></a>

```shell
$ ftbx list --help
                                                                                                                                                                                                                   
 Usage: ftbx list OBJECT_TYPE [OPTIONS]                                                                                                                                                            
                                                                                                                                                                                                                   
 Lists objects from an environment. Saves the results as CSV and JSON files in 'lists/'.                                                                                                                           
 - ftbx list actions  # list all actions                                                                                                                                                                           
 - ftbx list jobs --filters 'status=Failed' 'name=ftbx-script' --from 'cs-sbx' --name 'failed_cs-sbx_jobs'                                                                                                               
 - ftbx list actions --post-filters 'concurrentJobsLimit>0' --from 'cs-sbx'  # all actions with concurrency > 0                                                                                                      
 - ftbx list assets --filters 'fql=(name~PACKAGE and deleted=false)' --name 'live_packages'  # using fql                                                                                                           
                                                                                                                                                                                                                   
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    object_type      OBJECT_TYPE:{accounts|actions|assets|collections|eventHandlers|events|groups|jobs|messageTe  [default: None] [required]                                                                   │
│                       mplates|metadataDefinitions|objectTypes|profiles|quotas|resources|roles|tagCollections|task                                                                                               │
│                       Definitions|tasks|taxonomies|timedActions|userDefinedObjectTypes|users|variants|wizards|wor                                                                                               │
│                       kflowDefinitions|workflows|workspaces}                                                                                                                                                    │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --filters             TEXT    ex: 'status=Running' 'name=asset_name'                                                                                                                                              │
│ --post-filters        TEXT    ex: 'configuration.instance.execution-lock-type=NONE' 'concurrentJobsLimit>0'                                                                                                       │
│ --from                TEXT    [default: default]                                                                                                                                                                  │
│ --from-csv            TEXT    ex: 'lists/asset_list.csv' [default: None]                                                                                                                                          │
│ --name                TEXT    Name under which the JSON and CSV files should be saved [default: None]                                                                                                             │
│ --batch-size          INTEGER The batch size for the API number of results [default: None]                                                                                                                        │
│ --help                        Show this message and exit.                                                                                                                                                         │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

#### 1. List anything

  ```shell
  # List all actions 
  ftbx list actions

  # List all assets with fql in the default env
  ftbx list assets --filters "fql=(mimetype~mp4)" --name "mp4Assets"

  # List all assets with fql from wb-stg
  ftbx list assets --filters "fql=(mimetype~mp4)" --name "mp4Assets" --from wb-dev
  
  # List 5 jobs in a failed status 
  ftbx list jobs --filters "status=Failed" "limit=5" --name "failedJobs"
  
  # List scripts that contains "createJob"
  ftbx list actions --filters "type=script" --post-filters "configuration.instance[text]~createJob"
  
  # List jobs for which the last (-1) history message is an error message containing "getName()" in its stackTrace
  ftbx list jobs --filters "name=basic-long-running-action" --post-filters "history.events[-1].stackTrace~getName()"
  
  # List all actions with concurrency > 0 from default env
  ftbx list actions --post-filters "concurrentJobsLimit>0" --name "jobsWithConcurrentLimit"

  # List workflows that completed, and get some metadata fields from the asset the workflow was on
  ftbx list workflows --filters "name=my_workflow" "status=Completed" --post-filters "asset.metadata.instance.general-info.sha1!=None" "asset.fileInformation.currentLocation!=None"
  
  # List all workflows in a corrupted state
  ftbx list workflows --filters "status=Running" --post-filters "jobs.jobs[-1].status!=Running"

  # List events of type 'Login Failed' from April 1, 2024 to May 14, 2024
  ftbx list events --filters "eventType=Login Failed" "from=01 Apr 2024" "to=14 May 2024"
  
  # List account properties
  ftbx list accountProperties --from "cs-sbx"
  ```
  
> Note: FQL search has a max number of results of 10 000, so if you need any more than that, you will have to split your FQL search in multiples other ones.

# Pull <a name="pull"></a>

```shell
$ ftbx pull --help
                                                                                                                                                                                                                   
 Usage: ftbx pull OBJECT_TYPE [OPTIONS]                                                                                                                                                         
                                                                                                                                                                                                                   
 Pulls objects from environment(s) as files and folders.                                                                                                                                                           
 - ftbx pull jobs 12345 --from 'cs-sbx'  # pull job 12345
 - ftbx pull all --from 'wb-dev' 'wb-stg' 'wb-prod' # pull every config objects                                                                                                                                          
 - ftbx pull actions  # pull all actions                                                                                                                                                                           
 - ftbx pull workflowDefinitions --filters 'name=ftbx-workflow' --from 'cs-sbx' --with-dependencies                                                                                                                    
 - ftbx pull workflowDefinitions ftbx-workflow --from 'cs-sbx' --with-dependencies  # same as above
                                                                                                                                                                                                                   
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    object_type            OBJECT_TYPE:{all|accounts|actions|assets|collections|eventHandlers|e  [default: None] [required]                                           │
│                             vents|groups|jobs|messageTemplates|metadataDefinitions|objectTypes|p                                                                       │
│                             rofiles|quotas|resources|roles|tagCollections|taskDefinitions|tasks|                                                                       │
│                             taxonomies|timedActions|userDefinedObjectTypes|users|variants|wizard                                                                       │
│                             s|workflowDefinitions|workflows|workspaces}                                                                                                │
│      object_name_or_id      [OBJECT_NAME_OR_ID]                                                   [default: None]                                                      │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --filters                                        TEXT  ex: 'status=Running' 'name=asset_name'                                                                          │
│ --post-filters                                   TEXT  ex: 'configuration.instance.execution-lock-type=NONE' 'concurrentJobsLimit>0'                                   │
│ --from                                           TEXT  [default: default]                                                                                              │
│ --with-dependencies    --without-dependencies          Whether to also pull the objects dependencies [default: without-dependencies]                                   │
│ --help                                                 Show this message and exit.                                                                                     │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

#### 1. Pull anything

```shell
# Pull **ALL** actions
ftbx pull actions # default env
ftbx pull actions --from "wb-stg"

# Pull actions matching filters
ftbx pull actions --filters "name=set-asset-metadata" --from "wb-stg"
ftbx pull actions --filters "id=309" # default env
ftbx pull actions --filters "enabled=true" # default env
ftbx pull actions --filters "type=script" --from "wb-stg"
ftbx pull actions --filters "type=script" "enabled=true" # default env

# Pull **ALL**
ftbx pull all
ftbx pull all --from "wb-stg"

# Pull env actions with dependencies
ftbx pull actions --with-dependencies # default env

# Pull all actions where script contains "context.asset.id"
ftbx pull actions --post-filters "configuration.instance[text]~context.asset.id"

# Pull workflow definitions with dependencies
ftbx pull workflowDefinitions --filters "name=ingest-workflow" --with-dependencies

# Pull actions from several envs at the same time
ftbx pull actions --from "wb-dev" "wb-stg" "wb-prod" --filters "name=set-asset-metadata"

# Pull account properties
ftbx pull accountProperties --from "cs-sbx"
```

# Create <a name="create"></a>

```shell
$ ftbx create --help
                                                                                                                                                                                                                   
 Usage: ftbx create OBJECT_TYPE PLUGIN OBJECT_NAME [OPTIONS]                                                                                                                                                                                
                                                                                                                                                                                                                   
 Creates templated objects in an environment.                                                                                                                                                                      
 - ftbx create actions script 'my-script' --in cs-sbx                                                                                                                                                              
 - ftbx create actions decision 'my-decision' --in cs-sbx                                                                                                                                                          
 - ftbx create wizards launchWorkflow 'my-launch-workflow-wizard' --in cs-sbx                                                                                                                                      
 - ftbx create accountProperties default 'my-account-property' --in cs-sbx                                                                                                                                      
                                                                                                                                                                                                                   
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    object_type      OBJECT_TYPE:{accountProperties|actions|wizards}  [default: None] [required]                                                                                                               │
│ *    plugin           PLUGIN:{default|decision|script|launchWorkflow}  [default: None] [required]                                                                                                               │
│ *    object_name      TEXT                                             [default: None] [required]                                                                                                               │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --in          TEXT  [default: default]                                                                                                                                                                          │
│ --help              Show this message and exit.                                                                                                                                                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

#### 1. Create items

```shell
# Create a script action in default environment
ftbx create actions script "set-asset-metadata"

# Create a script action in a specific environment
ftbx create actions script "set-asset-metadata" --in "wb-stg"

# Create a decision action 
ftbx create actions decision "check-asset-status" --in "wb-stg"

# Create a launchWorkflow wizard
ftbx create wizards launchWorkflow "launch-my-workflow"
```

# Push <a name="push"></a>

```shell
$ ftbx push --help
                                                                                                                                                                                                                   
 Usage: ftbx push OBJECT_TYPE OBJECT_NAMES... [OPTIONS]                                                                                                                                             
                                                                                                                                                                                                                   
 Creates or updates objects in one or multiple environments. Generates backups before pushing.                                                                                                                     
 - ftbx push actions 'ftbx-script' --push-to-failed-jobs 'all'  # update action and push to all failed jobs                                                                                                                  
 - ftbx push actions 'ftbx-script' 'ftbx-decision'  # update two actions                                                                                                                                           
 - ftbx push actions 'ftbx-script' --from 'wb-dev' --to 'wb-stg' 'wb-prod'  # create action in stg and prod                                                                                                        
 - ftbx push workflowDefinitions 'ftbx-workflow' --from 'wb-dev' --to 'wb-stg' --with-dependencies  # with dependencies                                                                                            
                                                                                                                                                                                                                   
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    object_type       OBJECT_TYPE:{accounts|actions|assets|eventHandlers|groups|jobs|messageTemplates|metadataDef  [default: None] [required]                                                                  │
│                        initions|profiles|quotas|resources|roles|taskDefinitions|tasks|timedActions|userDefinedObje                                                                                              │
│                        ctTypes|users|variants|wizards|workflowDefinitions|workflows|workspaces}                                                                                                                 │
│ *    object_names      OBJECT_NAMES...                                                                              [default: None] [required]                                                                  │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --from                                             TEXT  [default: default]                                                                                                                                     │
│ --to                                               TEXT  [default: default]                                                                                                                                     │
│ --retry                  --no-retry                      Whether to also retry the given job [default: no-retry]                                                                                                │
│ --listen                 --no-listen                     Whether to get the logs of the job in the terminal [default: no-listen]                                                                                │
│ --push-to-failed-jobs                              TEXT  'all' OR csv file containing failed jobs to push the config to and retry (from 'ftbx list') [default: None]                                            │
│ --with-dependencies      --without-dependencies          Whether to also push the objects dependencies [default: without-dependencies]                                                                          │
│ --help                                                   Show this message and exit.                                                                                                                            │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

#### 1. Push anything

```shell
# Push action to an env
ftbx push actions check-end-node-wf # from default env to default env

# Push job and retry it (yes, you can pull jobs directly and tweak their code in your IDE)
ftbx push jobs 294036 --retry

# Push job, retry it but also LISTEN to it (logs will appear in your terminal)
ftbx push jobs 294036 --retry --listen

# Push updated action to **ALL** corresponding failed jobs and retry them
ftbx push actions "check-end-node-wf" --push-to-failed-jobs "all"

# Push updated action to failed jobs contained in .CSV or .JSON and retry them
ftbx push actions "check-end-node-wf" --push-to-failed-jobs "failed_jobs.csv"
ftbx push actions "check-end-node-wf" --push-to-failed-jobs "failed_jobs.json"

# LIST + PUSH with RETRY flow: push & retry failed jobs created after given date
ftbx list jobs --filters "name=check-end-node-wf" "createdFrom=20 Dec 2023"
ftbx push actions "check-end-node-wf" --push-to-failed-jobs "list.json"
ftbx push actions "check-end-node-wf" --push-to-failed-jobs "list.csv"

# Push (create, or update) action from wb-dev to wb-stg AND wb-prod (yes)
ftbx push actions "set-asset-metadata" --from "wb-dev" --to "wb-stg" "wb-prod"  

# Push/update workflow definition WITHOUT updating the resources configuration
ftbx push workflowDefinitions "Get Or Compute Asset Checksum" --from "templates" --to "cs-sandbox-ovh-flex-config" --with-dependencies

# Push workflow definition with ALL its dependencies (actions, resources...)
ftbx push workflowDefinitions "Get Or Compute Asset Checksum" --from "templates" --to "cs-sandbox-ovh-flex-config" --with-dependencies --include-resources

# Push accountProperties
ftbx push accountProperties "my-account-property"
```

# Fail <a name="fail"></a>

```shell
$ ftbx fail --help
                                                                                                                                   
 Usage: ftbx fail OBJECT_TYPE [OBJECT_IDS] [OPTIONS]...                                                                  
                                                                                                                                   
 Fail object instances (requires to be connected to the servers and `consul_host` and `consul_token` in `~/.ftbx/environments`).                                  
 - ftbx fail jobs 1234 5678 91011  # fail the 3 jobs in the default environment                                                    
 - ftbx fail jobs --from-file 'lists/failed_jobs.csv'                                                                              
 - ftbx fail jobs --from-file 'lists/failed_jobs.json'                                                                             
                                                                                                                                   
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    object_type      OBJECT_TYPE:{jobs}  [default: None] [required]                                                            │
│      object_ids       [OBJECT_IDS]...     [default: None]                                                                       │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --from-file        TEXT  ex: 'lists/failed_jobs.csv [default: None]                                                             │
│ --in               TEXT  [default: default]                                                                                     │
│ --help                   Show this message and exit.                                                                            │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

#### 1. Fail instances 

```shell
# Fail a job with id 12345
ftbx fail jobs 12345

# Fail multiple jobs
ftbx fail jobs 1234 5678 91011

# Fail jobs from file
ftbx fail jobs --from-file 'lists/failed_jobs.csv'
ftbx fail jobs --from-file 'lists/failed_jobs.json'
```

# Restore <a name="restore"></a>

```shell
$ ftbx restore --help
                                                                                                                                                                                                                   
 Usage: ftbx restore OBJECT_TYPE OBJECT_NAME BACKUP_NAME [OPTIONS]                                                                                                                                          
                                                                                                                                                                                                                   
 Restores objects to a previous point in time.                                                                                                                                                                     
 - ftbx restore actions 'ftbx-script' '2024-08-30 09h50m38s' --in 'cs-sbx'                                                                                                                                           
 - ftbx restore assets 12345 '2024-07-23 09h50m38s' --in 'cs-sbx'                                                                                                                                                    
                                                                                                                                                                                                                   
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    object_type      OBJECT_TYPE:{accounts|actions|assets|eventHandlers|groups|jobs|messageTemplates|metadataDef  [default: None] [required]                                                                   │
│                       initions|profiles|quotas|resources|roles|taskDefinitions|tasks|timedActions|userDefinedObje                                                                                               │
│                       ctTypes|users|variants|wizards|workflows|workspaces}                                                                                                                                      │
│ *    object_name      TEXT                                                                                         [default: None] [required]                                                                   │
│ *    backup_name      TEXT                                                                                         [default: None] [required]                                                                   │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --in          TEXT  [default: default]                                                                                                                                                                          │
│ --help              Show this message and exit.                                                                                                                                                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

#### 1. Restore backup (in object_type/object_name/backup)

```shell
ftbx restore actions "set-tech-metadata-dpx" "2023-10-10 15h53m43s" --in "wb-prod"
```
  
# Compare <a name="compare"></a>

```shell
$ ftbx compare --help
                                                                                                                                                                                                                   
 Usage: ftbx compare OBJECT_TYPE ENVIRONMENTS... [OPTIONS]                                                                                                                                                                          
                                                                                                                                                                                                                   
 Compares objects between environments. Saves the result(s) in 'compare_env1_env2/'.                                                                                                                               
 - ftbx compare actions 'wb-dev' 'wb-stg' 'wb-prod'  # compare all actions                                                                                                                                               
 - ftbx compare actions 'wb-dev' 'wb-stg' 'wb-prod' --filters 'name=ftbx-script'                                                                                                                                           
 - ftbx compare metadataDefinitions 'wb-stg' 'wb-prod' --filters 'name=Asset'                                                                                                                                            
                                                                                                                                                                                                                   
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    object_type       OBJECT_TYPE:{accounts|actions|eventHandlers|groups|messageTemplates|metadataDefinitions|obj  [default: None] [required]                                                                  │
│                        ectTypes|profiles|quotas|resources|roles|tagCollections|taskDefinitions|taxonomies|timedAct                                                                                              │
│                        ions|userDefinedObjectTypes|users|variants|wizards|workflowDefinitions|workspaces}                                                                                                       │
│ *    environments      ENVIRONMENTS...                                                                              [default: None] [required]                                                                  │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --filters        TEXT                                                                                                                                                                                           │
│ --help                 Show this message and exit.                                                                                                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

#### 1. Compare items

```shell
# Compare action "check-end-node-wf" between wb-dev, wb-stg and wb-prod
ftbx compare actions "wb-dev" "wb-stg" "wb-prod" --filters "name=check-end-node-wf"

# Compare **ALL** actions between wb-dev, wb-stg and wb-prod
ftbx compare actions "wb-dev" "wb-stg" "wb-prod"
```

# Assert <a name="assert"></a>

```shell
$ ftbx assert --help
                                                                                                                                                                                                                   
 Usage: ftbx.py assert OBJECT_TYPE OBJECT_NAME_OR_ID ASSERTIONS... [OPTIONS]                                                                                                                                                           
                                                                                                                                                                                                                   
 Asserts some statement(s) or condition(s). Returns 'True' or 'False'.                                                                                                                                             
 - ftbx assert assets 12345 'deleted!=True'                                                                                                                                                                        
 - ftbx assert actions ftbx-script 'concurrentJobsLimit>0'                                                                                                                                                         
 - ftbx assert actions ftbx-script 'configuration.instance.execution-lock-type=NONE'                                                                                                                               
                                                                                                                                                                                                                   
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    object_type            OBJECT_TYPE:{accounts|actions|assets|collections|eventHandlers|events|groups|jobs|messag  [default: None] [required]                                                                │
│                             eTemplates|metadataDefinitions|objectTypes|profiles|quotas|resources|roles|tagCollection                                                                                            │
│                             s|taskDefinitions|tasks|taxonomies|timedActions|userDefinedObjectTypes|users|variants|wi                                                                                            │
│                             zards|workflowDefinitions|workflows|workspaces}                                                                                                                                     │
│ *    object_name_or_id      TEXT                                                                                      [default: None] [required]                                                                │
│ *    assertions             ASSERTIONS...                                                                             operators: [!~, !=, >=, <=, ~, =, <, >] [default: None] [required]                        │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --in          TEXT  [default: default]                                                                                                                                                                          │
│ --help              Show this message and exit.                                                                                                                                                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

#### 1. Assertions

```shell
# assert asset id 12345 has metadata field 'value' set to 1 in wb-prod
ftbx assert assets 12345 'metadata.instance.value=1' --in 'wb-prod'

# assert my_action has concurrentJobsLimit set to 0 and lock = NONE
ftbx assert actions my_action "concurrentJobsLimit=0" "configuration.instance.execution-lock-type=NONE"
```

# Retry <a name="retry"></a>

```shell
$ ftbx retry --help
                                                                                                                                                                                                                   
 Usage: ftbx retry OBJECT_TYPE [OPTIONS]                                                                                                                                                       
                                                                                                                                                                                                                   
 Retries object instances in an environment either from API filters or from a file (csv or json).                                                                                                                  
 - ftbx retry jobs --in 'cs-sbx' # retry all failed jobs                                                                                                                                                             
 - ftbx retry jobs --filters 'name=ftbx-script' 'createdFrom=22 Jul 2024'                                                                                                                                          
 - ftbx retry workflows --file 'lists/failed_workflows.csv' --in 'cs-sbx'                                                                                                                                           
                                                                                                                                                                                                                   
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    object_type      OBJECT_TYPE:{jobs|workflows}  [default: None] [required]                                                                                                                                  │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --in             TEXT  [default: default]                                                                                                                                                                       │
│ --filters        TEXT  ex: 'name=ftbx-script' 'createdFrom=22 Jul 2024'                                                                                                                                         │
│ --file           TEXT  ex: 'lists/failed_jobs.csv' 'lists/failed_jobs.json' (from 'ftbx list') [default: None]                                                                                                  │
│ --help                 Show this message and exit.                                                                                                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

### 1. Retry instances

```shell
# "status=Failed" is applied by the command by default 

# retry 5 failed "untar-frames" jobs with query
ftbx retry jobs --filters "name=untar-frames" "limit=5"

# retry all failed "untar-frames" jobs
ftbx retry jobs --filters "name=untar-frames"

# retry **ALL** failed jobs/workflows
ftbx retry jobs
ftbx retry workflows

# retry all failed jobs from a CSV file (CSV file must contain the "id" column)
ftbx retry jobs --file "failed_jobs.csv"

# retry all failed workflows from a JSON file (JSON file must be made of a dict for each instance, with a "id" key within each dict)
ftbx retry workflows --file "failed_workflows.json"

# LIST + RETRY flow
ftbx list jobs --filters "status=Failed" "name=untar-frames" --name "list" # this will create a JSON and CSV file with the failed items 
ftbx retry jobs --file "lists/list.json" # same as below
ftbx retry jobs --file "lists/list.csv" # same as above
```

# Cancel <a name="cancel"></a>

```shell
ftbx cancel --help
                                                                                                                
 Usage: ftbx cancel OBJECT_TYPE:{jobs|workflows} OBJECT_NAME_OR_ID [OPTIONS]                                                                     
                                                                                                                
 Cancel **failed** object instance(s) in an environment.                                                                   
 - ftbx cancel jobs 12345 --in 'cs-sbx'  # cancel job 12345 in cs-sbx                                           
 - ftbx cancel workflows --filters 'name=my-workflow' 'limit=20' # cancel 20 workflows                          
 - ftbx cancel jobs --filters 'name=my-jobs' --post-filters 'history.events[-1].stackTrace~Row updated by       
 another transaction'                                                                                           
                                                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    object_type            OBJECT_TYPE:{jobs|workflows}  [default: None] [required]                         │
│      object_name_or_id      [OBJECT_NAME_OR_ID]           [default: None]                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --filters             TEXT  ex: 'name=asset_name', 'limit=30'                                                │
│ --post-filters        TEXT  ex: 'configuration.instance.execution-lock-type=NONE' 'concurrentJobsLimit>0'    │
│ --file                TEXT  ex: 'lists/failed_jobs.csv' 'lists/failed_jobs.json' (from 'ftbx list')          │
│                             [default: None]                                                                  │
│ --in                  TEXT  [default: default]                                                               │
│ --help                      Show this message and exit.                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

### 1. Cancel object instances

```shell
# "status=Failed" is applied by ftbx by default

# cancel 1 failed workflow
ftbx cancel workflows 121345

# cancel 5 failed "untar-frames" jobs
ftbx cancel jobs --filters 'name=untar-frames' 'limit=5'

# cancel all failed "untar-frames" jobs
ftbx cancel jobs 'untar-frames' # same as below
ftbx cancel jobs --filters 'name=untar-frames' # same as above

# cancel **ALL** failed jobs or workflow
ftbx cancel jobs
ftbx cancel workflows

# cancel all failed jobs from a CSV file (CSV file must contain the 'id' column)
ftbx cancel jobs --file 'failed_jobs.csv'

# cancel all workflows from a JSON file (JSON file must be made of a dict for each instance, with an 'id' key)
ftbx cancel workflows --file 'failed_workflows.json'

# LIST + CANCEL flow
ftbx list jobs --filters 'status=Failed' 'name=untar-frames' --name 'failed_jobs'
ftbx cancel jobs --file "lists/failed_jobs.csv"
ftbx cancel jobs --file "lists/failed_jobs.json"
```

# Launch <a name="launch"></a>

```shell
$ ftbx launch --help
                                                                                                                                                                                                                   
 Usage: ftbx launch OBJECT_TYPE OBJECT_NAME [OPTIONS]                                                                                                                                         
                                                                                                                                                                                                                   
 Launches a job or workflow with the given parameters.                                                                                                                                                             
 - ftbx launch jobs 'ftbx-script' --params 'assetId=12345' 'workspaceId=303' --in 'cs-sbx' --listen                                                                                                                   
 - ftbx launch workflows 'ftbx-workflow' --params 'assetId=12345' --in 'cs-sbx'                                                                                                                                        
 - ftbx launch jobs 'ftbx-script' --use-local --listen # push local config before launching                                                                                                                     
                                                                                                                                                                                                                   
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    object_type      OBJECT_TYPE:{jobs|workflows}  [default: None] [required]                                                                                                                                  │
│ *    object_name      TEXT                          [default: None] [required]                                                                                                                                  │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --in                             TEXT  [default: default]                                                                                                                                                       │
│ --params                         TEXT  ex: 'assetId=1234' 'workspaceId=303'                                                                                                                                     │
│ --from-file                      TEXT  ex: 'payload.json' [default: None]                                                                                                                                       │
│ --use-local    --no-use-local          Whether to push local config before launching the instance [default: no-use-local]                                                                                       │
│ --listen       --no-listen             Whether to get the logs of the launched instance in the terminal [default: no-listen]                                                                                    │
│ --help                                 Show this message and exit.                                                                                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

### 1. Launch instances

```shell
# launch a check-end-node-wf job
ftbx launch jobs "check-end-node-wf"

# launch a check-end-node-wf job in wb-dev
ftbx launch jobs "check-end-node-wf" --in "wb-dev"

# launch and listen to a check-end-node-wf in wb-dev
ftbx launch jobs "check-end-node-wf" --in "wb-dev" --listen

# launch a check-end-node-wf on asset id 809, in workspace id 303
ftbx launch jobs "check-end-node-wf" --params "assetId=809" "workspaceId=303"

# launch a check-end-node-wf on asset id 809 from file launch_config.json
# launch_config.json:
# {
#   "assetId"=809,
#   "workspaceId"=303
# } 
ftbx launch jobs "check-end-node-wf" --from-file "launch_config.json"

# launch a check-end-node-wf with your local configuration on asset id 809
ftbx launch jobs "check-end-node-wf" --params "assetId=809" --use-local
```

---

# Workflow Designer <a name="workflow-designer"></a>

```shell
$ ftbx workflowDesigner --help
                                                                                                                                                                                                                   
 Usage: ftbx workflowDesigner WORKFLOW_NAME [OPTIONS]                                                                                                                                                           
                                                                                                                                                                                                                   
 Opens the workflow designer for a given workflow in an environment.                                                                                                                                               
 -ftbx workflow_designer 'ftbx-workflow' --in 'cs-sbx'                                                                                                                                                               
                                                                                                                                                                                                                   
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    workflow_name      TEXT  [default: None] [required]                                                                                                                                                        │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --in          TEXT  [default: default]                                                                                                                                                                          │
│ --help              Show this message and exit.                                                                                                                                                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

### 1. Open workflow designer

```shell
# open workflow designer in default environment
ftbx workflowDesigner "Get or compute asset checksum"

# open workflow designer in wb-stg environment
ftbx workflowDesigner "Get or compute asset checksum" --in "wb-stg"
```

# Metadata Designer <a name="metadata-designer"></a>

```shell
$ ftbx metadataDesigner --help
                                                                                                                                                                                                                   
 Usage: ftbx metadataDesigner [OPTIONS]                                                                                                                                                                         
                                                                                                                                                                                                                   
 Opens the metadata designer in your default web browser.                                                                                                                                                          
 - ftbx metadataDesigner  # in default environment                                                                                                                                                                 
 - ftbx metadataDesigner --in 'cs-sbx'                                                                                                                                                                               
                                                                                                                                                                                                                   
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --in          TEXT  [default: default]                                                                                                                                                                          │
│ --help              Show this message and exit.                                                                                                                                                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

### 1. Open metadata designer

```shell
# open metadata designer in default environment
ftbx metadataDesigner

# open metadata designer in wb-stg environment
ftbx workflowDesigner --in "wb-stg"
```

# ERRORS & FIXES <a name="errors-fixes"></a>

### Self-signed certificates <a name="self-signed-certificates"></a>
```shell
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1006)
```
Fix: see [4. Connect to self-signed environments](#4-connect-to-self-signed-environments)

---

# CONTACTS <a name="contacts"></a>

David NAISSE - [dnaisse@dalet.com](dnaisse@dalet.com)
