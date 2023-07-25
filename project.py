import os
import sys
import requests
from py_edamam import Edamam
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QPixmap


# Constants
EDAMAM_APP_ID = "d402015c"
EDAMAM_APP_KEY = "8976145cbbd79e2a40804d58d6b96b11"

# Class of the recipe's window
class Window(QMainWindow):
    def __init__(self, name, url, ingredients, calories, cuisineType, dishType):
        super(Window, self).__init__()
        loadUi("windowDesign.ui", self)
        # Configuring buttons
        self.copy_url.clicked.connect(self.copy_URL)
        self.return_to_recipes.clicked.connect(self.return_To_Recipes)
        self.exit.clicked.connect(self.exit_window)

        # Configuring text fields
        self.recipe_name.setText(name)
        self.recipe_url.setText(url)
        self.recipe_ingredients.setText(ingredients)
        self.recipe_calories.setText(str(calories))
        self.recipe_cuisineType.setText(cuisineType)
        self.recipe_dishType.setText(dishType)

        # Informing the user that the recipe image has been downloaded
        self.show_message(name)

    # Window methods
    def show_message(self, name):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Image Downloaded Successfully !")
        msg.setText(f"Picture downloaded as '{name}' in the current directory.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


    def copy_URL(self):
        text_to_copy = self.recipe_url.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(text_to_copy)


    def return_To_Recipes(self):
        self.close()


    def exit_window(self):
        sys.exit()


# Functions
def edamam_recipes_collector(ingredients):
    # Collecting recipes through the API
    e = Edamam(recipes_appid=EDAMAM_APP_ID, recipes_appkey=EDAMAM_APP_KEY)
    response = e.search_recipe(ingredients)
    recipes = [recipe['recipe'] for recipe in response["hits"]]

    return recipes


def edamam_recipes_infos(recipes):
    # Initializing Variables
    titles, images, urls, ingredients, calories, cuisineType, dishType = [], [], [], [], [], [], []

    # Sorting Elements
    for recipe in recipes:
        recipe_title = recipe['label']
        titles.append(recipe_title)

        recipe_image = recipe['image']
        images.append(recipe_image)

        recipe_url = recipe['url']
        urls.append(recipe_url)

        recipe_calories = round(float(recipe['calories']), 2)
        calories.append(recipe_calories)

        recipe_cuisineType = " - ".join(recipe['cuisineType'])
        cuisineType.append(recipe_cuisineType)

        recipe_dishType = " - ".join(recipe['dishType'])
        dishType.append(recipe_dishType)

        all_ingredients = [ingredient['text'] for ingredient in recipe['ingredients']]
        all_ingredients_string = " - ".join(all_ingredients)
        ingredients.append(all_ingredients_string)

    return titles, images, urls, ingredients, calories, cuisineType, dishType


def download_picture(name, link):
    # Trying to download the picture
    try:
        response = requests.get(link)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

    # Setting the picture's name as the recipe's name
    filename = name + ".jpg"

    with open(filename, "wb") as f:
        f.write(response.content)

    return True


def ingredients_collector() -> str:
    # initializing variables
    ingredients = list()
    ingredients_counter = 1
    # Getting the first ingredient (Obligatory)
    ingredient = input(f"Enter ingredient[{ingredients_counter}]: ")
    ingredients.append(ingredient)
    ingredients_counter += 1
    while True:
        answer = yes_or_no_answer("Do you still want to add ingredients")
        if answer:
            ingredient = input(f"Enter ingredient[{ingredients_counter}]: ")
            ingredients.append(ingredient)
            ingredients_counter += 1
        else:
            break

    ingredients_string = ' '.join(ingredients)

    return ingredients_string


def recipe_picker(titles):
    # Prompting the user to select a recipe
    for idx, recipe in enumerate(titles):
        print(f"[{idx + 1}]: {recipe}")

    while True:
        try:
            answer = int(input("Recipe to choose: "))
            while not (1 <= answer <= len(titles)):
                print("Invalid input !")
                answer = int(input("Recipe to choose: "))
        except ValueError:
            pass
        else:
            break

    return (answer - 1)


def recipe_info_shower(title, url, ingredients, calories, cuisineType, dishType): # Secondary To Use
    # Printing the recipe's infos instead of showing the recipe's window
    print(f"[1] : Recipe's Name: {title}")

    print(f"\n[2] : Recipe's URL: {url}")

    print("\n[3] : The Recipe's Ingredients :", ingredients, sep='\n')

    print(f"\n[4] : The Recipe's Total Calories: {calories}")

    print(f"\n[5] : The Recipe's Cuisine Type: {cuisineType}")

    print(f"\n[6] : The Recipe's Dish Type: {dishType}")

    return True


def window_maker(title, url, ingredients, calories, cuisineType, dishType):
    # Intializing the recipe's window
    app = QApplication([])
    window = Window(title, url, ingredients, calories, cuisineType, dishType)
    window.show()
    app.exec_()

    return True


def yes_or_no_answer(string):
    # Getting a 'y' or 'n' from the user
    answer = input(f"{string} (y/n): ").strip().lower()
    while answer != 'y' and answer != 'n':
        answer = input(f"{string} (y/n): ").strip().lower()

    if answer == 'y':
        return True
    else:
        return False


def screen_clear():
    # Clearing the terminal according to the user's system
    os.system('cls' if os.name == 'nt' else 'clear')
    return True


# Main function
def main():
    # Getting the ingredients from the user
    ingredients_string = ingredients_collector()

    # Web scrapping and collecting recipes
    recipes = edamam_recipes_collector(ingredients_string)

    # Sorting scrapped data
    titles, images, urls, ingredients, calories, cuisineType, dishType = edamam_recipes_infos(recipes)

    screen_clear()

    while True:
        # Prompting the user to select a recipe
        idx = recipe_picker(titles)
        screen_clear()
        download_picture(titles[idx], images[idx])
        window_maker(titles[idx], urls[idx], ingredients[idx], calories[idx], cuisineType[idx], dishType[idx])
        recipe_info_shower(titles[idx], urls[idx], ingredients[idx], calories[idx], cuisineType[idx], dishType[idx])


if __name__ == '__main__':
    main()
