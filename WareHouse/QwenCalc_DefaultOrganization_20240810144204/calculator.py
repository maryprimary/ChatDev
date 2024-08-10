class Calculator:
    '''
    A Calculator class that performs basic arithmetic operations.
    '''
    def add(self, x, y):
        return x + y
    def subtract(self, x, y):
        return x - y
    def multiply(self, x, y):
        return x * y
    def divide(self, x, y):
        if y != 0:
            return x / y
        else:
            return "Error: Division by zero!"
    def clear(self):
        return 0