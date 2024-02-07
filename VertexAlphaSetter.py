bl_info = {
    "name": "Vertex Color Setter",
    "author": "Noxel Foxel",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Tools",
    "description": "Paints Vertex Colors including Alpha",
    "doc_url": "https://github.com/NoxelFoxel/VertexColorSetter.git",
    "category": "Vertex Paint",
}

import bpy
import bmesh


def set_vertex_color(color):
    obj = bpy.context.active_object
    if obj.mode != 'EDIT':
        bpy.ops.object.mode_set(mode='EDIT')
    mesh = obj.data
    bm = bmesh.from_edit_mesh(mesh)

    if not bm.loops.layers.color:
        col_layer = bm.loops.layers.color.new("Col")
    else:
        col_layer = bm.loops.layers.color.active

    selected_verts = [v for v in bm.verts if v.select]
    for vert in selected_verts:
        for loop in vert.link_loops:
            # Make sure the color assignment is compatible
            loop[col_layer] = (color[0], color[1], color[2], color[3])  # Explicitly unpack RGBA

    bmesh.update_edit_mesh(mesh)
    bpy.ops.object.mode_set(mode='OBJECT')


class SetVertexColorOperator(bpy.types.Operator):
    bl_idname = "object.set_vertex_color"
    bl_label = "Set Vertex Color"

    def execute(self, context):
        # Retrieve RGBA color including alpha from the color picker
        color = context.scene.color_value
        set_vertex_color((color[0], color[1], color[2], color[3]))  # Pass RGBA
        return {'FINISHED'}


class VIEW3D_PT_VertexColorSetter(bpy.types.Panel):
    bl_label = "Vertex Color Setter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, 'color_value', text="Color and Alpha")
        layout.operator("object.set_vertex_color")


def register():
    bpy.utils.register_class(SetVertexColorOperator)
    bpy.utils.register_class(VIEW3D_PT_VertexColorSetter)
    bpy.types.Scene.color_value = bpy.props.FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0, 1.0),
        size=4,
        min=0.0, max=1.0,
        description="Set Vertex Color and Alpha"
    )


def unregister():
    bpy.utils.unregister_class(SetVertexColorOperator)
    bpy.utils.unregister_class(VIEW3D_PT_VertexColorSetter)
    del bpy.types.Scene.color_value


if __name__ == "__main__":
    register()
