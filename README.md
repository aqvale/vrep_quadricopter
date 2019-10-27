# Quadricopter.py Vrep 🤖 🌟

**Vrep** The robot simulator [V-REP](http://www.coppeliarobotics.com/), with integrated development environment, is based on a distributed control architecture: each object/model can be individually controlled via an embedded script, a plugin, a ROS or BlueZero node, a remote API client, or a custom solution. This makes V-REP very versatile and ideal for multi-robot applications. Controllers can be written in C/C++, Python, Java, Lua, Matlab or Octave. 

[![Latest version on](https://badge.fury.io/py/instabot-py.svg)](https://badge.fury.io/py/instabot-py)

## Requirements

- Python v3.6 or greater
- V-REP 3.6.2 or greater
- Linux 64x

## Quick Start 🚀

- **Make sure you have Python 3.6 or above installed**

  - `python3 --version`


- **Install Python from Pyenv**

  - install [pyenv](https://mrdjangoblog.wordpress.com/2016/08/18/installing-pyenv-python-3-5/)
  - `pyenv install 3.6.0`

- **How to install** 🏁

  - Git `clone` this repo or download as a ZIP and extract
  - Run `python main.py`

- ** Configuration  ** ⚙️

  - To run `quadricopter-py` on other operating systems you need to replace the `remote_api.so` located in the folder `../V-REP_PRO_EDU_V3_6_2/programming/remoteApiBindings/lib/lib`.

## Documentation
- ** Quadricopter  ** <br>
| Atribute             | Type      |                Description                           | Default value |
|:--------------------:|:---------:|:----------------------------------------------------:|:-------------:|
| _serverIp            | str       | Address ip of the server remote                      | '127.0.0.1'   |
| _serverPort          | int       | Port of the server remote                            | 19999         |
| _refObj              | int       | Object value reference in vision sensor              |               |
| _clientID            | int       | Id of the client with api remote                     | |
| target               | object    | Target that control the quadricopter                 | |
| vision               | object    | Vision that get image                                | |
| sonar                | object    | Responsible for detecting collision when landing     | |
| vMin                 | float     | Minimum speed while searching. This value can be changed during application execution. | 0.1 |
| _objFound            | bool      | State object found                                   | |
| msg                  | str       | Mensage of the quadricopter                          | |

| Method               | Parameters|                Description                           |        Return                    |
|:--------------------:|:---------:|:----------------------------------------------------:|:--------------------------------:|
| _createTargetControl |           | Get object handle that control quadcopter            | Object with handle to control Target      |
| _createVisionSensor  |           | Get object handle vision sensor                      | Object with handle to get the Sensor Vision |
| _createSonarSensor   |           | Get object handle sonar sensor                       | Object with handle to get the Sensor Sonar |
| _startServer         |           | Start api remote                                     | The client ID, or -1 if the connection to the server was not possible|
| _finishServer        |           | Close the comunication with api remote               | |
| startPosition        | vStart - Initial speed <br> sMap - Object Scene Map | Initial position of quadricopter | |
| searchObj            | sMap - Object Scene Map | Search the object in the map | |
| land                 | sMap - Object Scene Map | Centers the quadricopter with the object | True if found sucess it and false if lose the object |

- ** SceneMap  **

- Fundamental for define the limits of the quadricopter simpler.
| Atribute             | Type      |                Description                           | Default value |
|:--------------------:|:---------:|:----------------------------------------------------:|:-------------:|
| xMin                 | float     | Minimum coordinate that the map displays             |               |
| xMax                 | float     | Maximum coordinate that the map displays             |               |
| yMin                 | float     | Minimum coordinate that the map displays             |               |
| yMax                 | float     | Maximum coordinate that the map displays             |               |
| zMin                 | float     | Minimum coordinate that the map displays             |               |
| zMax                 | float     | Maximum coordinate that the map displays             |               |

- ** VisionSensor  **

| Atribute             | Type      |                Description                           | Default value |
|:--------------------:|:---------:|:----------------------------------------------------:|:-------------:|
| id                   | int       | Get object handle vision sensor                      |    |
| _clientID            | int       | Id of the client with api remote                     | |
| resolution           | int       | Resolution the image                                 | |
| line                 | int       | Vector line representing a matrix line               | |
| half                 | int       | Divide the image into two parts                      | |  

| Method               | Parameters|                Description                           |        Return                    |
|:--------------------:|:---------:|:----------------------------------------------------:|:--------------------------------:|
| getImage             |           | Get imagem of the vision sensor                      | Return an array with view values       |
| getPositionObject    | image - Array of the captured image  <br> refObj - Object value reference in vision sensor   | Get the object position of the vision sensor                      | Return an array with orientation and direction respectively |

- ** TargetControl  **

| Atribute             | Type      |                Description                           | Default value |
|:--------------------:|:---------:|:----------------------------------------------------:|:-------------:|
| id                   | int       | Get object handle vision sensor                      |    |
| _clientID            | int       | Id of the client with api remote                     | | 

| Method               | Parameters|                Description                           |        Return                    |
|:--------------------:|:---------:|:----------------------------------------------------:|:--------------------------------:|
| getPosition          |           | Get the target position                              | Return the coordinate of the target x, y, z |
| setPosition          | x, y, z   | Set the target position                              |  |

- ** SonarSensor  **
| Atribute             | Type      |                Description                           | Default value |
|:--------------------:|:---------:|:----------------------------------------------------:|:-------------:|
| id                   | int       | Get object handle sonar  sensor                      |    |
| _clientID            | int       | Id of the client with api remote                     |    | 


| Method               | Parameters|                Description                           |        Return                    |
|:--------------------:|:---------:|:----------------------------------------------------:|:--------------------------------:|
| getStateColision     |           | Checks if the quadricopter will collide              | Return true if will collide and false if not |

## Documentation

- [VREP](http://www.coppeliarobotics.com/helpFiles/)

## Community

- [Forum](http://www.forum.coppeliarobotics.com)

## Tanks
Thanks you cimantec that allowed me to perform this test which provided knowing and learning how to use robotic automation tools. I would like to improve and learn a lot more in this area of study.