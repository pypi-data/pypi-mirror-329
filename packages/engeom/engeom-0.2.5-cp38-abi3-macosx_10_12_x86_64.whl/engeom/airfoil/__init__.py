from ..engeom import _airfoil

# Global import of all functions
for name in [n for n in dir(_airfoil) if not n.startswith("_")]:
    globals()[name] = getattr(_airfoil, name)
