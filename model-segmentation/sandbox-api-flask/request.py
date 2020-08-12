# curl -X POST -H "Content-Type: application/json" --data '{"imageURL": "https://storage.googleapis.com/segmentation-testing/testing_images1/bikes.jpeg"}' http://localhost:5000/predict


import requests

headers = {
    'Content-Type': 'application/json',
}

data = '{"imageURL": "https://storage.googleapis.com/segmentation-testing/testing_images1/bikes.jpeg"}'

response = requests.post('http://localhost:5000/predict', headers=headers, data=data)

print(response)
