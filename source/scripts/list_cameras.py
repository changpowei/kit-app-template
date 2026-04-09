import omni.usd
from pxr import UsdGeom

stage = omni.usd.get_context().get_stage()

print("=" * 80)
print("All cameras in stage:")
print("=" * 80)

count = 0
for prim in stage.Traverse():
    if prim.IsA(UsdGeom.Camera):
        count += 1
        print(f"\n[{count}] {prim.GetPath()}")

        for attr in prim.GetAttributes():
            val = attr.Get()
            if val is not None:
                print(f"    {attr.GetName()} = {val}")

print(f"\n{'=' * 80}")
print(f"Total cameras found: {count}")
print("=" * 80)
