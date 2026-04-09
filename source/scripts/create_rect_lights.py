import omni.usd
from pxr import UsdLux, UsdGeom, Gf

stage = omni.usd.get_context().get_stage()

# Create parent xform
UsdGeom.Xform.Define(stage, "/Root")
lights_xform = UsdGeom.Xform.Define(stage, "/Root/Lights")

# Move the Lights xform
lights_xform.AddTranslateOp().Set(Gf.Vec3d(-22, -19, 8.4))

# 6 columns (X) x 5 rows (Y), spacing X=5, Y=10
for col in range(6):
    for row in range(5):
        name = f"RectLight_{col}_{row}"
        path = f"/Root/Lights/{name}"
        light = UsdLux.RectLight.Define(stage, path)

        # Position
        x = col * 5
        y = row * 10
        UsdGeom.Xformable(light.GetPrim()).AddTranslateOp().Set(Gf.Vec3d(x, y, 0))

        # Light properties
        light.GetIntensityAttr().Set(5000)
        light.GetExposureAttr().Set(1.0)
        light.GetWidthAttr().Set(10.0)
        light.GetHeightAttr().Set(3.0)

print("Created 30 RectLights under /Root/Lights")
