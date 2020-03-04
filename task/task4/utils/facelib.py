import os
import numpy as np


def compute_dist(array1, array2):
    array3 = np.sqrt(np.power(array1, 2).sum(axis=1, keepdims=True))
    array4 = np.sqrt(np.power(array2, 2).sum(axis=1, keepdims=True))
    if np.dot(array3, np.transpose(array4)).any() == 0:
        return -1
    similarity = np.dot(array1, np.transpose(array2)) / np.dot(array3, np.transpose(array4))

    return similarity


class FaceLib():
    def __init__(self, threshold=(0.2, 0.7), path=''):
        self.threshold = threshold
        self.faces = {}
        self.path = path

    def __call__(self, face_feature):
        self.init()
        similarity, match_person = self.match(face_feature)
        if similarity > self.threshold[1]:
            return match_person
        elif similarity < self.threshold[0]:
            new_person = self.update(face_feature)
            return new_person
        else:
            return 'None'

    def init(self):
        assert len(self.path), 'save path of faces is not exist!'
        face_files = os.listdir(self.path)
        for face_file in face_files:
            name = face_file.split('.')[0]
            if name in self.faces:
                continue
            else:
                self.faces[name] = np.load(os.path.join(self.path, face_file))

    def match(self, face_feature):
        similarity = 0
        match_person = ''
        for name, save_feature in self.faces.items():
            s = compute_dist(face_feature, save_feature)
            if s > similarity:
                similarity = s
                match_person = name
        return similarity, match_person

    def update(self, face_feature):
        new_person = 'person{}'.format(len(self.faces)+1)
        print('====', new_person)
        # np.save(os.path.join(self.path, new_person + '.npy'), face_feature)
        return new_person

    def remove(self):
        os.remove(os.path.join(self.path, name+'.npy'))
