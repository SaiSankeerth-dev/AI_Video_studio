import sys
import os
try:
    import bpy
    IS_BLENDER = True
except ImportError:
    IS_BLENDER = False

def render(output_path, frames=150):
    if not IS_BLENDER:
        print(f"Standalone render mock to {output_path}")
        return
    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.fps = 30
    scene.frame_start = 1
    scene.frame_end = frames
    scene.render.filepath = output_path
    bpy.ops.render.render(animation=True)
    print(f"Rendered {frames} frames to {output_path}")

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'shot.mp4'
    render(out)
