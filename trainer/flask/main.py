from flask_cors import CORS
import os
import flask
import pickle
import numpy as np
import random

app = flask.Flask(__name__)
CORS(app)


class Test:
    def __init__(self, images, path, final_test=False):
        self.current_image = 0
        self.attempts = 0
        self.images = images

        self.const_images = images.copy()

        print(images)
        coords = [image.split("-")[1].split(".")[0] for image in images]
        self.coordinates = [tuple(map(int, coord[1:-1].split(","))) for coord in coords]
        self.labels = [image.split("-")[0] for image in images]
        self.path = path

        print(self.labels)

        self.distances = []
        self.first_try = True
        self.done = False
        self.text = ""
        self.final_test = final_test

    def get_current_image_path(self):
        return self.path + self.images[self.current_image]

class GreekTest:
    def __init__(self, images, path, final_test=False):
        self.current_image = 0
        self.attempts = 0
        self.images = images

        self.const_images = images.copy()

        self.labels = [image.split(".")[0] for image in images]
        self.path = path

        print(self.labels)

        self.distances = []
        self.first_try = True
        self.done = False
        self.text = ""
        self.final_test = final_test

    def get_current_image_path(self):
        print(self.path, self.current_image, self.images[self.current_image])
        return self.path + self.images[self.current_image]


class User:
    def __init__(self, id):
        self.id = id
        self.tests = []

    def save(self):
        with open(f"users/{self.id}.pkl", "wb") as f:
            pickle.dump(self, f)


def create_user(id):
    user = User(id)

    random.seed(0)
    images = os.listdir("images-resized")
    random.shuffle(images)

    user.tests.append(Test(images=images, path="images-resized/"))

    images = os.listdir("greek-images/")
    random.seed(1)
    random.shuffle(images)

    user.tests.append(GreekTest(images=images, path="greek-images/", final_test=True))

    return user


def load_user(id):
    # check if user exists
    if not os.path.exists(f"users/{id}.pkl"):
        return None

    with open(f"users/{id}.pkl", "rb") as f:
        user = pickle.load(f)

    return user


@app.route("/", methods=["POST"])
def index():
    d = flask.request.get_json()
    if d is None:
        return flask.jsonify({"error": "no json"})

    token = d["token"]

    user = load_user(token)
    if user is None:
        user = create_user(token)
        user.save()

    test = None
    for t in user.tests:
        if not t.done:
            test = t

    if test is None:
        return flask.jsonify({"error": "no test"})

    if "guess" in d.keys():
        guess = d["guess"].lower()

        if guess not in test.labels:
            test.text = "Word not found"
            data = test.__dict__
            return flask.jsonify(data)

        print("guess", guess)

        if guess == test.labels[test.current_image]:
            if test.first_try:
                test.images.remove(test.images[test.current_image])
                test.labels.remove(test.labels[test.current_image])
                test.coordinates.remove(test.coordinates[test.current_image])
                test.distances.append([0, guess, guess])
                test.attempts += 1
            else:
                test.first_try = True

            print(len(test.images))
            if len(test.images) > 1:
                test.current_image = random.choice(
                    [i for i in range(len(test.images)) if i != test.current_image]
                )
            elif len(test.images) == 1:
                test.current_image = 0
            else:
                test.done = True

            test.text = "Correct"
        else:
            test.first_try = False
            guess_index = test.labels.index(guess)
            # distance = np.sqrt(
            #     np.sum(
            #         np.square(
            #             np.subtract(
            #                 test.coordinates[test.current_image],
            #                 test.coordinates[guess_index],
            #             )
            #         )
            #     )
            # )
            # distance = round(distance, 3)
            test.distances.append([0, guess, test.labels[test.current_image]])

            # test.text = f"Incorrect; distance: {distance}; actual: {test.labels[test.current_image]}; guess: {guess}"
            test.text = (
                f"Incorrect; actual: {test.labels[test.current_image]}; guess: {guess}"
            )

            test.attempts += 1

    data = test.__dict__

    user.save()

    return flask.jsonify(data)


@app.route("/image/<token>")
def images(token):
    user = load_user(token)

    if user is None:
        return flask.jsonify({"error": "no user"})
    
    t = None

    for test in user.tests:
        if test.done:
            continue

        t = test

    image = t.get_current_image_path()
    print(image)

    return flask.send_from_directory(directory=image.split("/")[0], path=image.split("/")[1])


if __name__ == "__main__":
    app.run(host="localhost", port=3000)
