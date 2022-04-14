import hou

selection = hou.selectedNodes()
node = hou.node('/obj')

def create_camera(alembic):
    if alembic.type().name() == 'alembicxform':
        return node.createNode('cam', alembic.name() + '_bake')
    else:
        raise TypeError('Input is not an alembic\nNode type: ' + str(alembic.type()))

def keyframe_parms(source, dest):
    cur_frame = hou.intFrame()

    hou.setFrame(int(hou.playbar.playbackRange()[0]))
    for f in range(int(hou.playbar.playbackRange()[0]), int(hou.playbar.playbackRange()[1])+1, 1):
        hou.setFrame(f)
       
        worldTransform = source.worldTransform()
        set_transform(worldTransform, dest)
        
        set_camera_parms(source, dest)

    hou.setFrame(cur_frame)

def set_transform(worldTransform, dest):
    dest.setWorldTransform(worldTransform)
    
    tx = dest.parm('tx').eval()
    ty = dest.parm('ty').eval()
    tz = dest.parm('tz').eval()
    rx = dest.parm('rx').eval()
    ry = dest.parm('ry').eval()
    rz = dest.parm('rz').eval()
    
    dest.parm('tx').setKeyframe(hou.Keyframe(tx))
    dest.parm('ty').setKeyframe(hou.Keyframe(ty))
    dest.parm('tz').setKeyframe(hou.Keyframe(tz))

    dest.parm('rx').setKeyframe(hou.Keyframe(rx))
    dest.parm('ry').setKeyframe(hou.Keyframe(ry))
    dest.parm('rz').setKeyframe(hou.Keyframe(rz))

def set_camera_parms(source, dest):
    try:
        focal = source.parm('focal').eval()
        aperture = source.parm('aperture').eval()
        near = source.parm('near').eval()
        far = source.parm('far').eval()
        resx = source.parm('resx').eval()
        resy = source.parm('resy').eval()
        winsizex = source.parm('winsizex').eval()
        winsizey = source.parm('winsizey').eval()
        shutter = source.parm('shutter').eval()
        aspect = source.parm('aspect').eval()
    except:
        for ch in source.children():
            if ch.type().name() == 'cam':
                src_cam = ch
                break
        focal = src_cam.parm('focal').eval()
        aperture = src_cam.parm('aperture').eval()
        near = src_cam.parm('near').eval()
        far = src_cam.parm('far').eval()
        resx = src_cam.parm('resx').eval()
        resy = src_cam.parm('resy').eval()
        winsizex = src_cam.parm('winsizex').eval()
        winsizey = src_cam.parm('winsizey').eval()
        shutter = src_cam.parm('shutter').eval()
        aspect = src_cam.parm('aspect').eval()
    
    dest.parm('focal').setKeyframe(hou.Keyframe(focal))
    dest.parm('aperture').setKeyframe(hou.Keyframe(aperture))
    dest.parm('near').setKeyframe(hou.Keyframe(near))
    dest.parm('far').setKeyframe(hou.Keyframe(far))
    dest.parm('resx').setKeyframe(hou.Keyframe(resx))
    dest.parm('resy').setKeyframe(hou.Keyframe(resy))
    dest.parm('winsizex').setKeyframe(hou.Keyframe(winsizex))
    dest.parm('winsizey').setKeyframe(hou.Keyframe(winsizey))
    dest.parm('shutter').setKeyframe(hou.Keyframe(shutter))
    dest.parm('aspect').setKeyframe(hou.Keyframe(aspect))
    
for n in selection:
    new_cam = create_camera(n)
    keyframe_parms(n, new_cam)