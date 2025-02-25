# colav_protobuf

[![PyPI - Version](https://img.shields.io/pypi/v/colav-protobuf.svg)](https://pypi.org/project/colav-protobuf)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/colav-protobuf.svg)](https://pypi.org/project/colav-protobuf)
<!--[![PyPI - Protobuf Version]()]-->
This package contains python protobuf compilations for easy import as well as mock examples of each of these messages you can import via examples.

Message types include and their proto formatting include: 
- [missionRequest](https://github.com/RyanMcKeeQUB/colav_protobuf/tree/main/src/colav_proto/missionRequest.proto)
- [missionResponse](https://github.com/RyanMcKeeQUB/colav_protobuf/tree/main/src/colav_proto/missionResponse.proto)
- [agentUpdate](https://github.com/RyanMcKeeQUB/colav_protobuf/tree/main/src/colav_proto/agentUpdate.proto)
- [obstaclesUpdate](https://github.com/RyanMcKeeQUB/colav_protobuf/tree/main/src/colav_proto/obstaclesUpdate.proto)
- [controllerFeedback](https://github.com/RyanMcKeeQUB/colav_protobuf/tree/main/src/colav_proto/controllerFeedback.proto)

-----

## Table of Contents

- [Installation](#installation)
- [Structure](#structure)
- [Usage](#usage)
- [License](#license)

## Installation

```bash
pip install colav-protobuf
```

## Structure
The src code in [colav_protobuf](https://github.com/RyanMcKeeQUB/colav_protobuf) shows that the project is organised into main directories: 
- [Tests](https://github.com/RyanMcKeeQUB/colav_protobuf/tree/main/tests): The tests directory contains a variety of unit tests ensuring that the pkg is working as expected and are called as apart of the CI/CD pipeline defined by the [github_action](./.github/workflows/workflow.yml)
- [src](https://github.com/RyanMcKeeQUB/colav_protobuf/tree/main/src/): The src contains three pkgs
    -   [colav_proto](https://github.com/RyanMcKeeQUB/colav_protobuf/tree/main/src/colav_proto/)the original proto files which were compiled by protobuf compiler [protos](./src/colav_proto/) these are un-importable but will give you a good idea of the proto structure.
    - [colav_protobuf](https://github.com/RyanMcKeeQUB/colav_protobuf/tree/main/src/colav_protobuf/): This is the importable python pkg you can import the different messages types as follows: 
    - [examples](https://github.com/RyanMcKeeQUB/colav_protobuf/tree/main/src/colav_protobuf/examples/): This pkg contains mock of each of the protobufs for example and testing purposes.

## Usage
When pkg is installed, Using it is simple imports are as follows. 

```python
    from colav_protobuf import MissionRequest
    from colav_protobuf import MissionResponse
    from colav_protobuf import AgentUpdate
    from colav_protobuf import ObstaclesUpdate
    from colav_protobuf import ControllerFeedback
```

Examples of these object initiations are shown in the [examples](https://github.com/RyanMcKeeQUB/colav_protobuf/tree/main/src/colav_protobuf/examples/) which contains a number of importable message exmaples.
how to publish it via a python socket: 

Here is a sample of proto creation of a agent configuration message: and 

```python
    from colav_protobuf import AgentUpdate
    import socket 

    agent_update = AgentUpdate
    agent_update.mission_tag = "COLAV_MISSION_NORTH_BELFAST_TO_SOUTH_FRANCE"
    agent_update.agent_tag = "EF12_WORKBOAT"
    agent_update.state.pose.position.x =   float(3_675_830.74)
    agent_update.state.pose.position.y = float(-272_412.13)
    agent_update.state.pose.position.z =  float(4_181_577.70)
    agent_update.state.pose.orientation.x = 0
    agent_update.state.pose.orientation.y = 0
    agent_update.state.pose.orientation.z = 0
    agent_update.state.pose.orientation.w = 1

    agent_update.state.velocity = 20
    agent_update.state.yaw_rate = 0.2
    agent_update.state.acceleration = 1

    agent_update.timestamp = "1708853235"
    agent_update.timestep = "000000000012331"

    aserialised_agent_update = agent_update.SerializeToString()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(serialized_agent_update, ("192.168.1.100", 7200))
```


## License

`colav-protobuf` is distributed under the terms of the [MIT](https://github.com/RyanMcKeeQUB/colav_protobuf/tree/main/LICENSE) license.
