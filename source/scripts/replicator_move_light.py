import asyncio
import random
import omni.usd
import omni.replicator.core as rep
from pxr import UsdGeom, Gf, Usd

stage = omni.usd.get_context().get_stage()

# 清除舊的 MovableRectLight
for prim in stage.GetPrimAtPath("/Root").GetChildren():
    if prim.GetName().startswith("MovableRectLight"):
        stage.RemovePrim(prim.GetPath())
        print(f"Removed old prim: {prim.GetPath()}")

with rep.new_layer():
    moveable_light = rep.create.light(
        light_type="rect",
        name="MovableRectLight",
        parent="/Root",
        color=(1.0, 0, 0),
        intensity=100000,
        position=(0, 0, 2),
    )

camera = rep.create.camera(position=(-25, -15, 6), look_at=(-11, 0, 0))

# 修正相機曝光參數（對齊 Viewport 相機設定，避免過曝）
cam_prim = stage.GetPrimAtPath("/Replicator/Camera_Xform/Camera")
if cam_prim:
    cam_prim.GetAttribute("exposure:fStop").Set(5.0)
    cam_prim.GetAttribute("exposure:time").Set(0.02)
    cam_prim.GetAttribute("exposure:responsivity").Set(1.1)
    print("Camera exposure adjusted: fStop=5.0, time=0.02")

render_product = rep.create.render_product(camera, (1024, 768))

writer = rep.writers.get("BasicWriter")
writer.initialize(
    output_dir="/home/c95cpw/omniverse/kit-app-template/output/Replicator_Agent",
    rgb=True,
    normals=True,
    distance_to_image_plane=True,
    semantic_segmentation=True,
    colorize_depth=True,
)
writer.attach([render_product])


def move_light(stage: Usd.Stage) -> None:
    """Move the light randomly between 0 and -20 meters on the x axis."""
    prim = stage.GetPrimAtPath("/Root/MovableRectLight_Xform")
    if not prim:
        print("Light prim not found!")
        return

    xformable = UsdGeom.Xformable(prim)
    translate_op = None
    for op in xformable.GetOrderedXformOps():
        if op.GetOpType() == UsdGeom.XformOp.TypeTranslate:
            translate_op = op
            break

    new_x = random.uniform(-20, 0)
    if translate_op:
        current = translate_op.Get()
        translate_op.Set(Gf.Vec3d(new_x, current[1], current[2]))
    else:
        translate_op = xformable.AddTranslateOp()
        translate_op.Set(Gf.Vec3d(new_x, 0, 2))

    print(f"  Moved light to X={new_x:.2f}")


async def go(num_frames=10):
    await asyncio.sleep(2)
    for i in range(num_frames):
        move_light(stage)
        await rep.orchestrator.step_async()
        await asyncio.sleep(0.5)
        print(f"Frame {i + 1}/{num_frames} captured")

asyncio.ensure_future(go())
