import omni.usd
from pxr import UsdGeom

stage = omni.usd.get_context().get_stage()

lights_to_disable = [
    "/Root/Warehouse/Lights/RectLight",
    "/Root/Warehouse/Lights/RectLight_01",
    "/Root/Warehouse/Lights/RectLight_02",
    "/Root/Warehouse/Lights/RectLight_03",
    "/Root/Warehouse/Lights/RectLight_04",
    "/Root/Warehouse/Lights/RectLight_05",
    "/Root/Warehouse/Lights/RectLight_06",
]

for path in lights_to_disable:
    prim = stage.GetPrimAtPath(path)
    if prim:
        UsdGeom.Imageable(prim).MakeInvisible()
        print(f"Disabled: {path}")
    else:
        print(f"Not found: {path}")

print(f"\nDone! Disabled {len(lights_to_disable)} lights.")
