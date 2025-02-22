#!/usr/bin/env python3

class Course:

    def __init__(self, nombre, duracion, link):
        self.nombre = nombre
        self.duracion = duracion
        self.link = link

    def __repr__(self):

        return f'El curso tiene el nombre: {self.nombre} duracion de: {self.duracion} horas y su link es: {self.link}\n'

    #Se puede usar __repr__ para hacer lo de un _str_ pero linea a linea, cosa que puedas hacer
    # courses[0] y te salga en objeto uno con su respectivo texto
    #__str__ solo se muestra con un iterador, repr, se puede usar sin un for, simplemente 
    #mostrando el objeto.


courses = [
    Course("Introduccion al hacking", 53, "wwww.hack.com"),
    Course("Personalizacion de linux", 3, "wwww.hack.com"),
    Course("Introduccion a Linux", 13, "wwww.hack.com")
]

def list_courses():
    for course in courses:
        print(course)

def search_course_by_name(name):
    for course in courses:
        if course.nombre == name:
            return course

    return None
