# A simple class demonstration in Python

class Animal:
    # Class attribute (shared by all instances)
    species_count = 0
    
    # Constructor (initialization method)
    def __init__(self, name, age):
        # Instance attributes (unique to each instance)
        self.name = name
        self.age = age
        Animal.species_count += 1
    
    # Instance method
    def make_sound(self):
        return "Some generic sound"
    
    # Instance method with string representation
    def __str__(self):
        return f"{self.name} is {self.age} years old"

# Inheritance demonstration
class Dog(Animal):
    def __init__(self, name, age, breed):
        # Call parent class's __init__
        super().__init__(name, age)
        self.breed = breed
    
    # Override parent's method
    def make_sound(self):
        return "Woof!"

# Creating and using instances
if __name__ == "__main__":
    # Create an Animal instance
    generic_animal = Animal("Generic", 5)
    print(generic_animal)  # Using __str__ method
    print(generic_animal.make_sound())
    
    # Create a Dog instance
    my_dog = Dog("Buddy", 3, "Golden Retriever")
    print(my_dog)
    print(f"{my_dog.name} says: {my_dog.make_sound()}")
    print(f"Breed: {my_dog.breed}")
    
    # Demonstrate class attribute
    print(f"Total number of animals created: {Animal.species_count}")