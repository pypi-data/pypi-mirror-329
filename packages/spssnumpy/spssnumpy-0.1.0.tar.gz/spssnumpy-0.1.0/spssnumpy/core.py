import math

class Array:
    def __init__(self, data):
        if isinstance(data, list):
            self.data = data
            self.shape = self._infer_shape(data)
        else:
            raise TypeError("Input must be a list or nested list.")

    def _infer_shape(self, data):
        """Infer the shape of the array."""
        if isinstance(data[0], list):
            return (len(data), len(data[0]))
        return (len(data),)

    def __repr__(self):
        return f"Array({self.data})"

    # Arithmetic Operations
    def __add__(self, other):
        """Element-wise addition."""
        if self.shape != other.shape:
            raise ValueError("Arrays must have the same shape for addition.")
        result = [[self.data[i][j] + other.data[i][j] for j in range(self.shape[1])] for i in range(self.shape[0])]
        return Array(result)

    def __sub__(self, other):
        """Element-wise subtraction."""
        if self.shape != other.shape:
            raise ValueError("Arrays must have the same shape for subtraction.")
        result = [[self.data[i][j] - other.data[i][j] for j in range(self.shape[1])] for i in range(self.shape[0])]
        return Array(result)

    def __mul__(self, other):
        """Element-wise multiplication."""
        if self.shape != other.shape:
            raise ValueError("Arrays must have the same shape for element-wise multiplication.")
        result = [[self.data[i][j] * other.data[i][j] for j in range(self.shape[1])] for i in range(self.shape[0])]
        return Array(result)

    def __truediv__(self, other):
        """Element-wise division."""
        if self.shape != other.shape:
            raise ValueError("Arrays must have the same shape for element-wise division.")
        result = [[self.data[i][j] / other.data[i][j] for j in range(self.shape[1])] for i in range(self.shape[0])]
        return Array(result)

    def dot(self, other):
        """Matrix multiplication."""
        if self.shape[1] != other.shape[0]:
            raise ValueError("Number of columns in the first matrix must equal the number of rows in the second matrix.")
        result = [[sum(self.data[i][k] * other.data[k][j] for k in range(self.shape[1])) for j in range(other.shape[1])] for i in range(self.shape[0])]
        return Array(result)

    # Shape Manipulation
    def transpose(self):
        """Transpose the matrix."""
        transposed = [[self.data[j][i] for j in range(self.shape[0])] for i in range(self.shape[1])]
        return Array(transposed)

    def reshape(self, new_shape):
        """Reshape the array."""
        flat = [item for row in self.data for item in row]
        if len(flat) != new_shape[0] * new_shape[1]:
            raise ValueError("Cannot reshape array of size {} into shape {}".format(len(flat), new_shape))
        reshaped = [flat[i * new_shape[1]:(i + 1) * new_shape[1]] for i in range(new_shape[0])]
        return Array(reshaped)

    def flatten(self):
        """Flatten the array."""
        return Array([item for row in self.data for item in row])

    # Indexing and Slicing
    def __getitem__(self, index):
        """Access elements or slices."""
        if isinstance(index, tuple):
            row_idx, col_idx = index
            if isinstance(row_idx, slice) and isinstance(col_idx, slice):
                rows = self.data[row_idx]
                result = [row[col_idx] for row in rows]
                return Array(result)
            elif isinstance(row_idx, int) and isinstance(col_idx, int):
                return self.data[row_idx][col_idx]
        elif isinstance(index, int):
            return Array(self.data[index])
        raise IndexError("Invalid index type.")

    # Linear Algebra
    def determinant(self):
        """Calculate the determinant of a square matrix."""
        if self.shape[0] != self.shape[1]:
            raise ValueError("Determinant is only defined for square matrices.")
        if self.shape == (1, 1):
            return self.data[0][0]
        det = 0
        for col in range(self.shape[1]):
            minor = [[self.data[i][j] for j in range(self.shape[1]) if j != col] for i in range(1, self.shape[0])]
            det += ((-1) ** col) * self.data[0][col] * Array(minor).determinant()
        return det

    # Mathematical Functions
    def sum(self):
        """Sum of all elements."""
        return sum(sum(row) for row in self.data)

    def mean(self):
        """Mean of all elements."""
        total = sum(sum(row) for row in self.data)
        return total / (self.shape[0] * self.shape[1])

    def min(self):
        """Minimum value."""
        return min(min(row) for row in self.data)

    def max(self):
        """Maximum value."""
        return max(max(row) for row in self.data)

    def sin(self):
        """Apply sine to each element."""
        return Array([[math.sin(x) for x in row] for row in self.data])

    def cos(self):
        """Apply cosine to each element."""
        return Array([[math.cos(x) for x in row] for row in self.data])

    @staticmethod
    def zeros(shape):
        """Create an array filled with zeros."""
        return Array([[0 for _ in range(shape[1])] for _ in range(shape[0])])

    @staticmethod
    def ones(shape):
        """Create an array filled with ones."""
        return Array([[1 for _ in range(shape[1])] for _ in range(shape[0])])