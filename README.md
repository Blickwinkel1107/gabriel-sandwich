# Information about the original Sandwich App

Please refer to [this repo](https://github.com/cmusatyalab/gabriel-sandwich#readme) for more information

# Sandwich Engine state

## User State

Start->nothing->bread->ham->lettuce->cucumber->half->tomato->ham_wrong->full

Holo_x/y: keep updating

## Update

Update Trigger: det_for_class + current engine state

### Algorithm
```
Foreach object_class:
    Foreach detected_object:
        If confidence score >= 0.5, then add to det_for_class dict
        Get_instruction(engine_state, det_for_class)
```

### How gabriel keeps the state
Originally, the state is only presented in the communicating message

But for study of project, I implemented the state on the cloudlet side

You can see "self.user_progress" is the user state on server side.

# Migration
## Related Links
[Dockerhub](https://hub.docker.com/repository/docker/blickwinkel1107/gabriel-sandwich-os/general)

[Github](https://github.com/Blickwinkel1107/gabriel-sandwich)

[Andriod App](https://github.com/Blickwinkel1107/gabriel-instruction)

[Course Project Poster](): for Background, System Architecture, Reflection, etc

## Workflow
```
Orchestrator
->Signal "START_MIGRATE" (in packet)
->MigrateEngine @ VM#1
->MessageQueue @ VM#1
->Sandwich::handle_migrate() @ VM#1
->MigrateAPI::extract_state_callback() @ VM#1
->MigrateEngine @ VM#2
->Sandwich::handle_merge() @ VM#2
->MigrateAPI::merge_state_callback() @ VM#2
```
For more info and visualization, please refer to [Project Poster]()

## How to Start a migration
Note: this project cannot work solely with Github codes. The libraries it required are outdated and installed in docker image only. Recommend run the docker.

1. Pull the docker from Dockerhub
   ```bash
   docker pull blickwinkel1107/gabriel-sandwich-os
   ```
2. Run docker
   
   Note: Require 9099 (for gabriel) and 8765 (for orchestrator request) ports are open on the host. Host must have a gpu.
   ```bash
   docker run --rm -it --gpus all --network host blickwinkel1107/gabriel-sandwich-os
   ```
3. Run Sandwich Backend Engine (and MigrateEngine)
   
   Enter the docker, and type commands:
   ```bash
   cd ~/gabriel-sandwich
   ./main.py
   ```
4. Start sandwich application ([download here](https://github.com/Blickwinkel1107/gabriel-instruction)) on client side (cell phone/google glass/any wearable device)
   
   You need to use gradle to compile the application and install it on your device. 
   
5. When working with Sandwich Application, you can migrate the states by following command:
   ```bash
   python3 migrate_orchestrator.py <Addr>:5678
   ``` 
   for example:
   ```bash
   python3 migrate_orchestrator.py cloudlet021.elijah.cs.cmu.edu:5678
   ```
   After enter the command, the migration request will be sent to "cloudlet021.elijah.cs.cmu.edu".
   On the client app, you will see the state will be migrated to another cloudlet. 

6. See useful logs
   ```bash
   cd ~/gabriel-sandwich
   ./taillog.sh
   ```
   or
   ```bash
   cd ~/gabriel-sandwich
   tail -F logs
   ```
