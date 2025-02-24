from ..engeom import _geom3

# Global import of all functions
for name in [n for n in dir(_geom3) if not n.startswith("_")]:
    globals()[name] = getattr(_geom3, name)
