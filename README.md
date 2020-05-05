# pscraper-tool
This project contains the script that is used to schedule the daily scraping script. 

## Overview
It uses the [schedule](https://pypi.org/project/schedule/) library to schedule daily scrape jobs. 
The scraping process is comprised of several scrape jobs which are configured in a [`config.yml`](/config.yml) file.
Each job will run concurrently on a separate process. When all processes are complete the script
builds and sends a slack report. The script is also responsible for configuring the logging. 
The logs reside in the `logs` directory.

The script is automated to run daily without interruptions. The command used to run it is 
```bash
$ nohup ./scrape.py &
```
It runs inside a tmux session in a Google Cloud Compute Engine so that the process doesn't require any supervision.