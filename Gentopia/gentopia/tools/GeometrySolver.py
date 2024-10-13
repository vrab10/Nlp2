from typing import AnyStr, Any, Dict
from gentopia.tools.basetool import *
import math

class GeometryExpertArgs(BaseModel):
    shape: str = Field(..., description="The geometric shape to calculate (e.g., circle, square, triangle, sphere, cube)")
    operation: str = Field(..., description="The operation to perform (e.g., area, perimeter, volume, surface_area)")
    parameters: Dict[str, float] = Field(default={}, description="A dictionary of shape parameters (e.g., {'radius': 5} for a circle)")

class GeometryExpert(BaseTool):
    name = "geometry_expert"
    description = "An expert tool for performing geometric calculations using the math library."
    args_schema: Optional[Type[BaseModel]] = GeometryExpertArgs

    def _circle_calculations(self, operation, params):
        radius = params.get('radius')
        if radius is None:
            return "Error: Radius is required for circle calculations."
        if operation == 'area':
            return math.pi * radius ** 2
        elif operation == 'perimeter':
            return 2 * math.pi * radius
        else:
            return f"Error: Unsupported operation '{operation}' for circle."

    def _square_calculations(self, operation, params):
        side = params.get('side')
        if side is None:
            return "Error: Side length is required for square calculations."
        if operation == 'area':
            return side ** 2
        elif operation == 'perimeter':
            return 4 * side
        else:
            return f"Error: Unsupported operation '{operation}' for square."

    def _triangle_calculations(self, operation, params):
        if operation == 'area':
            base = params.get('base')
            height = params.get('height')
            if base is None or height is None:
                return "Error: Base and height are required for triangle area calculation."
            return 0.5 * base * height
        elif operation == 'perimeter':
            a, b, c = params.get('a'), params.get('b'), params.get('c')
            if a is None or b is None or c is None:
                return "Error: All three sides (a, b, c) are required for triangle perimeter calculation."
            return a + b + c
        else:
            return f"Error: Unsupported operation '{operation}' for triangle."

    def _sphere_calculations(self, operation, params):
        radius = params.get('radius')
        if radius is None:
            return "Error: Radius is required for sphere calculations."
        if operation == 'volume':
            return (4/3) * math.pi * radius ** 3
        elif operation == 'surface_area':
            return 4 * math.pi * radius ** 2
        else:
            return f"Error: Unsupported operation '{operation}' for sphere."

    def _cube_calculations(self, operation, params):
        side = params.get('side')
        if side is None:
            return "Error: Side length is required for cube calculations."
        if operation == 'volume':
            return side ** 3
        elif operation == 'surface_area':
            return 6 * side ** 2
        else:
            return f"Error: Unsupported operation '{operation}' for cube."

    def _run(self, shape: str, operation: str, parameters: Dict[str, float] = {}) -> Any:
        shape = shape.lower()
        operation = operation.lower()

        if not parameters:
            return f"Error: No parameters provided for {shape} {operation} calculation."

        if shape == 'circle':
            result = self._circle_calculations(operation, parameters)
        elif shape == 'square':
            result = self._square_calculations(operation, parameters)
        elif shape == 'triangle':
            result = self._triangle_calculations(operation, parameters)
        elif shape == 'sphere':
            result = self._sphere_calculations(operation, parameters)
        elif shape == 'cube':
            result = self._cube_calculations(operation, parameters)
        else:
            return f"Error: Unsupported shape '{shape}'."

        if isinstance(result, (int, float)):
            return f"The {operation} of the {shape} is approximately {result:.4f}"
        else:
            return result

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    expert = GeometryExpert()
    
    # Test cube volume
    print(expert._run("cube", "volume", {"side": 3}))
    
    # Test circle area
    print(expert._run("circle", "area", {"radius": 5}))
    
    # Test square perimeter
    print(expert._run("square", "perimeter", {"side": 4}))
    
    # Test triangle area
    print(expert._run("triangle", "area", {"base": 6, "height": 4}))
    
    # Test sphere volume
    print(expert._run("sphere", "volume", {"radius": 3}))
    
    # Test with missing parameters
    print(expert._run("cube", "volume", {}))