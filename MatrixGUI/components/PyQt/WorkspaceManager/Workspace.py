from DirectorySpace import DirectorySpace
from Scene import Scene
from Utils import Utils

class Workspace(DirectorySpace):
    """ A workspace containing its own configuration and scenes.

    Attributes:
        name (str): The name of the workspace.
        path (str): The path of the workspace.
        subdirs (dict(str,str)): The useful subdirectories (path,name)
        scenes (dict(str,Scene)): The dictionnary of the scenes it contains.
            Keys are the scene paths.
        current_scene (str): The path of the current scene
        qt_directory (QDir): The directory corresponding to that workspace
    """

    def __init__(self, name="", absolute_path=""):
        """Initialize a workspace.

        Args:
            name (str): The name of the workspace. Default is "".
            absolute_path (str): The absolute path of the workspace. Default is "".

        Raises:
            AssertionError: If a directory with that path already exists.

        Examples:
            >>> ws = Workspace("ws1","/home/mpizenbe/matrix/ws1")
        """
        super().__init__(name,absolute_path,"absolute")
        self.subdirs["Configs"] = "Configuration folder"
        for subpath in self.subdirs:
            self.qt_directory.mkpath(subpath)
        self.scenes = dict()
        self.current_scene = ""

    def delete(self):
        """ Delete the workspace (and its contents).

        It must not be called by itself but by the workspace manager !

        Raises:
            AssertionError: If the workspace directory does not exist or can not be deleted.
        """
        # Deleting the scenes
        self.current_scene = ""
        for scene_path in self.scenes:
            self.delete_scene(scene_path)
        # Deleting the workspace directory
        super().delete()


    def new_scene(self, name="", path=""):
        """ Add a new scene to the workspace.

        Args:
            name (str): The name of the new scene
            path (str): The local path of the scene (inside workspace)

        Raises:
            AssertionError: If a scene with the same path already exists.
        """
        path = Utils.valid_name(path)
        assert (path not in self.scenes), "A scene with the path "+path+" already exists."
        scene = Scene(self, name, path)
        self.scenes[scene.path] = scene
        self.set_current_scene(scene.path)
        print(scene)

    def delete_scene(self, scene_path):
        """ Delete the scene identified by its local path.

        Args:
            scene_path (str): The path (relatively to the workspace) of the scene to delete.
        """
        assert (scene_path in self.scenes),\
                "The scene "+ scene_path +" does not exist in the workspace."
        self.scenes[scene_path].delete()
        del self.scenes[scene_path]
        if (self.current_scene == scene_path):
            self.current_scene = ""

    def get_current_scene(self):
        """ Get the current scene of the workspace.

        Returns:
            Scene: The current scene.

        Raises:
            AssertionError: If no current scene.
            AssertionError: If the current scene has disappeared.
        """
        assert (self.current_scene), "There is no current scene."
        assert (self.current_scene in self.scenes), "The current scene is not reachable."
        return self.scenes[self.current_scene]

    def set_current_scene(self, scene_path):
        """ Set the current scene.

        Args:
            scene_path (str): The relative path of the scene which will be the current scene.

        Raises:
            AssertionError: If the scene does not exist in the workspace.
        """
        assert (scene_path in self.scenes), "That scene does not exist in this workspace."
        self.current_scene = scene_path

    def __str__(self):
        """ Change displaying of a workspace.

        Example:
            >>> print(workspace)
        """
        s = ["Workspace : " + self.name                     ,\
             "   path          : " + self.path              ,\
             "   current scene : " + self.current_scene     ,\
             "   all scenes    : " + str(list(self.scenes.keys()))]
        return "\n".join(s)