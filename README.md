# Poster

## Concept

Perfecting the way jobs are launched and executed, by providing a simple interface to run experiments using existing
technologies.
The project is focused on single experiments.
For multirun experiments or parameter sweeping, write a wrapper script that deals with job submission.

Take a look at:

- <https://github.com/maharshi95/submititnow>

## Features

- run, rerun and continue experiments

## CLI

TODO

## Callbacks

Callbacks can server all sorts of purposes. They can be used to save the model, log metrics, etc.

- [X] Hydra Zen (argument parsing) Parse arguments using Hydra
- [ ] Hydra (argument parsing) Parse arguments using Hydra
- [ ] Aim (Experiment Tracker) Log metrics and hyperparameters
- [ ] Python Fire (argument parsing) Parse arguments using Python Fire
- [ ] Local Directory (data storage) Save files to a local directory
- [ ] S3 (data storage) Save files to S3
- [ ] Weights & Biases (Experiment Tracker) Log metrics and hyperparameters
- [ ] SCP (data storage) Securely copy files to a remote server
- [ ] Submitit (Job submission) Submits the job to a cluster
- [ ] Logging (logging) Logs the output of the experiment
- [ ] Telegram (notification) Sends a message to a telegram bot when the experiment is done
- [ ] Email (notification) Sends an email when the experiment is done
- [ ] HardwareInfo (monitoring) Monitors your GPU usage
- [ ] Git (version control) Can check out a specific commit, branch, etc. before running

## Extra functions

Logging functions:

- log metric
- log message
- log image(s)

data save functions

- save file (based on local, scp, s3, etc.)
  offline mode is a priority, so extend the callbacks to save locally first, then upload to s3 or scp?
  This would require a pipeline to be set up, so that the data is saved locally first, then uploaded to the cloud (in 2
  processing steps).
  Hard to track what has been executed without a central database (like sqlite)

## Usage

Use it as shown in `simple.py`.

`python script.py --hello` executes the script, but does it like poster was not there.

`poster run python script.py --hello` executes the script with all defined callbacks.

`post run python script.py --hello \ python script.py --world` does a multirun execution.

To do the multirun execution we do some sys.argv manipulation, so every run works fine!

TODO: how to deal with forking, e.g. when they run on different nodes, e.g. when using submitit.

TODO: auto invoke end function on program end! (e.g. even when sigterm or similar is received)

TODO: need to create a poster.json file to be able to rerun the experiment.

TODO: should argument parsing, e.g. with hydra, be done in the script or in the poster?

TODO: Conceptually, i think all callbacks should be part of the run.
What is now referred to as job adds so much complexitry.
