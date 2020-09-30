import db


def display_wood_records():
    print("id", "part", "type1", "type2", "category", "class", "material", "specie", "circumference", "length", sep="\t")

    for wood in db.get_all_wood_records():
        print(wood.id,
            wood.part.name, wood.type1.name, wood.type2.name, wood.category.name, wood.the_class.name,
            wood.material.name, wood.specie.name, wood.circumference, wood.length, sep="\t")


while True:
    cmd = input("Enter a command: 'list' or 'exit'\n")
    if cmd == "exit":
        exit(0)
    if cmd == "list":
        display_wood_records()
