def add(a, b):
    """Add two numbers and return the result."""
    return a + b

def multiply(a, b):
    """Multiply two numbers and return the result."""
    return a * b

def divide(a, b):
    """Divide two numbers and return the result."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

class Calculator:
    """A simple calculator class."""
    
    def __init__(self):
        self.history = []
    
    def calculate(self, operation, a, b):
        """Perform calculation and store in history."""
        if operation == "add":
            result = add(a, b)
        elif operation == "multiply":
            result = multiply(a, b)
        elif operation == "divide":
            result = divide(a, b)
        else:
            raise ValueError(f"Unknown operation: {operation}")
        
        self.history.append(f"{operation}({a}, {b}) = {result}")
        return result
    
    def get_history(self):
        """Return calculation history."""
        return self.history

if __name__ == "__main__":
    # Sample usage
    calc = Calculator()
    
    print("Testing calculator functions:")
    print(f"5 + 3 = {add(5, 3)}")
    print(f"4 * 7 = {multiply(4, 7)}")
    print(f"10 / 2 = {divide(10, 2)}")
    
    print("\nTesting Calculator class:")
    result1 = calc.calculate("add", 15, 25)
    result2 = calc.calculate("multiply", 6, 8)
    result3 = calc.calculate("divide", 20, 4)
    
    print(f"Results: {result1}, {result2}, {result3}")
    print("History:")
    for entry in calc.get_history():
        print(f"  {entry}")