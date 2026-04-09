import asyncio
import random
import omni.usd
import omni.replicator.core as rep
from pxr import Usd, UsdGeom, Sdf

stage = omni.usd.get_context().get_stage()

# 先將所有倉庫燈恢復為可見
for i in range(7):
    suffix = "" if i == 0 else f"_{i:02d}"
    path = f"/Root/Warehouse/Lights/RectLight{suffix}"
    prim = stage.GetPrimAtPath(path)
    if prim:
        prim.GetAttribute("visibility").Set(UsdGeom.Tokens.inherited)
        print(f"Restored: {path}")

camera = "/OmniverseKit_Persp"
render_product = rep.create.render_product(camera, (1024, 1024))

writer = rep.writers.get("BasicWriter")
writer.initialize(
    output_dir="/home/c95cpw/omniverse/kit-app-template/output/Replicator_Toggle",
    rgb=True,
    normals=True,
    distance_to_image_plane=True,
    semantic_segmentation=True,
)
writer.attach([render_product])


def toggle_light(stage: Usd.Stage) -> None:
    """隨機決定每盞倉庫燈的開關狀態"""
    for i in range(7):
        suffix = "" if i == 0 else f"_{i:02d}"
        path = f"/Root/Warehouse/Lights/RectLight{suffix}"
        prim = stage.GetPrimAtPath(path)
        if not prim:
            continue

        # 每盞燈 50% 機率開或關
        vis = UsdGeom.Tokens.inherited if random.random() > 0.5 else UsdGeom.Tokens.invisible
        prim.GetAttribute("visibility").Set(vis)
        state = "ON" if vis == UsdGeom.Tokens.inherited else "OFF"
        print(f"  {path}: {state}")


async def go(num_frames=10):
    for i in range(num_frames):
        toggle_light(stage)
        # 等待渲染收斂後再截圖
        await asyncio.sleep(3)
        await rep.orchestrator.step_async()
        await asyncio.sleep(2)
        print(f"Frame {i + 1}/{num_frames} captured\n")

asyncio.ensure_future(go())
