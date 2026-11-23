import numpy as np

class JacobiSystem:
    def __init__(self, coefficients, absolute_values):
        self.coefficients = coefficients
        self.absolute_values = absolute_values
        self._verify()

        self.len = coefficients.shape[0]
        self.iteration = 0
        self.approximate_result = np.zeros(coefficients.shape[0])
        self.exact_result = np.linalg.solve(coefficients, absolute_values)

        self._update_error()


    def _verify(self):
        if self.coefficients.shape[0] != self.coefficients.shape[1]:
            raise ValueError("Coefficient matrix must be square.")
        if self.coefficients.shape[0] != self.absolute_values.shape[0]:
            raise ValueError("Coefficient matrix and absolute values vector must have compatible dimensions.")

        # Verify that the matrix is diagonally dominant
        for i in range(self.coefficients.shape[0]):
            diagonal_element = abs(self.coefficients[i][i])
            off_diagonal_sum = sum(abs(self.coefficients[i][j]) for j in range(self.coefficients.shape[1]) if j != i)
            if diagonal_element <= off_diagonal_sum:
                raise ValueError("Coefficient matrix must be diagonally dominant.")

    def _update_error(self):
        self.error = np.linalg.norm(self.exact_result - self.approximate_result)

    def iterate(self):
        new_solution = np.zeros(self.len)
        for calculation_variable_index in range(self.len):
            for coefficient_index in range(self.len):
                if coefficient_index != calculation_variable_index:
                    new_solution[calculation_variable_index] += - (self.coefficients[calculation_variable_index][coefficient_index] * self.approximate_result[coefficient_index] 
                                        / self.coefficients[calculation_variable_index][calculation_variable_index])
                else:
                    new_solution[calculation_variable_index] += self.absolute_values[calculation_variable_index] / self.coefficients[calculation_variable_index][calculation_variable_index]
        self.approximate_result = new_solution
        self._update_error()
        self.iteration += 1

    def iterate_to_low_error(self, error_threshold):
        while self.error > error_threshold:
            self.iterate()
            print(f"Iteration {self.iteration}: Approximate result = {self.approximate_result}, Error = {self.error}")

    


if __name__ == "__main__":
    coefficients = np.array([[10,1,-1], 
                            [-1,8,1], 
                            [1,-1,-20]])

    absolute_values = np.array([-2,1,3])


    system = JacobiSystem(coefficients, absolute_values)
    system.iterate_to_low_error(error_threshold=1e-5)

    exact_result = np.linalg.solve(coefficients, absolute_values) 

