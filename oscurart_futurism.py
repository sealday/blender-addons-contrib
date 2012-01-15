bl_info = {
    "name": "Futurism",
    "author": "Oscurart",
    "version": (1, 1),
    "blender": (2, 5, 9),
    "api": 40900,
    "location": "Object > Futurism",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}


import bpy

def object_osc_futurism (self, context,STEP, HOLD):
    ACTOBJ=bpy.context.active_object # OBJETO ACTIVO
    FS=bpy.context.scene.frame_start # FRAME START
    FE=bpy.context.scene.frame_end # FRAME END
    OBJLIST=[] # LISTA PARA OBJETOS ????
    FC=FS # FRAME CURRENT
    OBJNUMBER=1 # SUFIJO DE NUMERO PARA OBJETOS
    STEPINC=0 # NUMERO PARA EVALUAR LOS PASOS    
    # SETEO EL FRAME CURRENT
    bpy.context.scene.frame_set(FS)  
    
    OBACT = bpy.context.active_object
    
    ## CREO EMPTY
    bpy.ops.object.add()
    bpy.context.active_object.name = "FuturismContainer"
    EMPTY = bpy.context.active_object
    
    bpy.context.scene.objects.active = OBACT  
    
    for OBJETO in range((FE+1)-FS):
        if STEPINC == STEP:
            # CREO UN MESH A PARTIR DE OBJETO
            MESH=ACTOBJ.to_mesh(bpy.context.scene, True, 'PREVIEW')
            # CREO OBJETO
            OBJECT=bpy.data.objects.new(ACTOBJ.name[:3]+str(FC), MESH)
            # CONECTO A LA ESCENA
            bpy.context.scene.objects.link(OBJECT)
            # SETEO FRAME CURRENT
            bpy.context.scene.frame_set(FC)
            # MARCO EXPRESIONES PARA VIEW
            OBJECT.driver_add("hide")
            OBJECT.animation_data.drivers[0].driver.variables.new()
            OBJECT.animation_data.drivers[0].driver.expression= "False if bpy.context.scene.frame_current >= "+str(FC)+" and bpy.context.scene.frame_current <= "+str(FC+HOLD)+" else True"
            OBJECT.animation_data.drivers[0].driver.variables[0].targets[0].id_type = 'SCENE'
            OBJECT.animation_data.drivers[0].driver.variables[0].targets[0].id= bpy.context.scene
            OBJECT.animation_data.drivers[0].driver.variables[0].targets[0].data_path = "current_frame"
            # MARCO EXPRESIONES PARA RENDER
            OBJECT.driver_add("hide_render")
            OBJECT.animation_data.drivers[1].driver.variables.new()
            OBJECT.animation_data.drivers[1].driver.expression= "False if bpy.context.scene.frame_current >= "+str(FC)+" and bpy.context.scene.frame_current <= "+str(FC+HOLD)+" else True"
            OBJECT.animation_data.drivers[1].driver.variables[0].targets[0].id_type = 'SCENE'
            OBJECT.animation_data.drivers[1].driver.variables[0].targets[0].id= bpy.context.scene
            OBJECT.animation_data.drivers[1].driver.variables[0].targets[0].data_path = "current_frame"            
            # RESETEO STEPINC
            STEPINC=0
            # COPIAMOS S R T
            OBJECT.location=ACTOBJ.location
            OBJECT.rotation_euler=ACTOBJ.rotation_euler
            OBJECT.scale=ACTOBJ.scale
            #EMPARENTO
            OBJECT.parent=EMPTY
        # AVANZO STEP Y FRAME
        FC+=1
        STEPINC+=1
        
    

# CLASE PARA OPERADOR
class Oscurart_futurism (bpy.types.Operator):
    bl_idname = "object.duplicate_futurism"
    bl_label = "Duplicate Futurism"
    bl_description = "Duplicate object per frame"
    bl_options = {'REGISTER', 'UNDO'}

    scale = bpy.props.IntProperty(name='Step',default=1, min=1, max=1000)
    
    hold = bpy.props.IntProperty(name='Hold', default=0, min=0)

    def execute(self, context):
        object_osc_futurism(self, context, self.scale, self.hold)

        return {'FINISHED'}


# Registration

def add_osc_futurism_button(self, context):
    self.layout.operator(
        Oscurart_futurism.bl_idname,
        text="Futurism",
        icon="PLUGIN")


def register():
    bpy.utils.register_class(Oscurart_futurism)
    bpy.types.VIEW3D_MT_object.append(add_osc_futurism_button)


def unregister():
    bpy.utils.unregister_class(Oscurart_futurism)
    bpy.types.VIEW3D_MT_object.remove(add_osc_futurism_button)


if __name__ == '__main__':
    register()