import numpy as np
from cobiformulate.formulate import OptimizationHelper, Constraint
import cobiformulate.cobi_cloud.cobi_cloud as cloud

class OptimizationProblem(OptimizationHelper):
    def __init__(self):
        super().__init__()
        self.variables = []
        self.constraints = []
        self.objective = None
        self.variable_names = []  # To store variable names
        self.full_variable_names = []  # To store all binary variables
        self.user_variable_count = 0
        self.converted_constraints_lambda_list = []
 
    def add_variable(self, base_name, vtype, lower_bound=0, upper_bound=1, count=1, resolution = 5):
        self.user_variable_count += count
        if count == 1:
            return self._add_variable_helper(base_name, vtype, lower_bound, upper_bound, resolution)
        return np.array([self._add_variable_helper(f"{base_name}{i}", vtype, lower_bound, upper_bound, resolution) for i in range(count)])

    def set_objective(self, expr):
        self.objective = expr

    def add_constraint(self, lhs, operator, rhs):
        if isinstance(lhs, np.ndarray) and isinstance(rhs, np.ndarray):
            if len(lhs) != len(rhs):
                raise ValueError("The number of expressions and constants must be the same.")
            for expr, const in zip(lhs, rhs):
                constraint = Constraint(expr, operator, float(const))
                self.constraints.append(constraint)
        else:
            constraint = Constraint(lhs, operator, rhs)
            self.constraints.append(constraint)

    def solve(self, timeoutSec = 1, target = -1e9, lam=None):
        if not self.has_converted_constraints:
            self._convert_constraints_and_move_to_objective()
        qubo = self._create_qubo(lam)
        
        if cloud.USE_CLOUD:
            solution = cloud.send_problem(qubo)
            solution = solution[0]
        else:
            import local_solver
            n = qubo.shape[0]
            solution = local_solver.cobisolv(n, qubo, timeoutSec, int(target))
        variable_values = self._spins_to_variables(solution)
        obj_value = self._compute_objective_value(solution)
        feasible = self._check_constraints(solution)
        sol = [value for key, value in variable_values.items()][:self.user_variable_count]
        return sol, obj_value, feasible

    def tune_lambda_and_solve(self, tuning_iterations = 5, timeoutSec = 1, target = -1e9, lam = None):
        if not self.has_converted_constraints:
            self._convert_constraints_and_move_to_objective()
        for _ in range(tuning_iterations):
            qubo = self._create_qubo(lam)
            if cloud.USE_CLOUD:
                solution = cloud.send_problem(qubo)
                solution = solution[0]
            else:
                import local_solver
                n = qubo.shape[0]
                solution = local_solver.cobisolv(n, qubo, timeoutSec, int(target))
            variable_values = self._spins_to_variables(solution)
            self._check_constraints_and_tune_lambda(solution)
        obj_value = self._compute_objective_value(solution)
        feasible = self._check_constraints(solution)
        sol = np.array([value for key, value in variable_values.items()][:self.user_variable_count])
        return sol, int(obj_value), feasible

    def __repr__(self):
        repr_str = "Optimization Problem\n"
        repr_str += "Variables:\n" + "\n".join(str(v) for v in self.variables) + "\n"
        if self.objective:
            repr_str += f"Objective:\n  {self.objective}\n"
        if self.constraints:
            repr_str += "Constraints:\n" + "\n".join(str(c) for c in self.constraints) + "\n"
        repr_str += "Variable Names:\n" + ", ".join(self.variable_names) + "\n"
        repr_str += "Full Variable Names:\n" + ", ".join(self.full_variable_names) + "\n"
        return repr_str

if __name__ == "__main__":
    cloud.connect("C0B1")
    prob2 = OptimizationProblem()
    N = 10
    x = prob2.add_variable("x", "I", lower_bound=0, upper_bound=15, count=N)
    c3 = -np.array([3, 4, 6, 2, 6, 9, 3, 2, 5, 9])
    A3 = np.array([
        [ 4,  3,  2, -3, -1, -2,  3,  4,  1, -3],
        [ 0,  1,  3,  1,  0,  1,  1, -3, -2, -2],
        [-2, -2, -2,  3,  4,  4,  1, -4, -1, -4],
        [ 1,  2, -2,  2,  2,  2, -4,  0, -1, -3],
        [-4, -3, -2, -2,  4, -3,  4, -3,  1,  3]
    ])
    b3 = np.array([59, 64, 77, 71, 38])
    prob2.set_objective(c3 @ x)
    prob2.add_constraint(A3 @ x, "<=", b3)
    s,o,f = prob2.solve()
    print(s,o,f)
    # fn = "lambda_tuning_results3.txt"
    # with open(fn, "w") as f:
    #     for _ in range(100):
    #         sol, obj_value, feasible = prob2.tune_lambda_and_solve(tuning_iterations=1, timeoutSec=2)
    #         print(sol.tolist(), int(obj_value), feasible)
    #         geo_mean_lambda = 1
    #         for i in prob2.converted_constraints_lambda_list:
    #             print(i[1], end=' ')
    #             geo_mean_lambda *= i[1]
    #         geo_mean_lambda = geo_mean_lambda ** (1/5)
    #         print()
    #         f.write(f"{int(obj_value)} {feasible} {geo_mean_lambda}\n")
