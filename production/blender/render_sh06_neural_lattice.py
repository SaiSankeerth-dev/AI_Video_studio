# Headless Blender render script for sh06_neural_lattice
import bpy
import math

# Reset scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.fps = 30
scene.render.image_settings.file_format = 'PNG'

# World lighting (Dark investigative ambiance)
world = bpy.data.worlds.new("DocWorld")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes['Background']
bg.inputs['Color'].default_value = (0.01, 0.015, 0.025, 1.0)
bg.inputs['Strength'].default_value = 0.5

# Camera setup with slow cinematic push
cam_data = bpy.data.cameras.new("DocCamera")
cam_data.lens = 35.0
cam_data.dof.use_dof = True
cam_data.dof.focus_distance = 6.0
cam_data.dof.aperture_fstop = 2.8

cam_obj = bpy.data.objects.new("DocCamera", cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (0.0, -10.0, 1.8)
cam_obj.rotation_euler = (math.radians(82), 0.0, 0.0)

# Animate Camera Push
cam_obj.keyframe_insert(data_path="location", frame=1)
cam_obj.location = (0.0, -7.5, 1.6)
cam_obj.keyframe_insert(data_path="location", frame=180)

# Build Server Racks & Fiber Paths
for i in range(-5, 6):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(i * 2.2, 0.0, 1.5))
    rack = bpy.context.active_object
    rack.scale = (0.9, 0.8, 3.0)
    mat = bpy.data.materials.new(name=f"RackMat_{i}")
    mat.diffuse_color = (0.05, 0.08, 0.12, 1.0)
    rack.data.materials.append(mat)

# Render
scene.render.filepath = "//render_sh06_neural_lattice.png"
print("Blender blueprint compiled successfully for sh06_neural_lattice.")
