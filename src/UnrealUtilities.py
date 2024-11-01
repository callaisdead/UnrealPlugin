from unreal import ( #importing various Unreal Engine classes and modules needed for asset manipulation, material creation, and importing
    AssetToolsHelpers,
    EditorAssetLibrary,
    AssetTools,
    Material,
    MaterialFactoryNew,
    MaterialEditingLibrary,
    MaterialExpressionTextureSampleParameter2D as TexSample2D,
    MaterialProperty,
    AssetImportTask,
    FbxImportUI
)

import os #importing the OS (operating system interactions) module to interact with the file system

#setting up intial paths and names for substance directory, base material, and texture parameters
class UnrealUtility:
    def __init__(self):
        self.substanceRootDir = '/game/Substance/'
        self.substancBaseMatname = 'M_SubstanceBase'
        self.substanceBaseMatPath = self.substanceRootDir + self.substancBaseMatname
        self.substanceTempFolder = '/game/Substance/temp'
        self.baseColorName = "BaseColor"
        self.normalName = "Normal"
        self.occRoughnessMetallic = "OcclusionRoughnessMetallic"

    #retrieves asset tools for further operations
    def GetAssetTools()->AssetTools:
        AssetToolsHelpers.get_asset_tools()
        
    #iterates through the specified directory and processes .fbx files
    def ImportFromDir(self, dir):
        for file in os.listdir(dir):
            if ".fbx" in file:
                self.LoadMeshFromPath(os.path.join(dir, file))
    
    #Configures and executes an import task for the specified mesh path, setting import options and hangling skeletal mesh imports
    def LoadMeshFromPath(self, meshPath):
        meshName = os.path.split(meshPath)[-1].replace(".fbx", "")
        importTask = AssetImportTask()
        importTask.replace_existing = True
        importTask.filename = meshPath
        importTask.destination_path = '/game/' + meshName
        importTask.automated = True
        importTask.save = True

        fbxImportOption = FbxImportUI()
        fbxImportOption.import_mesh = True
        fbxImportOption.import_as_skeletal = True
        fbxImportOption.import_materials = False
        fbxImportOption.static_mesh_import_data.combine_meshes = True
        importTask.options = fbxImportOption

        self.GetAssetTools().import_asset_tasks([importTask])
        return importTask.get_objects()[0]
       
    #Cheks if the base material exists, if not, it creates a new one with specified texture parameters (BaseColor, Normal, OcclusionRoughnessMetallic) and saves it, 
    def FindOrBuildBaseMaterial(self):
        if EditorAssetLibrary.does_asset_exist(self.substanceBaseMatPath):
            return EditorAssetLibrary.load_asset(self.substanceBaseMatPath)
        
        baseMat = self.GetAssetTools().create_asset(self.substancBaseMatname, self.substanceRootDir, Material, MaterialFactoryNew)
        baseColor = MaterialEditingLibrary.create_material_exprsession(baseMat,TexSample2D, -800, 0)
        baseColor.set_eitor_property("parameter_name", self.baseColorName)
        MaterialEditingLibrary.connect_material_property(baseColor, "RGB", MaterialProperty.MP_BASE_COLOR)

        normal = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 400)
        normal.set_editor_property("parameter_name", self.normalName)
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal"))
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL)

        occRoughnessMetallic = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 800)
        occRoughnessMetallic.set_editor_property("parameter_name", self.occRoughnessMetallic)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "G", MaterialProperty.MP_ROUGHNESS)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "B", MaterialProperty.MP_METALLIC)

        EditorAssetLibrary.save_asset(baseMat.get_path_name())
        return baseMat