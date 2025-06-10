class ProjectModel:
def init(self):
self.project_name = ""
self.author = ""
self.address = ""
self.image_path = ""
self.grid_size = 50
self.grid_origin = (0, 0)

def set_project_info(self, name, author, address):
    self.project_name = name
    self.author = author
    self.address = address

def set_image_path(self, path):
    self.image_path = path

def set_grid_parameters(self, size, origin_x, origin_y):
    self.grid_size = size
    self.grid_origin = (origin_x, origin_y)
