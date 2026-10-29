"""Refine v002 from its locked camera; preserve source versions and editable assets."""
import bpy, math, random, json, time, ast, sys
from pathlib import Path
from mathutils import Vector, Matrix, noise

ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets'
random.seed(271027)
bpy.context.preferences.filepaths.use_scripts_auto_execute=False
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'kinetic-studio-proof-v002.blend'),load_ui=False)
scene=bpy.context.scene
baseline_camera=list(scene.camera.matrix_world)
baseline_zones={c.name:len(c.objects) for c in scene.collection.children if 'ZONE_' in c.name}

# Reuse the existing mesh helpers without running the original scene rebuild.
tree=ast.parse((ROOT/'build_kinetic_studio.py').read_text(encoding='utf-8'))
helpers={'box','tube','ellipsoid','path','finish','move_to_collection','material','area'}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in helpers],type_ignores=[]),'scene_helpers','exec'))
def collection(name):
    global COL
    COL=bpy.data.collections.new(name);scene.collection.children.link(COL);return COL
def hide(obj):
    obj.hide_render=True;obj.hide_set(True)
def hide_tree(root):
    hide(root)
    for child in root.children_recursive:hide(child)
def image(path,noncolor=False):
    im=bpy.data.images.load(str(path),check_existing=True)
    im.colorspace_settings.name='Non-Color' if noncolor else 'sRGB'
    return im

black=bpy.data.materials['Graphite powder coat']
chrome=bpy.data.materials['Brushed aluminum']
walnut=bpy.data.materials['Oiled walnut cabinetry']
rubber=bpy.data.materials['Rubber and cable jacket']
ceramic=bpy.data.materials['Stoneware planter']
stemmat=bpy.data.materials['Plant stems']
leaf=bpy.data.materials['Leaf wax']
cream=bpy.data.materials['Warm paper and bone']

collection('11_REFINED_FURNITURE')
leather=bpy.data.materials['Soft espresso leather']
nt=leather.node_tree;p=nt.nodes['Principled BSDF']
tex=nt.nodes.new('ShaderNodeTexCoord');mapping=nt.nodes.new('ShaderNodeVectorMath');mapping.operation='SCALE';mapping.inputs['Scale'].default_value=1.8
nt.links.new(tex.outputs['Generated'],mapping.inputs[0])
diff=nt.nodes.new('ShaderNodeTexImage');diff.image=image(ASSETS/'brown_leather/brown_leather_diff_2k.jpg');diff.projection='BOX';diff.projection_blend=.25
nt.links.new(mapping.outputs[0],diff.inputs['Vector'])
tint=nt.nodes.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(.23,.24,.27,1)
nt.links.new(diff.outputs['Color'],tint.inputs[1]);nt.links.new(tint.outputs[0],p.inputs['Base Color'])
rough=nt.nodes.new('ShaderNodeTexImage');rough.image=image(ASSETS/'brown_leather/brown_leather_rough_2k.jpg',True);rough.projection='BOX';rough.projection_blend=.2
nt.links.new(mapping.outputs[0],rough.inputs['Vector'])
remap=nt.nodes.new('ShaderNodeMapRange');remap.inputs['To Min'].default_value=.25;remap.inputs['To Max'].default_value=.48
nt.links.new(rough.outputs['Color'],remap.inputs['Value']);nt.links.new(remap.outputs['Result'],p.inputs['Roughness'])
bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.17;bump.inputs['Distance'].default_value=.0008
nt.links.new(rough.outputs['Color'],bump.inputs['Height']);nt.links.new(bump.outputs[0],p.inputs['Normal'])
p.inputs['Coat Weight'].default_value=.12;p.inputs['Coat Roughness'].default_value=.36

thread=material('Leather edge piping',(.055,.033,.019),.58)
wrinkle=bpy.data.textures.new('Subtle upholstery settling',type='CLOUDS');wrinkle.noise_scale=.12;wrinkle.noise_depth=2
for o in list(bpy.data.objects['Foreground leather sofa'].children):
    if 'cushion' in o.name.lower():
        sub=o.modifiers.new('Editable cushion softness','SUBSURF');sub.levels=2;sub.render_levels=3
        disp=o.modifiers.new('Small natural cushion variation','DISPLACE');disp.texture=wrinkle;disp.strength=.0025;disp.texture_coords='GLOBAL'
        for face in o.data.polygons:face.use_smooth=True
        if 'seat' in o.name.lower():
            o.rotation_euler[2]=random.uniform(-.015,.015)
            w,d=.89,.72;z=o.location.z+.052
            pts=[]
            for cx,cy,start in [(w/2-.055,d/2-.055,0),(-w/2+.055,d/2-.055,90),(-w/2+.055,-d/2+.055,180),(w/2-.055,-d/2+.055,270)]:
                for k in range(7):
                    a=math.radians(start+k*15)
                    pts.append((o.location.x+cx+.055*math.cos(a),o.location.y+cy+.055*math.sin(a),z))
        else:
            pts=[]
            for cx,cz,start in [(.40,.185,0),(-.40,.185,90),(-.40,-.185,180),(.40,-.185,270)]:
                for k in range(7):
                    a=math.radians(start+k*15)
                    pts.append((o.location.x+cx+.04*math.cos(a),o.location.y-.094,o.location.z+cz+.04*math.sin(a)))
        seam=path('Editable upholstery piping',pts,.0028,thread,True);seam.parent=o.parent

# Give the central chair a curved, genuinely see-through woven back.
chair=bpy.data.objects['Central ergonomic chair']
for o in list(chair.children):
    if o.name.startswith(('Lumbar cushion','Back mesh panel')):hide(o)
meshmat=material('Ergonomic chair fine woven mesh',(.016,.021,.025),.68)
nt=meshmat.node_tree;p=nt.nodes['Principled BSDF'];out=nt.nodes['Material Output']
uv=nt.nodes.new('ShaderNodeTexCoord');sep=nt.nodes.new('ShaderNodeSeparateXYZ');nt.links.new(uv.outputs['UV'],sep.inputs[0])
thread_masks=[]
for axis in ['X','Y']:
    mul=nt.nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=145 if axis=='X' else 175
    fract=nt.nodes.new('ShaderNodeMath');fract.operation='FRACT'
    less=nt.nodes.new('ShaderNodeMath');less.operation='LESS_THAN';less.inputs[1].default_value=.30
    nt.links.new(sep.outputs[axis],mul.inputs[0]);nt.links.new(mul.outputs[0],fract.inputs[0]);nt.links.new(fract.outputs[0],less.inputs[0]);thread_masks.append(less)
maximum=nt.nodes.new('ShaderNodeMath');maximum.operation='MAXIMUM';nt.links.new(thread_masks[0].outputs[0],maximum.inputs[0]);nt.links.new(thread_masks[1].outputs[0],maximum.inputs[1])
transparent=nt.nodes.new('ShaderNodeBsdfTransparent');mix=nt.nodes.new('ShaderNodeMixShader');nt.links.new(maximum.outputs[0],mix.inputs[0]);nt.links.new(transparent.outputs[0],mix.inputs[1]);nt.links.new(p.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],out.inputs['Surface'])
verts=[];faces=[];nx,nz=18,24
for j in range(nz+1):
    v=j/nz;z=.72+v*.60
    for i in range(nx+1):
        u=i/nx;x=(u-.5)*.48*(.94+.06*math.sin(v*math.pi));y=-.23-.06*math.sin(v*math.pi)+.07*(abs(u-.5)*2)**2
        verts.append((x,y,z))
for j in range(nz):
    for i in range(nx):
        a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
me=bpy.data.meshes.new('Curved ergonomic mesh surface');me.from_pydata(verts,[],faces);me.update()
layer=me.uv_layers.new(name='Woven fabric coordinates')
for polygon in me.polygons:
    for loop_index in polygon.loop_indices:
        vi=me.loops[loop_index].vertex_index;layer.data[loop_index].uv=((vi%(nx+1))/nx,(vi//(nx+1))/nz)
    polygon.use_smooth=True
o=bpy.data.objects.new('Editable woven chair back',me);COL.objects.link(o);o.parent=chair;o.data.materials.append(meshmat)
outline=[(-.235,-.16,.72),(-.24,-.17,1.25),(-.18,-.20,1.33),(.18,-.20,1.33),(.24,-.17,1.25),(.235,-.16,.72)]
o=path('Ergonomic back perimeter frame',outline,.019,black,True);o.parent=chair
o=path('Ergonomic adjustable spine',[(0,-.32,.55),(0,-.34,.9),(0,-.29,1.28)],.019,black);o.parent=chair

# Restrained photographed wood response over the authored walnut palette.
woodrough=image(ASSETS/'wood_cabinet_worn_long/wood_cabinet_worn_long_rough_2k.jpg',True)
wooddiff=image(ASSETS/'wood_cabinet_worn_long/wood_cabinet_worn_long_diff_2k.jpg')
for m in [walnut]+[m for m in bpy.data.materials if m.name.startswith('Floor walnut plank variation')]:
    nt=m.node_tree;p=nt.nodes['Principled BSDF']
    oldcolor=p.inputs['Base Color'].links[0].from_socket if p.inputs['Base Color'].is_linked else None
    coord=nt.nodes.new('ShaderNodeTexCoord')
    rough=nt.nodes.new('ShaderNodeTexImage');rough.image=woodrough;rough.projection='BOX';rough.projection_blend=.2
    nt.links.new(coord.outputs['Generated'],rough.inputs['Vector'])
    remap=nt.nodes.new('ShaderNodeMapRange');remap.inputs['To Min'].default_value=.29;remap.inputs['To Max'].default_value=.43
    nt.links.new(rough.outputs['Color'],remap.inputs['Value']);nt.links.new(remap.outputs['Result'],p.inputs['Roughness'])
    bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.15;bump.inputs['Distance'].default_value=.0007
    nt.links.new(rough.outputs['Color'],bump.inputs['Height']);nt.links.new(bump.outputs[0],p.inputs['Normal'])
    photo=nt.nodes.new('ShaderNodeTexImage');photo.image=wooddiff;photo.projection='BOX';photo.projection_blend=.2;nt.links.new(coord.outputs['Generated'],photo.inputs['Vector'])
    blend=nt.nodes.new('ShaderNodeMixRGB');blend.blend_type='MIX';blend.inputs[0].default_value=.13
    if oldcolor:nt.links.new(oldcolor,blend.inputs[1])
    else:blend.inputs[1].default_value=(.11,.06,.025,1)
    nt.links.new(photo.outputs['Color'],blend.inputs[2]);nt.links.new(blend.outputs[0],p.inputs['Base Color'])
    if m.name.startswith('Floor'):
        ramp=next(n for n in nt.nodes if n.type=='VALTORGB')
        factor=.96+random.random()*.08
        ramp.color_ramp.elements[0].color=(.06*factor,.032*factor,.016*factor,1)
        ramp.color_ramp.elements[1].color=(.25*factor,.135*factor,.06*factor,1)

rug=bpy.data.materials['Warm charcoal woven rug'];nt=rug.node_tree;p=nt.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(.060,.064,.062,1)
tc=nt.nodes.new('ShaderNodeTexCoord');patch=nt.nodes.new('ShaderNodeTexNoise');patch.inputs['Scale'].default_value=5;patch.inputs['Detail'].default_value=1
nt.links.new(tc.outputs['Generated'],patch.inputs['Vector']);ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.035,.038,.037,1);ramp.color_ramp.elements[1].color=(.13,.125,.11,1)
nt.links.new(patch.outputs['Fac'],ramp.inputs[0]);nt.links.new(ramp.outputs[0],p.inputs['Base Color'])

# Append mesh data only; relink source textures and retain direct editability.
cache={}

def _relink_node_image(node, asset):
    if node.type != 'TEX_IMAGE' or not node.image:
        return
    candidate = ASSETS / asset / 'textures' / Path(node.image.filepath.replace('\\', '/')).name
    if candidate.exists():
        node.image.filepath = str(candidate)
        node.image.reload()
    if any(s in node.image.name.lower() for s in ['rough', 'metal', 'nor_', 'alpha', 'arm']):
        node.image.colorspace_settings.name = 'Non-Color'

def _relink_material_textures(material, asset):
    if not material or not material.use_nodes:
        return
    for node in material.node_tree.nodes:
        _relink_node_image(node, asset)

def _prepare_asset_object(obj, asset):
    world = obj.matrix_world.copy()
    obj.parent = None
    obj.matrix_world = world
    obj.animation_data_clear()
    for mat in obj.data.materials:
        _relink_material_textures(mat, asset)

def _load_asset(asset):
    source = ASSETS / asset / (asset + '_1k.blend')
    with bpy.data.libraries.load(str(source), link=False) as (src, dst):
        dst.objects = src.objects
    obs = [o for o in dst.objects if o and o.type == 'MESH']
    for o in obs:
        _prepare_asset_object(o, asset)
    points = [o.matrix_world @ Vector(corner) for o in obs for corner in o.bound_box]
    low = Vector(tuple(min(p[a] for p in points) for a in range(3)))
    high = Vector(tuple(max(p[a] for p in points) for a in range(3)))
    return obs, low, high

def asset_instance(asset,name,loc,height,rotation=0,slender=1):
    if asset not in cache:
        cache[asset] = _load_asset(asset)
    obs,low,high=cache[asset]
    root=bpy.data.objects.new(name,None);COL.objects.link(root);root.location=loc;root.rotation_euler[2]=rotation
    scale=height/(high.z-low.z);root.scale=(scale*slender,scale*slender,scale)
    center=Vector(((low.x+high.x)/2,(low.y+high.y)/2,low.z))
    for src in obs:
        o = src.copy()
        o.data = src.data
        COL.objects.link(o)
        o.name = name + ' / ' + src.name
        o.parent = root
        o.matrix_basis = Matrix.Translation(-center) @ src.matrix_world
        o.hide_render = False
        o.hide_set(False)
    return root
hide_tree(bpy.data.objects['Foreground lounge chair'])
asset_instance('mid_century_lounge_chair','Detailed leather lounge chair',(4.85,-3.25,.04),1.25,-.35)

collection('12_REFINED_PLANTS')
for o in list(bpy.data.collections['07_LOUNGE_AND_PLANTS'].objects):
    if o.name.startswith('Studio plant'):hide(o)
for i,(x,y,h) in enumerate([(-10.9,-.55,1.7),(-6.07,3.0,1.55),(-2.75,3.6,1.85),(2.76,3.5,1.95),(7.14,3.7,1.65),(11.15,-.35,1.8)]):
    asset_instance('potted_plant_02',f'Broadleaf floor plant {i+1:02}',(x,y,.035),h,i*1.12,.72)
for i,(x,y,z,h) in enumerate([(.58,-2.85,.42,.34),(-1.76,2.9,.82,.28),(-3.28,4.44,1.74,.38),(6.6,4.5,2.94,.35)]):
    asset_instance('potted_plant_04',f'Detailed succulent {i+1:02}',(x,y,z),h,i*.8)

def _create_leaflet(name, base, wing, az, side, root):
    a = az + side * 1.05
    d = Vector((math.cos(a), math.sin(a), -.28))
    cross = Vector((-math.sin(a), math.cos(a), 0))
    verts = []
    for k in range(6):
        u = k / 5
        point = base + d * wing * u + Vector((0, 0, .04 * math.sin(u * math.pi)))
        w = .018 * math.sin(u * math.pi)
        verts.extend([tuple(point - cross * w), tuple(point + cross * w)])
    faces = [(k * 2, k * 2 + 1, k * 2 + 3, k * 2 + 2) for k in range(5)]
    me = bpy.data.meshes.new(name + ' leaflet mesh')
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name + ' separate leaflet', me)
    COL.objects.link(ob)
    ob.data.materials.append(leaf)
    ob.parent = root
    for p in me.polygons:
        p.use_smooth = True

def _create_frond(name, az, length, start, root):
    def center(t):
        return start + Vector((
            math.cos(az) * length * t,
            math.sin(az) * length * t,
            math.sin(t * math.pi) * length * .25 - length * t * .3
        ))
    stem = path(name + ' arching frond', [tuple(center(i / 7)) for i in range(8)], .006, stemmat)
    stem.parent = root
    for j in range(16):
        t = .12 + j * .05
        base = center(t)
        wing = length * .22 * math.sin(t * math.pi)
        for side in [-1, 1]:
            _create_leaflet(name, base, wing, az, side, root)

def palm(name, x, y, h):
    root = bpy.data.objects.new(name, None)
    COL.objects.link(root)
    pot = tube(name + ' tall stoneware pot', (x, y, .035), (x, y, .48), .22, ceramic, .27, 48)
    pot.parent = root
    trunk = path(name + ' stem', [(x, y, .40), (x + .03, y, h * .65), (x, y, h * .87)], .018, stemmat)
    trunk.parent = root
    for frond in range(11):
        az = frond * 2.399
        length = h * (.37 + .15 * random.random())
        start = Vector((x, y, h * (.72 + .22 * random.random())))
        _create_frond(name, az, length, start, root)
    return root
palm('Left accent palm',-11.12,1.8,2.25)
palm('Engineering accent palm',6.93,4.1,2.25)

collection('13_REFINED_EXTERIOR')
for o in bpy.data.collections['08_EXTERIOR'].objects:
    if o.name.startswith(('Distant sky backdrop','Editable distant mountain silhouette')):hide(o)

env=image(ASSETS/'qwantani_dusk_2_puresky/qwantani_dusk_2_puresky_2k.hdr',True)
world=scene.world;world.use_nodes=True;nt=world.node_tree;nt.nodes.clear()
out=nt.nodes.new('ShaderNodeOutputWorld');tc=nt.nodes.new('ShaderNodeTexCoord');mapping=nt.nodes.new('ShaderNodeMapping');mapping.inputs['Rotation'].default_value[2]=math.radians(92)
nt.links.new(tc.outputs['Generated'],mapping.inputs['Vector'])
hdr=nt.nodes.new('ShaderNodeTexEnvironment');hdr.image=env;nt.links.new(mapping.outputs['Vector'],hdr.inputs['Vector'])
lightbg=nt.nodes.new('ShaderNodeBackground');lightbg.inputs['Strength'].default_value=.12;nt.links.new(hdr.outputs['Color'],lightbg.inputs['Color'])
visiblebg=nt.nodes.new('ShaderNodeBackground');visiblebg.inputs['Strength'].default_value=.45;nt.links.new(hdr.outputs['Color'],visiblebg.inputs['Color'])
ray=nt.nodes.new('ShaderNodeLightPath');mix=nt.nodes.new('ShaderNodeMixShader');nt.links.new(ray.outputs['Is Camera Ray'],mix.inputs[0]);nt.links.new(lightbg.outputs[0],mix.inputs[1]);nt.links.new(visiblebg.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],out.inputs[0])

def terrain_material(name,base,snowheight):
    m=material(name,base,.86,0,.018)
    nt=m.node_tree;p=nt.nodes['Principled BSDF'];coord=nt.nodes.new('ShaderNodeTexCoord');sep=nt.nodes.new('ShaderNodeSeparateXYZ');nt.links.new(coord.outputs['Object'],sep.inputs[0])
    noise_tex=nt.nodes.new('ShaderNodeTexNoise');noise_tex.inputs['Scale'].default_value=.75;noise_tex.inputs['Detail'].default_value=5;noise_tex.inputs['Roughness'].default_value=.8
    nt.links.new(coord.outputs['Object'],noise_tex.inputs[0])
    relief=nt.nodes.new('ShaderNodeBump');relief.inputs['Strength'].default_value=.38;relief.inputs['Distance'].default_value=.15;nt.links.new(noise_tex.outputs['Fac'],relief.inputs['Height']);nt.links.new(relief.outputs[0],p.inputs['Normal'])
    mul=nt.nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=3.8;nt.links.new(noise_tex.outputs['Fac'],mul.inputs[0])
    add=nt.nodes.new('ShaderNodeMath');add.operation='ADD';nt.links.new(sep.outputs['Z'],add.inputs[0]);nt.links.new(mul.outputs[0],add.inputs[1])
    snow=nt.nodes.new('ShaderNodeMapRange');snow.inputs['From Min'].default_value=snowheight;snow.inputs['From Max'].default_value=snowheight+2.4;nt.links.new(add.outputs[0],snow.inputs['Value'])
    mix=nt.nodes.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(*base,1);mix.inputs[2].default_value=(.46,.51,.61,1);nt.links.new(snow.outputs[0],mix.inputs[0]);nt.links.new(mix.outputs[0],p.inputs['Base Color'])
    return m

terrain_names=[]
for layer,(center,span,height,base,col) in enumerate([(205,90,22,-8,(.12,.16,.23)),(138,64,12,-7,(.065,.095,.15)),(91,40,6,-5,(.028,.05,.085))]):
    verts=[];faces=[];nx,ny=340,84;width=430
    for j in range(ny+1):
        y=center-span/2+j*span/ny
        for i in range(nx+1):
            x=-width/2+i*width/nx;v=Vector((x*.027,y*.045,layer*2.7))
            ridge=1-abs(noise.noise(v));detail=0
            for octave in range(4):detail+=(1-abs(noise.noise(v*(2**octave))))/(2**octave)
            envelope=math.exp(-((y-center)/(span*.29))**2)
            main=.38+.22*math.sin(x*.048+layer*1.7)+.22*ridge+.12*detail
            peak=math.exp(-((x+5-layer*14)/24)**2)*.32+math.exp(-((x-80)/21)**2)*.21
            z=base+height*envelope*(main+peak)+noise.noise(Vector((x*.34,y*.34,layer)))*.17
            verts.append((x,y,z))
    for j in range(ny):
        for i in range(nx):
            a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
    me=bpy.data.meshes.new('Alpine terrain heightfield mesh');me.from_pydata(verts,[],faces);me.update()
    ob=bpy.data.objects.new(f'Editable alpine range {layer+1:02}',me);COL.objects.link(ob);ob.data.materials.append(terrain_material('Alpine rock and broken snow '+str(layer),col,6.5 if layer==0 else 15))
    for p in me.polygons:p.use_smooth=True
    terrain_names.append(ob.name)
sun=bpy.data.lights.new('Blue-hour distant mountain rim','SUN');sun.energy=.55;sun.angle=.15;sun.color=(.42,.55,1)
ob=bpy.data.objects.new(sun.name,sun);COL.objects.link(ob);ob.rotation_euler=(math.radians(48),math.radians(-25),math.radians(-35))

# Render genuine landscape artwork from the new exterior and pack it into the monitors.
collection('14_SCREEN_ARTWORK')
data=bpy.data.cameras.new('Landscape artwork source camera');data.lens=44
artcam=bpy.data.objects.new(data.name,data);COL.objects.link(artcam);artcam.location=(0,12,3.0);artcam.rotation_euler=(Vector((0,150,5.0))-artcam.location).to_track_quat('-Z','Y').to_euler()
hero=scene.camera
visibility={c.name:c.hide_render for c in scene.collection.children}
for c in scene.collection.children:
    if c.name not in ['08_EXTERIOR','13_REFINED_EXTERIOR','14_SCREEN_ARTWORK']:c.hide_render=True
scene.camera=artcam;scene.render.resolution_x=1024;scene.render.resolution_y=384;scene.cycles.samples=24
scene.render.filepath=str(ROOT/'screen-landscape-v003.png');bpy.ops.render.render(write_still=True)
for name,state in visibility.items():bpy.data.collections[name].hide_render=state
scene.camera=hero
screen_image=image(ROOT/'screen-landscape-v003.png')
screen_material=material('Rendered mountain landscape display',(.1,.1,.1),.5)
nt=screen_material.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Strength'].default_value=.65
tex=nt.nodes.new('ShaderNodeTexImage');tex.image=screen_image;nt.links.new(tex.outputs['Color'],em.inputs['Color']);nt.links.new(em.outputs[0],out.inputs[0])
for o in list(scene.objects):
    if 'layered mountain' in o.name:hide(o)
def display_plane(name,x,y,z,w,h):
    me=bpy.data.meshes.new(name+' mesh');me.from_pydata([(x-w/2,y,z-h/2),(x+w/2,y,z-h/2),(x+w/2,y,z+h/2),(x-w/2,y,z+h/2)],[],[(0,1,2,3)]);me.update()
    uv=me.uv_layers.new()
    for i,co in enumerate([(0,0),(1,0),(1,1),(0,1)]):uv.data[i].uv=co
    o=bpy.data.objects.new(name,me);COL.objects.link(o);o.data.materials.append(screen_material)
display_plane('Hero monitor landscape artwork',0,3.02-.054,1.66,2.79,.91)
display_plane('Projects monitor landscape artwork',9.45,4.55-.054,1.85,2.29,1.24)

scene.cycles.samples=96;scene.cycles.adaptive_threshold=.015
scene.render.resolution_x=1920;scene.render.resolution_y=540
scene.camera=hero;hero.data.dof.use_dof=False
assert all(abs(a-b)<1e-6 for rowa,rowb in zip(baseline_camera,hero.matrix_world) for a,b in zip(rowa,rowb)), 'Hero camera changed'
assert all(len(bpy.data.collections[name].objects)>=count for name,count in baseline_zones.items())

prefs=bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
scene.cycles.device='GPU' if any(d.use for d in prefs.devices) else 'CPU'
scene.render.filepath=str(ROOT/'kinetic-studio-proof-v003.png')
scene['refinement_revision']='v003'
scene['asset_provenance']='Poly Haven CC0 models, maps, and dusk HDRI; full source URLs, authors, and checksums in assets/asset-provenance.json.'
scene['proof_limitations']='Anatomy and technical displays remain schematic. Exterior terrain is artist-authored, not a geographic reconstruction. Hero camera is an inferred fit.'
bpy.ops.file.pack_all()
missing=[im.name for im in bpy.data.images if im.source=='FILE' and not im.packed_file and not Path(bpy.path.abspath(im.filepath)).is_file()]
assert not missing,missing
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'kinetic-studio-proof-v003.blend'))
t=time.time();bpy.ops.render.render(write_still=True)
report=json.loads((ROOT/'proof-verification.json').read_text(encoding='utf-8-sig'))
report.update(revision='v003',status='rendered-awaiting-visual-review',render_seconds=round(time.time()-t,2),resolution=[1920,540],samples=96,objects=len(scene.objects),materials=len(bpy.data.materials),blend=str(ROOT/'kinetic-studio-proof-v003.blend'),render=scene.render.filepath)
report['collections']={c.name:len(c.objects) for c in scene.collection.children}
report['mesh_objects']=sum(o.type=='MESH' for o in scene.objects)
report['asset_provenance']='Authored studio and terrain plus selected Poly Haven CC0 assets; see assets/asset-provenance.json for source URLs, authors, and checksums.'
report['devices']=[{'name':d.name,'type':d.type,'enabled':bool(d.use)} for d in prefs.devices]
report.pop('total_seconds',None)
report['refinement']={'hero_camera_unchanged':True,'original_zone_collections_preserved':True,'packed_file_images':sum(bool(i.packed_file) for i in bpy.data.images),'missing_images':missing,'terrain_meshes':terrain_names,'licensed_assets':list(json.loads((ASSETS/'asset-provenance.json').read_text())['assets'])}
report['limitations']=scene['proof_limitations']
(ROOT/'proof-verification-v003.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('KINETIC_REFINEMENT_V003_RENDERED',report['render_seconds'],len(scene.objects),flush=True)
