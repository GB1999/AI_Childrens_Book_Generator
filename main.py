# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from story_generator import StoryGenerator

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
 sg = StoryGenerator("config.json")
 sg.pick_story()
 sg.visualize_story()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
