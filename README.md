# Pytorch Summer Hackathon 2020 Information Page

## Project name: PyVinci


#### Main packages deployed:
- pyvinci-segmentation 
- pyvinci-client
- pyvinci-server

#### Main use cases:
- 1: Hashtag generator (Using a panoptic segmentation model)
- 2: (Not released): Generate new image from user labels (Using layer based sequencing image generator with GANs with the labels/masks created by the panoptic segmentation model)

#### Team members:
- Santiago Norena
- Hector Mejia
- Nicolas David
- Alejandro Martinez
- Sahivi Gonzalez

---------------------------------------------------------------------------------------
## PyVinci Use Case Diagram 
###### VERSION 2 (Areas highlighted in red were not released into production)
![use case diagram](architecture/UML-Diagrams/version-2/PyVinci-UseCase-Diagram.png)

## PyVinci System Architecture Diagram 
##### Cross-function / Swimlane diagram
###### VERSION 2 (Version released for competition)
![cross-function / swim lane diagram](architecture/UML-Diagrams/version-2/PyVinci-System-Architecture-Diagram.png)

---------------------------------------------------------------------------------------
## Deployment Demo:

Accessing the domain name https://www.pyvinci.com/ will take user to the main page. (No longer in production)

#### New user needs to register, then login.
![login page](deployment_demo/login_page.png)

#### Once logged in, user can see list of projects, or create a new one.
![projects page](deployment_demo/projects_list_page.png)

#### After uploading images in new project page, the user can click "Begin Modeling".
![before model](deployment_demo/new_project_BEFORE_running_model.png)

#### After the ML model generates labels for all images, they will show up below each image. 
#### User can click "Home" to create a new project or see list of projects.
![after model](deployment_demo/new_project_AFTER_running_model.png)

## PyVinci Initial Concept
![PyVinci Initial(use case #2)](deployment_demo/pyvinci-thumbnail.png)

## PyVinci Initial Concept
![PyVinci Initial(use case #2)](client/pyvinci_final.png)

## It was built with:
- numpy
- python
- pytorch
- detectron2
- cv2
- psycopq2
- sqlalchemy
- posgresql
- docker
- go / golang 
- go-fiber
- nginx
- Amazon Web Services (AWS): EC2, S3
- npm
- react
- miragejs

### Acknowledgements:
- https://github.com/0zgur0/Seq_Scene_Gen
