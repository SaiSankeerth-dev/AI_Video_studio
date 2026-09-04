import math
import sys
import os
try:
    import bpy
    IS_BLENDER = True
except ImportError:
    IS_BLENDER = False

def build_atlas_datacenter_scene(output_blend_path="D:/gitM/01_ContentFactory/projects/video-001/blender/scene-files/atlas_datacenter.blend"):
    if not IS_BLENDER:
        print("Running outside of Blender.")
        return

    # Clean default objects
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    # 1. World Settings
    world = bpy.data.worlds.new("AtlasWorld")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs[0].default_value = (0.01, 0.01, 0.02, 1.0)
        bg_node.inputs[1].default_value = 0.2

    # 2. Server Rack Material
    mat_server = bpy.data.materials.new(name="ServerRackMat")
    mat_server.use_nodes = True
    bsdf = mat_server.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.05, 0.05, 0.06, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.3

    # LED Material
    mat_led = bpy.data.materials.new(name="LedMat")
    mat_led.use_nodes = True
    bsdf_led = mat_led.node_tree.nodes.get("Principled BSDF")
    if bsdf_led:
        bsdf_led.inputs["Emission Color"].default_value = (0.0, 0.8, 1.0, 1.0)
        bsdf_led.inputs["Emission Strength"].default_value = 5.0

    # 3. Server Racks (Grid Layout)
    for row in range(-3, 4):
        for col in range(-5, 6):
            if col == 0: continue # Central Corridor
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(col * 2.2, row * 4.5, 1.5))
            rack = bpy.context.active_object
            rack.scale = (0.7, 1.4, 3.0)
            rack.data.materials.append(mat_server)

            # LED Indicator bar
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(col * 2.2, row * 4.5 - 0.75, 1.8))
            led = bpy.context.active_object
            led.scale = (0.5, 0.05, 0.1)
            led.data.materials.append(mat_led)

    # 4. Floor Plane with Metallic Reflection
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0))
    floor = bpy.context.active_object
    mat_floor = bpy.data.materials.new(name="FloorMat")
    mat_floor.use_nodes = True
    bsdf_floor = mat_floor.node_tree.nodes.get("Principled BSDF")
    if bsdf_floor:
        bsdf_floor.inputs["Base Color"].default_value = (0.02, 0.02, 0.03, 1.0)
        bsdf_floor.inputs["Roughness"].default_value = 0.15
        bsdf_floor.inputs["Metallic"].default_value = 0.8
    floor.data.materials.append(mat_floor)

    # 5. Camera with Slow Dolly Push
    bpy.ops.object.camera_add(location=(0, -14, 1.7), rotation=(math.radians(88), 0, 0))
    cam = bpy.context.active_object
    bpy.context.scene.camera = cam

    cam.keyframe_insert(data_path="location", frame=1)
    cam.location = (0, -2, 1.7)
    cam.keyframe_insert(data_path="location", frame=150)

    # 6. Lighting
    for y in [-10, -5, 0, 5, 10]:
        bpy.ops.object.light_add(type='POINT', location=(0, y, 3.5))
        light = bpy.context.active_object
        light.data.energy = 250
        light.data.color = (0.0, 0.65, 1.0)

    # 7. Save .blend file
    os.makedirs(os.path.dirname(output_blend_path), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=output_blend_path)
    print(f"Atlas Data Center 3D scene saved to: {output_blend_path}")

if __name__ == '__main__':
    out_blend = sys.argv[-1] if len(sys.argv) > 1 and sys.argv[-1].endswith('.blend') else "D:/gitM/01_ContentFactory/projects/video-001/blender/scene-files/atlas_datacenter.blend"
    build_atlas_datacenter_scene(out_blend)
