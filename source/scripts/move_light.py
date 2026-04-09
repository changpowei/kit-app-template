import random
import omni.usd
from pxr import UsdGeom, Gf


def move_light():
    stage = omni.usd.get_context().get_stage()
    prim = stage.GetPrimAtPath("/Root/MovableRectLight_Xform")
    xformable = UsdGeom.Xformable(prim)

    # Get current translation
    current_ops = xformable.GetOrderedXformOps()
    translate_op = None
    for op in current_ops:
        if op.GetOpType() == UsdGeom.XformOp.TypeTranslate:
            translate_op = op
            break

    if translate_op:
        current = translate_op.Get()
        new_x = random.uniform(-20, 0)
        translate_op.Set(Gf.Vec3d(new_x, current[1], current[2]))
    else:
        translate_op = xformable.AddTranslateOp()
        new_x = random.uniform(-20, 0)
        translate_op.Set(Gf.Vec3d(new_x, 0, 0))

    print(f"Moved light to x={new_x:.2f}")


move_light()
