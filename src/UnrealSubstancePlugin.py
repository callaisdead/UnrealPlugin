import tkinter.filedialog #imports the file dialog functionality from the tkinter modulue that will be used for selecting directories
from unreal import ToolMenuContext, ToolMenus, uclass, ufunction, ToolMenuEntryScript #imports various Unreal Engine classes and decorators used for menu context, tools, and scripting
#imports standard Python libraries for operating systems interactions, system-specific parameters, module reloading, ang GUI interactions
import os
import sys
import importlib
import tkinter

#adds the directory containing the current script to the system oath if it is not already included. This ensures that modules in the same directory can be imported
srcPath = os.path.dirname(os.path.abspath(__file__))
if srcPath not in sys.path:
    sys.path.append(srcPath)

#imports the UnrealUtilies module and reloads it to ensure the latest version is used
import UnrealUtilities
importlib.reload(UnrealUtilities)

#defines a New Unreal Engine tool menu entry script class using the @uclass decorator
@uclass()
class BuildBaseMaterialEntryScript(ToolMenuEntryScript):
    #overrides the can_execute method to call a utility function for building a base material and prints a confirmation message
    @ufunction(override=True)
    def can_execute(self, context: ToolMenuContext) -> None:
        UnrealUtilities.UnrealUtility().FindOrBuildBaseMaterial()
        print("Build Base Material")
#defines another Unreal Engine tool menu entry script class
@uclass()
class LoadMeshEntryScript(ToolMenuEntryScript):
    #overrides the execute method to open a file dialog for selecting a directory, then calls a utility function to import meshes from the selected directory
    @ufunction(override=True)
    def execute(self, context) -> None:
        window = tkinter.Tk()
        window.withdraw()
        importDir = tkinter.filedialog.askdirectory()
        window.destroy()
        UnrealUtilities.UnrealUtility().ImportFromDir(importDir)

class UnrealSubstancePlugin: #initializes the main pllugin class, setting up menu names and creating the menu
    def __init__(self):
        self.submenuName = "UnrealStubstancePlugin"
        self.submenuLabel = "Unreal Substance Plugin"
        self.CreateMenu()

    def CreateMenu(self): #creates the menu, addes submenus, and integrates the entry scripts into Unreal Engine's level editor main menu
        mainMenu = ToolMenus.get().find_menu("LevelEditor.MainMenu")

        existing = ToolMenus.get().find_menu(f"LevelEditor.MainMenu.{self.submenuName}")
        if existing:
            print(f"deleting previous menu: {existing}")
            ToolMenus.get().remove_menu(existing.menu_name)

        self.submenu = mainMenu.add_sub_menu(mainMenu.menu_name,"", self.submenuName, self.submenuLabel)
        self.AddEntryScript("BuildBaseMaterial", "Build base Material", BuildBaseMaterialEntryScript())
        self.AddEntryScript("LoadFromDirectory", "Load From Directory", LoadMeshEntryScript())
        ToolMenus.get().refresh_all_widgets()

    def AddEntryScript(self,name, label, script: ToolMenuEntryScript): #adds a menu entry script to the submenu, initializing and registering it
        script.init_entry(self.submenu.menu_name, self.submenu.menu_name, "", name, label)
        script.register_menu_entry()

UnrealSubstancePlugin() #instantiates the UnrealSubstancePlugin class, which sets up and displats the menu in Unreal Engine