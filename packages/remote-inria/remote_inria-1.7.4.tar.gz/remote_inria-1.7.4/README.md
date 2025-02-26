# RemI

## -> [Documentation](https://remote-inria.gitlabpages.inria.fr/) <-

**Rem**ote **I**nria\
Code here, run there !

_A CLI tool for remotely interacting with Inria computing resources._


## What is remi ?

remi is a tool aiming at easing the workflow of Inria researchers when it comes to performing
computations remotely.
More precisely, **remi** is configured for each project you might want to
use it for.\
Once your preferences are set, you can run your code either on your desktop at Inria or on one the
cluster nodes.

If you are tired of messing up with 4-line `oarsub` commands or if you find yourself `commit`ting
and `push`ing your code each time you want to test it remotely, this tool is for you !

**Note:** Even though this tool has been made to work from a personal computer different from your
Inria desktop, it also totally works when running directly from the Inria desktop.\
Most of the `remi` features are still relevant in this case.

**Presentation / tutorial video:**\
https://odysee.com/@GaetanLepage:6/remote-inria:6


## Main features
- **Synchronization:** **remi** creates a remote clone of your project on the Inria storage space
  (under `\scratch`) and lets you synchronize it easily.
- **Remote execution:** The core idea behind **remi** is to provide an easy way to execute code on
  remote computers (regular Inria desktops or cluster servers).
- **Clusters and singularity support:** The _complex_ way to request computing resources is
  integrated in **remi** to minimize overhead. Singularity container management is also embedded
  (build and use).

- **Jupyter notebook support:** This tool lets you run a jupyter notebook server on your Inria
  workstation and connect to it locally on the browser.


## Contributing

Any help to the improvement of **remi** is more than welcome.\
You may write an issue to warn me of any bug or desired feature by [writing an
issue](https://gitlab.inria.fr/remote-inria/remi/-/issues/new).


## Acknowledgement

This project was inspired from [LabML Remote](https://github.com/lab-ml/remote).\
The latter does not support `ssh` through a bastion because it uses the
[paramiko](https://www.paramiko.org/) library. RemI, on the other hand, uses traditional calls to
`ssh` command.\
The main motivation to start a separate project was to design a tool specifically with the Inria
computing needs in mind (use of Inria clusters, natively using the available resources etc).
