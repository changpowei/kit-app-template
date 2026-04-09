import omni.usd
from pxr import UsdLux

stage = omni.usd.get_context().get_stage()

print("=" * 80)
print("All light sources in stage:")
print("=" * 80)

count = 0
for prim in stage.Traverse():
    # Check all UsdLux light types
    if prim.IsA(UsdLux.RectLight) or \
       prim.IsA(UsdLux.DiskLight) or \
       prim.IsA(UsdLux.SphereLight) or \
       prim.IsA(UsdLux.CylinderLight) or \
       prim.IsA(UsdLux.DistantLight) or \
       prim.IsA(UsdLux.DomeLight) or \
       prim.IsA(UsdLux.PortalLight) or \
       prim.HasAPI(UsdLux.LightAPI):

        light_api = UsdLux.LightAPI(prim)
        intensity = light_api.GetIntensityAttr().Get()
        exposure = light_api.GetExposureAttr().Get()
        visibility = prim.GetAttribute("visibility").Get()

        count += 1
        print(f"\n[{count}] {prim.GetPath()}")
        print(f"    Type:       {prim.GetTypeName()}")
        print(f"    Intensity:  {intensity}")
        print(f"    Exposure:   {exposure}")
        print(f"    Visibility: {visibility}")

print(f"\n{'=' * 80}")
print(f"Total lights found: {count}")
print("=" * 80)
