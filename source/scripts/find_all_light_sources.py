import omni.usd
from pxr import UsdLux, UsdShade, UsdGeom, Sdf

stage = omni.usd.get_context().get_stage()

# 1. 所有 UsdLux 燈光（含 DomeLight）
print("=" * 80)
print("1. UsdLux Lights (visible only):")
print("=" * 80)
count = 0
for prim in stage.Traverse():
    if prim.HasAPI(UsdLux.LightAPI) or \
       prim.IsA(UsdLux.DomeLight) or \
       prim.IsA(UsdLux.RectLight) or \
       prim.IsA(UsdLux.SphereLight) or \
       prim.IsA(UsdLux.DistantLight) or \
       prim.IsA(UsdLux.DiskLight) or \
       prim.IsA(UsdLux.CylinderLight):

        vis = prim.GetAttribute("visibility").Get()
        if vis == "invisible":
            continue

        light_api = UsdLux.LightAPI(prim)
        intensity = light_api.GetIntensityAttr().Get()
        count += 1
        print(f"  [{count}] {prim.GetPath()} ({prim.GetTypeName()}) intensity={intensity} vis={vis}")

# 2. DomeLight 專門搜尋
print(f"\n{'=' * 80}")
print("2. DomeLights (all, including invisible):")
print("=" * 80)
dome_count = 0
for prim in stage.Traverse():
    if prim.IsA(UsdLux.DomeLight):
        dome_count += 1
        vis = prim.GetAttribute("visibility").Get()
        intensity = UsdLux.LightAPI(prim).GetIntensityAttr().Get()
        texture = prim.GetAttribute("inputs:texture:file").Get() if prim.GetAttribute("inputs:texture:file") else "None"
        print(f"  [{dome_count}] {prim.GetPath()} intensity={intensity} vis={vis} texture={texture}")

if dome_count == 0:
    print("  No DomeLights found")

# 3. 檢查 Render Settings 中的環境光
print(f"\n{'=' * 80}")
print("3. Render Settings (environment/background):")
print("=" * 80)
import carb.settings
settings = carb.settings.get_settings()
keys_to_check = [
    "/rtx/useDefault",
    "/rtx/indirectDiffuse/enabled",
    "/rtx/directLighting/domeLight/enabled",
    "/rtx/sceneDb/ambientLightIntensity",
    "/rtx/iray/globalIllumination",
]
for key in keys_to_check:
    val = settings.get(key)
    if val is not None:
        print(f"  {key} = {val}")

# 4. 檢查 emissive 材質
print(f"\n{'=' * 80}")
print("4. Potentially emissive materials:")
print("=" * 80)
emissive_count = 0
for prim in stage.Traverse():
    if prim.IsA(UsdShade.Shader):
        emissive_attr = prim.GetAttribute("inputs:emissive_color")
        emissive_intensity = prim.GetAttribute("inputs:emissive_intensity")
        if emissive_intensity:
            val = emissive_intensity.Get()
            if val and val > 0:
                emissive_count += 1
                print(f"  [{emissive_count}] {prim.GetPath()} emissive_intensity={val}")

if emissive_count == 0:
    print("  No emissive materials found")

print(f"\n{'=' * 80}")
print("Done!")
print("=" * 80)
