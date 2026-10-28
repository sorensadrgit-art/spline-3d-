"""Create a licensed sky texture for the delivery viewer; retain the HDR master."""
import bpy
import numpy as np
from pathlib import Path
root=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(root/'kinetic-studio-proof-v006.blend'),load_ui=False)
scene=bpy.context.scene
source=next(n.image for n in scene.world.node_tree.nodes if n.type=='TEX_ENVIRONMENT')
image=source.copy();image.scale(2048,1024)
pixels=np.asarray(image.pixels[:],dtype=np.float32).reshape(-1,4)
pixels[:,:3]*=np.asarray([.26,.39,.78],dtype=np.float32)*.30
image.pixels.foreach_set(pixels.reshape(-1))
scene.render.image_settings.file_format='JPEG';scene.render.image_settings.quality=90
image.save_render(str(root.parent/'kinetic-tour/public/models/blue-hour.jpg'),scene=scene)
print('KINETIC_LICENSED_SKY_READY')
