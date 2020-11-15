# Pytorch Summer Hackathon 2020 Information Page

## Project name: PyVinci

<<<<<<< Updated upstream
#### Main packages deployed:
=======
#### Main packages deployment packages:
>>>>>>> Stashed changes
- pyvinci-segmentation 
- pyvinci-client
- pyvinci-server

#### Team Members:
- Santiago Norena
- Hector Mejia
- Nicolas David
- Alejandro Martinez
- Sahivi Gonzalez

#### Main Use Cases
- Use Case #1: Hashtag generator (Using a panoptic segmentation model)
- Use Case #2 (Not released in production): Generate new image from user labels (Using layer based sequencing image generator with GANs with the labels/masks created by the panoptic segmentation model)
---------------------------------------------------------------------------------------

## PyVinci Use Case Diagram 
###### VERSION 2 (*Areas highlighted in red were not released into production)
![use case diagram](architecture/UML-Diagrams/version-2/PyVinci-UseCase-Diagram.png)

## PyVinci System Architecture Diagram 
##### (Cross-function / Swim lane diagram)
###### VERSION 2 (*Version released for competition)
![cross-function / swim lane diagram](architecture/UML-Diagrams/version-2/PyVinci-System-Architecture-Diagram.png)

## PyVinci Initial Concept
![PyVinci Initial(use case #2)](client/pyvinci_final.png)

---------------------------------------------------------------------------------------
## Deployment Demo:

#### Webpage
- https://www.pyvinci.com/ (*No longer in production)


- TODO: Show screenshots


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
